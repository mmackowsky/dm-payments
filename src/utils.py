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
