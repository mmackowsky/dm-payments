from datetime import datetime

import stripe
from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from config import get_settings
from database import SessionLocal, engine
from models import Payment
from utils import save_data_to_db, set_new_id

settings = get_settings()

stripe.api_key = settings.STRIPE_API_KEY
db = SessionLocal()
app = FastAPI()


@app.get("/stripe/cancel", status_code=status.HTTP_200_OK)
async def cancel():
    return {"message": "Operation cancelled"}


@app.get("/stripe/success", status_code=status.HTTP_200_OK)
async def success():
    return {"message": "Operation ended successfully"}


# Endpoint to start payment
@app.get("/stripe/create-payment-session", status_code=status.HTTP_200_OK)
async def create_payment_session():
    try:
        # Tworzenie sesji płatności w Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Przykładowy produkt",
                        },
                        "unit_amount": 100,  # Cena w centach
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=f"http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/stripe/success",
            cancel_url=f"http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/stripe/cancel",
        )
        return session
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stripe/webhook")
async def webhook(request: Request, stripe_signature: str = Header(None)):
    event = None
    data = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=settings.STRIPE_WEBHOOK_KEY,
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    print("Unhandled event type {}".format(event["type"]))

    return {"status": "success"}


# Endpoint that redirect user to Stripe payment form
@app.get("/stripe/checkout")
async def checkout():
    return RedirectResponse(url="/stripe/create-payment-session", status_code=302)


if __name__ == "__main__":
    import uvicorn

    Payment.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
