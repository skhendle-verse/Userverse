from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class GenericResponseModel(BaseModel, Generic[T]):
    message: str
    data: Optional[T]
