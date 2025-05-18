from pydantic import BaseModel, EmailStr, Field
from app.models.company.roles import CompanyDefaultRoles
from app.models.user.user import UserRead


class CompanyUserRead(UserRead):
    role_name: str


class CompanyUserAdd(BaseModel):
    email: EmailStr = Field(None, example="user.one@email.com")
    role: str = Field(CompanyDefaultRoles.VIEWER.name_value, example="Viewer")
