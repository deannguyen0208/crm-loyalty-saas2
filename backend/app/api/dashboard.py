from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Employee, Order, OrderItem, Product

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _period_start(period: str) -> datetime:
    now = datetime.utcnow()
    if period == "week":
        return now - timedelta(days=7)
    if period == "month":
        return now - timedelta(days=30)
    if period == "quarter":
        return now - timedelta(days=90)
    return now - timedelta(days=365)


@router.get("/summary")
def summary(period: str = "month", db: Session = Depends(get_db)):
    start = _period_start(period)
    orders = db.query(Order).filter(Order.created_at >= start).all()
    revenue = sum(o.total_amount for o in orders)
    profit = sum(o.profit_amount for o in orders)
    return {
        "period": period,
        "order_count": len(orders),
        "revenue": revenue,
        "profit": profit,
        "margin": round((profit / revenue) * 100, 2) if revenue else 0,
    }


@router.get("/best-sellers")
def best_sellers(db: Session = Depends(get_db)):
    rows = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("qty"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    return [{"product": name, "quantity": int(qty)} for name, qty in rows]


@router.get("/employee-kpi")
def employee_kpi(db: Session = Depends(get_db)):
    revenue_by_employee = defaultdict(float)
    for employee_name, total in (
        db.query(Employee.name, func.sum(Order.total_amount))
        .join(Order, Employee.id == Order.employee_id)
        .group_by(Employee.name)
        .all()
    ):
        revenue_by_employee[employee_name] = float(total or 0)

    kpis = []
    for employee in db.query(Employee).all():
        revenue = revenue_by_employee[employee.name]
        completion = round((revenue / employee.target_revenue) * 100, 2) if employee.target_revenue else 0
        kpis.append(
            {
                "employee": employee.name,
                "role": employee.role,
                "revenue": revenue,
                "target": employee.target_revenue,
                "completion": completion,
            }
        )
    return kpis
