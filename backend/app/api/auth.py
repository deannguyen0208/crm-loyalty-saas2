from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Cần email hoặc số điện thoại")

    existing = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.phone)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tài khoản đã tồn tại")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        or_(User.email == payload.email_or_phone, User.phone == payload.email_or_phone)
    ).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Thông tin đăng nhập không hợp lệ")

    return TokenResponse(access_token=create_access_token(str(user.id)))
