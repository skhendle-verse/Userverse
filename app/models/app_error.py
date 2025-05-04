from pydantic import BaseModel


class DetailModel(BaseModel):
    message: str
    error: str


class AppErrorResponseModel(BaseModel):
    detail: DetailModel
