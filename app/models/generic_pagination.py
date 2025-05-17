# app/models/generic_pagination.py
from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    limit: int = Field(10, ge=1, le=10)
    offset: int = Field(0, ge=0)


T = TypeVar("T")


class PaginationMeta(BaseModel):

    total_records: int
    limit: int
    offset: int
    current_page: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    records: List[T]
    pagination: PaginationMeta
