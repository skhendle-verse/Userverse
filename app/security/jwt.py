# The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
from fastapi import Security, Header, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from app.configs import get_configs
from app.configs import get_configs
from app.utils.app_error import AppError
import jwt
from typing import Optional

from datetime import datetime


configs = get_configs()
JWT_SECRET = configs.get("SECRET")
JWT_ALGORITHM = configs.get("ALGORITHM")


def decodeJWT(token: str, verify_options: bool = True) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            # verify=verify_options,
            options={"verify_signature": verify_options},
        )
        expire = datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S")

        if verify_options:
            if datetime.utcnow() >= expire:
                raise jwt.ExpiredSignatureError

        return decoded_token
    except jwt.ExpiredSignatureError as e:
        pass
        # raise AppError(
        #     status_code=status.HTTP_410_GONE,
        #     message="Token has expired.",
        #     error=str(e),
        # )
    except jwt.InvalidTokenError as e:
        raise AppError(
            status_code=status.HTTP_410_GONE,
            message="Invalid token.",
            error=str(e),
        )
    except Exception as e:
        raise AppError(
            status_code=status.HTTP_410_GONE,
            message="Token Validation Error, Please Try Again",
            error=str(e),
        )


async def get_current_user(
    auth: str = Security(APIKeyHeader(name="Authorization")),
) -> dict:

    if auth is None:
        raise AppError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid Request",
            error="Missing Authorization Headers, {'Authorization': 'Bearer TOKEN'}",
        )

    try:
        auth_type, TOKEN = auth.split(" ")
        if auth_type != "Bearer":
            raise AppError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid Request",
                error="Missing Authorization TYPE, {'Authorization': 'Bearer TOKEN'}",
            )
    except Exception as e:
        raise AppError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid Request",
            error=str(e),
        )

    current_user = decodeJWT(token=TOKEN).get("user", {})

    return current_user


# define the APIKeyHeader dependency
async def api_key_dependency(expired_token: Optional[str] = Header(None)):
    current_user = decodeJWT(
        token=expired_token,
        verify_options=False,
    ).get("user", {})

    return current_user


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AppError(
                    status_code=status.HTTP_403_FORBIDDEN,
                    message="Invalid Authentication Scheme.",
                )
            if not self.verify_jwt(credentials.credentials):
                raise AppError(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Invalid Auth Token.",
                )
            return credentials.credentials
        else:
            raise AppError(
                status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid Auth Token."
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        payload = decodeJWT(jwtoken)

        if payload:
            isTokenValid = True
        return isTokenValid
