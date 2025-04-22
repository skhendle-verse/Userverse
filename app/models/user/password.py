from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.utils.hash_password import pwd_context


class PasswordResetRequest(BaseModel):
    email: EmailStr


class OTPValidationRequest(BaseModel):
    email: EmailStr
    otp: str


class PasswordResetConfirm(BaseModel):
    token: str  # from OTP validation step
    new_password: str

    @validator("new_password", pre=True)
    def hash_password(cls, v: str) -> str:
        return pwd_context.hash(v)
