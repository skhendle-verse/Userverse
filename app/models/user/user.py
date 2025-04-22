from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from app.utils.hash_password import pwd_context


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    password: str

    @validator("new_password", pre=True)
    def hash_password(cls, v: str) -> str:
        return pwd_context.hash(v)


class UserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
