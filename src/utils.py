from sqlalchemy import desc

from database import SessionLocal
from models import Subscription


async def save_data_to_db(
    db: SessionLocal,
    id: int,
    user: int,
    amount: float,
    currency: str,
    date: str,
    status: str,
):
    data = Subscription(
        id=id,
        user=user,
        amount=amount,
        currency=currency,
        date=date,
        status=status,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def set_new_id(db: SessionLocal):
    last_object_id = db.query(Subscription).order_by(desc(Subscription.id)).first()
    next_id = (last_object_id.id + 1) if last_object_id.id else 1
    return next_id


def delete_last_item(db):
    try:
        last_item = db.query(Subscription).order_by(Subscription.id.desc()).first()

        if last_item:
            db.delete(last_item)
            db.commit()
            return {"message": "Last element has been removed."}
        else:
            return {"message": "No elements to remove."}
    finally:
        db.close()
