from datetime import datetime

import stripe
from fastapi import FastAPI, HTTPException, Request

from config import get_settings
from database import SessionLocal, engine
from models import Payment
from utils import save_data_to_db, set_new_id

settings = get_settings()

stripe.api_key = settings.STRIPE_API_KEY
db = SessionLocal()
app = FastAPI()


@app.post("api/process-payment/")
async def process_payment(request: Request, amount: int, currency: str, token: str):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,  # Stripe token obtained from the client-side (e.g., Stripe.js)
            description="Payment for FastAPI Store",
        )
        await save_data_to_db(
            db=db,
            id=set_new_id(db),
            user=int(request.headers.get("request-user-id")),
            amount=amount,
            currency=currency,
            date=str(datetime.now()),
            description="Payment for FastAPI Store",
            status="success",
        )
        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        await save_data_to_db(
            db=db,
            id=set_new_id(db),
            user=int(request.headers.get("request-user-id")),
            amount=amount,
            currency=currency,
            date=str(datetime.now()),
            description="Payment for FastAPI Store",
            status="error",
        )
        return {"status": "error", "message": str(e)}

    except stripe.error.StripeError as e:
        await save_data_to_db(
            db=db,
            id=set_new_id(db),
            user=int(request.headers.get("request-user-id")),
            amount=amount,
            currency=currency,
            date=str(datetime.now()),
            description="Payment for FastAPI Store",
            status="error",
        )
        return {
            "status": "error",
            "message": "Something went wrong. Please try again later.",
        }


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    Payment.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
