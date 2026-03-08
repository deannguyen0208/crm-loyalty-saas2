from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    staff_name = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)  # zalopay, momo, bank_transfer, cash
    cost_amount = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
