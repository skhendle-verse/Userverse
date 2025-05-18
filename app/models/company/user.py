from pydantic import BaseModel, EmailStr, field_validator, Field
from app.models.company.roles import CompanyDefaultRoles
from app.utils.hash_password import hash_password
from app.models.phone_number import validate_phone_number_format


class AddUser(BaseModel):
    email: EmailStr = Field(None, example="user.one@email.com")
    role: str = Field(CompanyDefaultRoles.VIEWER.name_value, example="Viewer")