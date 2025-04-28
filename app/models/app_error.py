from pydantic import BaseModel


class AppErrorModel(BaseModel):
    message: str
    details: str
