import re
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, field_validator, Field
from app.utils.hash_password import hash_password
from app.models.phone_number import validate_phone_number_format


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
        return validate_phone_number_format(v)


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        return validate_phone_number_format(v)


class UserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None


class TokenResponseModel(BaseModel):
    token_type: Literal["bearer"] = Field(
        "bearer",
        description="Type of the token",
    )
    access_token: str = Field(..., description="JWT access token")
    access_token_expiration: str = Field(
        ..., description="Access token expiration time in 'YYYY-MM-DD HH:MM:SS' format"
    )
    refresh_token: str = Field(..., description="JWT refresh token")
    refresh_token_expiration: str = Field(
        ..., description="Refresh token expiration time in 'YYYY-MM-DD HH:MM:SS' format"
    )
