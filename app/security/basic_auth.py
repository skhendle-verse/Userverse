from fastapi import Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils.app_error import AppError
from app.models.user import UserLogin
security = HTTPBasic()


def get_basic_auth_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    email = credentials.username
    if not email:
        raise AppError("Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    password = credentials.password
    if not password:
        raise AppError("Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)

    inputs = UserLogin(email=credentials.username, password=password)
    return inputs
