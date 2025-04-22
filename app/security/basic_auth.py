from fastapi import Depends, status, Security, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials, APIKeyHeader
from email_validator import validate_email, EmailNotValidError
from app.configs import get_configs
from app.exceptions import AppError
from app.features.agent_auth_service.model import AgentLoginModel
import jwt
from typing import Optional

from datetime import datetime

security = HTTPBasic()
configs = get_configs()


def validate_email_format(email: str):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        raise AppError(status_code=400, message="Invalid Email Format", error=str(e))


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    email = validate_email_format(credentials.username)
    password = credentials.password
    inputs = AgentLoginModel(email=email, password=password)
    return inputs
