from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    segment = Column(String, default="regular")
    loyalty_points = Column(Integer, default=0)
    total_spent = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
