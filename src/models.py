from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
