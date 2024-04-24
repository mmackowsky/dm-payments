import stripe
from fastapi import FastAPI, HTTPException

from config import get_settings

settings = get_settings()

stripe.api_key = settings.STRIPE_API_KEY

app = FastAPI()


@app.post("/process-payment/")
async def process_payment(amount: int, currency: str, token: str):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,  # Stripe token obtained from the client-side (e.g., Stripe.js)
            description="Payment for FastAPI Store",
        )

        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        return {
            "status": "error",
            "message": "Something went wrong. Please try again later.",
        }


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
