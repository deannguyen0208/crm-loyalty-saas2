from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, campaigns, customers, dashboard, orders
from app.core.config import settings
from app.core.database import Base, engine
from app.models import campaign, customer, order, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(customers.router, prefix=settings.api_prefix)
app.include_router(orders.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)
app.include_router(campaigns.router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "Cafe Loyalty SaaS API running"}
