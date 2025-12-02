import stripe
import os
from fastapi import APIRouter, Depends, HTTPException

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
router = APIRouter()

@router.post("/create_payment_intent")
def create_intent(ride_id: int, amount: int): # Amount in cents
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            metadata={"ride_id": str(ride_id)},
            payment_method_types=["card"],
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Webhook endpoint for ride completion capture
@router.post("/webhook")
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    if event['type'] == 'payment_intent.succeeded':
        # Capture funds, update ride status
        pass
    return {"status": "success"}
