from datetime import datetime
from pydantic import BaseModel


class OrderItemIn(BaseModel):
    product_name: str
    quantity: int
    unit_price: float


class OrderCreateRequest(BaseModel):
    employee_name: str
    payment_method: str
    total_amount: float
    profit_amount: float
    created_at: datetime | None = None
    items: list[OrderItemIn]


class PaymentRecord(BaseModel):
    method: str
    amount: float
    note: str | None = None
