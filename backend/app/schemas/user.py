from pydantic import BaseModel, field_validator

from app.core.security import validate_strong_password


class RegisterRequest(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        if not validate_strong_password(value):
            raise ValueError(
                "Mật khẩu phải có tối thiểu 10 ký tự gồm chữ hoa, chữ thường, số và ký tự đặc biệt"
            )
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str | None) -> str | None:
        if value and "@" not in value:
            raise ValueError("Email không hợp lệ")
        return value

    @field_validator("phone")
    @classmethod
    def check_contact(cls, value: str | None) -> str | None:
        if value and not value.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa chữ số")
        return value


class LoginRequest(BaseModel):
    email_or_phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
