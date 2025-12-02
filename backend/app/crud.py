
from http.client import HTTPException
#from backend.app import schemas
from . import models, schemas
from .models import AllowedDomain
#from .database import SessionLocal
from sqlalchemy.orm import Session

def is_email_allowed(db: Session, email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return db.query(AllowedDomain).filter(
        AllowedDomain.domain == domain,
        AllowedDomain.is_active == True
    ).first() is not None

def create_user(db: Session, user: schemas.UserCreate):
    if not is_email_allowed(db, user.email):
        raise HTTPException(status_code=403, detail="Email domain not authorized. Contact your admin.")
    
    # Rest same as before
    #hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email.lower(),
        full_name=user.full_name,
        phone=user.phone,
       # hashed_password=hashed_password,
        is_driver=False,
        is_verified=True # Auto-verified for corporate emails
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user