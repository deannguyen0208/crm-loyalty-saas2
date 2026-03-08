from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Employee, Order, OrderItem, Product
from app.schemas.customer import OrderCreateRequest

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("")
def create_order(payload: OrderCreateRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.name == payload.employee_name).first()
    if not employee:
        employee = Employee(name=payload.employee_name)
        db.add(employee)
        db.flush()

    order = Order(
        employee_id=employee.id,
        payment_method=payload.payment_method,
        total_amount=payload.total_amount,
        profit_amount=payload.profit_amount,
        created_at=payload.created_at or datetime.utcnow(),
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        product = db.query(Product).filter(Product.name == item.product_name).first()
        if not product:
            product = Product(name=item.product_name, price=item.unit_price)
            db.add(product)
            db.flush()

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )

    db.commit()
    return {"message": "Đã ghi nhận đơn hàng", "order_id": order.id}
