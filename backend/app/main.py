#from backend.app import models
from sqlalchemy import Boolean
from .database import get_db
from datetime import datetime
from fastapi import Body, FastAPI, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from . import crud, schemas, auth, maps, payments,models, background, reviews
#from .dependencies import get_db
import os
import redis
from celery import Celery
from .auth import MagicLinkToken

#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Neighboride - Carpool",description="Company email only .Magic link login . Full scaling")

# Scaling: Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Scaling: Redis for real-time
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Scaling: Celery for jobs
celery = Celery(__name__, broker=os.getenv("REDIS_URL"))
celery.autodiscover_tasks(["app"])

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
#@limiter.limit("5/minute")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/request-magic-link")
def request_magic_link(email: str = Body(...,embed=True), db: Session = Depends(get_db)):
    print('request received')
    return auth.create_magic_link(db, email)

@app.get("/auth/magic")
def magic_login(token: str, db: Session = Depends(get_db)):
    db_token = db.query(auth.MagicLinkToken).filter(
        MagicLinkToken.token == token,
        MagicLinkToken.used == False,
        MagicLinkToken.expires_at > datetime.utcnow()).first()
    if not db_token:
        raise HTTPException(400, "Invalid or expired link")
    
    user = crud.get_user_by_email(db, db_token.email)
    if not user:
        raise HTTPException(404, "User not found")
    
    db_token.used = True
    db.commit()
    
    access_token = auth.create_access_token({"sub": user.email})
    # Redirect to app with token
    return {"access_token": access_token, "redirect": "/dashboard"}


# Routes (abbreviated—full CRUD in crud.py)
#@app.post("/register", response_model=schemas.User)
#@limiter.limit("5/minute")
#def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
 #   return crud.create_user(db, user)

@app.post("/rides", response_model=schemas.Ride)
#@limiter.limit("10/minute")
def create_ride(ride: schemas.RideCreate, db: Session = Depends(get_db), current_user:models.User = Depends(auth.get_current_user)):
    if not current_user.is_verified:
        raise HTTPException(403, "Verify first")
    ride.origin_lat, ride.origin_lng = maps.geocode_address(ride.origin)
    ride.dest_lat, ride.dest_lng = maps.geocode_address(ride.destination)
   # ride.surge_multiplier = matching.calculate_surge_multiplier()
    new_ride = crud.create_ride(db, ride, current_user.id)
    # Notify via Celery
   # notifications.send_booking_alert.delay(current_user.id, new_ride.id)
    # Redis pub for real-time
    redis_client.publish("ride_updates", f"new:{new_ride.id}")
    return new_ride

#@app.get("/rides/search")
#def search_rides(origin: str, destination: str, db: Session = Depends(get_db)):
 #   return matching.get_next_driver_in_rotation(db, origin, destination) # Rotation logic

# Bookings + Stripe
@app.post("/bookings")
def book_ride(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    db_booking = crud.create_booking(db, booking, current_user.id)
    # Create Stripe intent
    amount = booking.seats_booked * db_booking.ride.price_per_seat * 100
    intent = payments.create_intent(db_booking.ride.id, amount)
    db_booking.ride.stripe_payment_intent = intent["client_secret"]
    db.commit()
    return db_booking

# Background Check
@app.post("/background_check")
def start_check(current_user = Depends(auth.get_current_user)):
    report_id = background.initiate_background_check(current_user.id, current_user.email)
    current_user.is_verified = True # Simulate approval
    return {"report_id": report_id}

# Reviews
app.include_router(reviews.router, prefix="/reviews")

# WebSocket for real-time
connected_clients = []

# Admin routes (protected)
@app.get("/admin/users")
def admin_users(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.email != "admin@neighboride.com":
        raise HTTPException(403, "Admin only")
    return db.query(models.User).all()

# More routes: /bookings, /reviews, /subscriptions, /background_check, /incentives
# Webhook for Stripe: payments.stripe_webhook
# Admin: /admin/users (protected)
# Admin routes (protected)
@app.get("/admin/users")
def admin_users(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.email != "admin@neighboride.com":
        raise HTTPException(403, "Admin only")
    return db.query(models.User).all()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    pubsub.subscribe("ride_updates")
    try:
        for message in pubsub.listen():
            await websocket.send_text(message["data"])
    except Exception:
        pubsub.unsubscribe("ride_updates")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, workers=8) # Scaling: 8 workers
