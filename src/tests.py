import datetime
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import get_db
from main import app
from models import Subscription
from utils import delete_last_item

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Subscription.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestStripeEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.client = TestClient(app)
        self.db = TestingSessionLocal()
        subscription = Subscription(
            id=1,
            user=1,
            amount=10,
            currency="usd",
            last_payment_date=datetime.datetime(2020, 1, 1),
            next_payment_date=datetime.datetime(2020, 2, 1),
            status="active",
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        self.db.close()

    def tearDown(self):
        db = TestingSessionLocal()
        db.query(Subscription).delete()
        db.commit()
        db.close()

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

    # @patch("main.stripe.Webhook.construct_event")
    def test_webhook_subscription_created(self, mock_construct_event):
        subscriptions_before = self.db.query(Subscription).all()
        # Mock event
        mock_construct_event.return_value = {"type": "customer.subscription.created"}

        # Call endpoint /stripe/webhook
        response = self.client.post(
            "/stripe/webhook", headers={"stripe_signature": "test_signature"}
        )

        self.assertEqual(response.status_code, 200)

        # Check that new object has been created

        subscriptions_after = self.db.query(Subscription).all()

        self.assertEqual(len(subscriptions_before), len(subscriptions_after) - 1)

        # Deleting item from database
        delete_last_item(self.db)


if __name__ == "__main__":
    unittest.main()
