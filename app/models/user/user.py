import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.utils.hash_password import hash_password


PHONE_NUMBER_REGEX = re.compile(
    r"^\+?\d{10,15}$"
)  # Allows optional "+" and 10-15 digits


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def hash_password(cls, v: str) -> str:
        return hash_password(v)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def hash_password(cls, v: str) -> str:
        return hash_password(v)

    @field_validator("phone_number")
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        if v and not PHONE_NUMBER_REGEX.match(v):
            raise ValueError(
                "Invalid phone number format. Must be 10-15 digits, optional leading '+'."
            )
        return v


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        if v and not PHONE_NUMBER_REGEX.match(v):
            raise ValueError(
                "Invalid phone number format. Must be 10-15 digits, optional leading '+'."
            )
        return v


class UserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
