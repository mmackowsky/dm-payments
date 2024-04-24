from sqlalchemy import desc

from database import SessionLocal
from models import Payment


async def save_data_to_db(
    db: SessionLocal,
    id: int,
    user: int,
    amount: float,
    currency: str,
    date: str,
    description: str,
    status: str,
):
    data = Payment(
        id=id,
        user=user,
        amount=amount,
        currency=currency,
        date=date,
        description=description,
        status=status,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def set_new_id(db: SessionLocal):
    last_object_id = db.query(Payment).order_by(desc(Payment.id)).first()
    next_id = (last_object_id.id + 1) if last_object_id.id else 1
    return next_id
