from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).order_by(Customer.created_at.desc()).all()


@router.post("", response_model=CustomerOut)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(name=payload.name, phone=payload.phone, segment=payload.segment)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
