import re
from typing import Optional, Literal
from app.models.company.address import CompanyAddress
from pydantic import BaseModel, EmailStr, field_validator, Field
from app.models.phone_number import validate_phone_number_format

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[CompanyAddress] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        return validate_phone_number_format(v)

class CompanyCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    phone_number: Optional[str] = None
    email: EmailStr
    address: Optional[CompanyAddress] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        return validate_phone_number_format(v)