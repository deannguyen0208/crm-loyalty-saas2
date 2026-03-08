from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Order
from app.schemas.customer import PaymentRecord

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/record")
def record_payment(payload: PaymentRecord, db: Session = Depends(get_db)):
    order = Order(payment_method=payload.method, total_amount=payload.amount, profit_amount=payload.amount * 0.25)
    db.add(order)
    db.commit()
    return {"message": "Đã ghi nhận thanh toán", "method": payload.method, "amount": payload.amount}


@router.get("/breakdown")
def payment_breakdown(db: Session = Depends(get_db)):
    stats = defaultdict(float)
    for method, amount in db.query(Order.payment_method, Order.total_amount).all():
        stats[method] += float(amount)
    return [{"method": method, "revenue": revenue} for method, revenue in stats.items()]
