from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, campaigns, customers, dashboard, orders, payments
from app.core.config import settings
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(dashboard.router)
app.include_router(payments.router)
app.include_router(campaigns.router)
app.include_router(customers.router)


@app.get("/")
def root():
    return {"message": "Cafe SaaS API is running"}
