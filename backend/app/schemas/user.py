from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    phone: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    identifier: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
