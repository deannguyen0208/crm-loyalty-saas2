from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone: str
    segment: str = "regular"


class CustomerOut(BaseModel):
    id: int
    name: str
    phone: str
    segment: str
    loyalty_points: int
    total_spent: float

    class Config:
        from_attributes = True
