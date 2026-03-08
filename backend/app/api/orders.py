from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.customer import Customer
from app.models.order import Order

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderCreate(BaseModel):
    customer_id: int | None = None
    staff_name: str
    item_name: str
    quantity: int = 1
    total_amount: float
    cost_amount: float
    payment_method: str


@router.get("")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()


@router.post("")
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = Order(**payload.model_dump())
    db.add(order)

    if payload.customer_id:
        customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()
        if customer:
            customer.total_spent += payload.total_amount
            customer.loyalty_points += int(payload.total_amount // 10000)

    db.commit()
    db.refresh(order)
    return order


@router.post("/seed-demo")
def seed_demo_orders(db: Session = Depends(get_db)):
    if db.query(Order).first():
        return {"message": "Đã có dữ liệu"}

    samples = [
        ("Lan", "Latte", 2, 120000, 60000, "momo"),
        ("Minh", "Cold Brew", 1, 45000, 20000, "zalopay"),
        ("An", "Espresso", 3, 90000, 40000, "bank_transfer"),
        ("Lan", "Bạc xỉu", 2, 80000, 35000, "momo"),
        ("Minh", "Matcha Latte", 1, 55000, 25000, "zalopay"),
    ]

    for i, (staff, item, qty, amount, cost, method) in enumerate(samples):
        order = Order(
            staff_name=staff,
            item_name=item,
            quantity=qty,
            total_amount=amount,
            cost_amount=cost,
            payment_method=method,
            created_at=datetime.utcnow(),
        )
        db.add(order)

    db.commit()
    return {"message": "Đã tạo dữ liệu demo"}
