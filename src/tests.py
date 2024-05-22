import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from config import get_settings
from database import SessionLocal
from main import app
from models import Subscription
from utils import delete_last_item

db = SessionLocal()
settings = get_settings()


class TestStripeEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.stripe.checkout.Session.create")
    def test_create_payment_session(self, mock_create_session):
        # Mock event
        mock_create_session.return_value = MagicMock(id="test_session_id")

        # Call endpoint /stripe/create-payment-session
        response = self.client.get("/stripe/create-payment-session")

        self.assertEqual(response.status_code, 200)

        mock_create_session.assert_called_once_with(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Subscription"},
                        "unit_amount": 1000,
                        "recurring": {"interval": "month"},
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/stripe/success",
            cancel_url=f"http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/stripe/cancel",
        )

    @patch("main.stripe.Webhook.construct_event")
    def test_webhook_subscription_created(self, mock_construct_event):
        # subscriptions_before = db.query(Subscription).all()
        # Mock event
        mock_construct_event.return_value = {"type": "customer.subscription.created"}

        # Call endpoint /stripe/webhook
        response = self.client.post(
            "/stripe/webhook", headers={"stripe_signature": "test_signature"}
        )

        self.assertEqual(response.status_code, 200)
        #
        # # Check that new object has been created
        #
        # subscriptions_after = db.query(Subscription).all()
        #
        # self.assertEqual(len(subscriptions_before), len(subscriptions_after) - 1)
        #
        # # Deleting item from database
        # delete_last_item(db)


if __name__ == "__main__":
    unittest.main()
