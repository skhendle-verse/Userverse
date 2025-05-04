from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.utils.hash_password import hash_password


class PasswordResetRequest(BaseModel):
    email: EmailStr


class OTPValidationRequest(BaseModel):
    otp: str
