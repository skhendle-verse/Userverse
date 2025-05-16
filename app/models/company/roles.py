from enum import Enum
from typing import Optional
from pydantic import BaseModel


class CompanyDefaultRoles(str, Enum):
    ADMINISTRATOR = "Administrator: Full access to manage users and data"
    VIEWER = "Viewer: Read-only access to company data"

    @property
    def name_value(self) -> str:
        """Returns just the role name (e.g., 'Administrator')."""
        return self.value.split(":")[0].strip()

    @property
    def description(self) -> str:
        """Returns just the role description."""
        return self.value.split(":", 1)[1].strip()


class RoleCreate(BaseModel):
    name: str
    description: Optional[str]


class RoleUpdate(BaseModel):
    description: Optional[str]


class RoleRead(BaseModel):
    name: str
    description: Optional[str]
