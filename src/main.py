from datetime import datetime

import stripe
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from config import get_settings
from database import SessionLocal, engine
from models import Payment
from utils import save_data_to_db, set_new_id

settings = get_settings()

stripe.api_key = settings.STRIPE_API_KEY
db = SessionLocal()
app = FastAPI()


@app.get("/stripe/cancel")
async def cancel():
    return {"message": "Operation cancelled"}


# Endpoint that redirect user to Stripe payment form
@app.get("/stripe/checkout")
async def checkout():
    return RedirectResponse(url="/stripe/create-payment-session", status_code=302)


if __name__ == "__main__":
    import uvicorn

    Payment.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
