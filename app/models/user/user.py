from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.utils.hash_password import pwd_context


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def hash_password(cls, v: str) -> str:
        return pwd_context.hash(v)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def hash_password(cls, v: str) -> str:
        return pwd_context.hash(v)


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
