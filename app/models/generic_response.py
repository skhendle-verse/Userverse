from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

# Type variable for any Pydantic model
T = TypeVar("T")

class GenericResponseModel(GenericModel, Generic[T]):
    message: str
    data: Optional[T]  # data can be any model or None
