from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.utils.hash_password import hash_password


class PasswordResetRequest(BaseModel):
    email: EmailStr


class OTPValidationRequest(BaseModel):
    email: EmailStr
    otp: str


class PasswordResetConfirm(BaseModel):
    token: str  # from OTP validation step
    new_password: str

    @field_validator("password")
    def hash_password(cls, v: str) -> str:
        return hash_password(v)