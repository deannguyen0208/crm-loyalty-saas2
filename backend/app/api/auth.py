from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_password_hash,
    validate_password_strength,
    verify_password,
)
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    valid, message = validate_password_strength(payload.password)
    if not valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    exists = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.phone)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email hoặc số điện thoại đã tồn tại")

    user = User(
        email=payload.email,
        phone=payload.phone,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(or_(User.email == payload.identifier, User.phone == payload.identifier)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")

    return TokenResponse(access_token=create_access_token(str(user.id)))
