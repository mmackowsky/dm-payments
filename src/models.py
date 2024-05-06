from datetime import timedelta

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False, default=1000, doc="Given in cents")
    currency = Column(String, nullable=False, default="usd")
    last_payment_date = Column(DateTime, nullable=False)
    next_payment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="inactive")

    def __repr__(self):
        return f"<Payment(id={self.id}, last_payment_date={self.last_payment_date}, next_payment_date={self.next_payment_date})>"
