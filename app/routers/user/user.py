import traceback
from fastapi import APIRouter, Depends, status
from app.configs import configs
from app.models.user.user import UserLogin, UserCreate, UserRead, UserUpdate

from app.security.basic_auth import get_basic_auth_credentials
from app.utils.app_error import AppError
from app.models.user.errors import UserErrorMessages
router = APIRouter()
tag = "User Management"


@router.post("/user", tags=[tag], response_model=UserRead)
def create_user_api(
    user: UserCreate,
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    try:
        pass
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserErrorMessages.USER_CREATION_FAILED.value,
            error=str(e),
        )


@router.post("/user/login", tags=[tag])
def login_user_api(
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    try:
        pass
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserErrorMessages.INVALID_CREDENTIALS.value,
            error=str(e),
        )
    


# This must use thr jwt token
@router.get("/user", tags=[tag], response_model=UserRead)
def get_user_api(
    jwt_token: UserLogin = Depends(get_basic_auth_credentials),
):
    try:
        pass
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserErrorMessages.INVALID_REQUEST_MESSAGE.value,
            error=str(e),
        )
    
@router.patch("/user", tags=[tag], response_model=UserRead)
def update_user_api(
    user: UserUpdate,
    jwt_token: UserLogin = Depends(get_basic_auth_credentials),
):
    try:
        pass
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserErrorMessages.USER_UPDATE_FAILED.value,
            error=str(e),
        )