from pydantic import BaseModel, Field
from typing import Optional

class CompanyAddress(BaseModel):
    street: Optional[str] = Field(None, example="123 Main St")
    city: Optional[str] = Field(None, example="Cape Town")
    state: Optional[str] = Field(None, example="CT")
    postal_code: Optional[str] = Field(None, example="8000")
    country: Optional[str] = Field(None, example="South Africa")
