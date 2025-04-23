import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.configs import configs
from app.models.app_error import AppErrorModel
from app.models.user.user import UserLogin, UserCreate, UserRead, UserUpdate

from app.security.basic_auth import get_basic_auth_credentials
from app.utils.app_error import AppError
from app.models.user.messages import UserResponseMessages

# logic
from app.logic.user.user import UserService

router = APIRouter()
tag = "User Management"


@router.post(
    "/user",
    tags=[tag],
    response_model=UserRead,
    responses={
        201: {"model": UserRead},
        400: {"model": AppErrorModel},
        500: {"model": AppErrorModel},
    },
)
def create_user_api(
    user: UserCreate,
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    """
    Create a new user.
    """
    try:
        response = UserService().create_user(
            user_credentials=credentials,
            user_data=user,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": UserResponseMessages.USER_CREATED.value,
                "data": response.model_dump(),
            },
        )
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserResponseMessages.USER_CREATION_FAILED.value,
            error=str(e),
        )


# This must use thr jwt token
@router.get(
    "/user",
    tags=[tag],
    responses={
        200: {"model": UserRead},
        400: {"model": AppErrorModel},
        500: {"model": AppErrorModel},
    },
)
def get_user_api(
    jwt_token: UserLogin = Depends(get_basic_auth_credentials),
):
    """
    Get user details.
    """
    try:
        response = UserService().get_user(user_email=jwt_token.email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": UserResponseMessages.USER_FOUND.value,
                "data": response.model_dump(),
            },
        )
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserResponseMessages.INVALID_REQUEST_MESSAGE.value,
            error=str(e),
        )


@router.patch(
    "/user/login",
    tags=[tag],
    responses={
        202: {"model": UserRead},
        400: {"model": AppErrorModel},
        500: {"model": AppErrorModel},
    },
)
def login_user_api(
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    """
    User login.
    """
    try:
        response = UserService().user_login(user_credentials=credentials)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": UserResponseMessages.USER_LOGGED_IN.value,
                "data": response.model_dump(),
            },
        )
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserResponseMessages.INVALID_CREDENTIALS.value,
            error=str(e),
        )


@router.patch(
    "/user",
    tags=[tag],
    response_model=UserRead,
    responses={
        202: {"model": UserRead},
        400: {"model": AppErrorModel},
        500: {"model": AppErrorModel},
    },
)
def update_user_api(
    user: UserUpdate,
    jwt_token: UserLogin = Depends(get_basic_auth_credentials),
):
    """
    Update user details.
    """
    try:
        user_db = UserService().get_user(user_email=jwt_token.email)
        response = UserService().update_user(
            user_id=user_db.id,
            user_data=user,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": UserResponseMessages.USER_UPDATED.value,
                "data": response.model_dump(),
            },
        )
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=UserResponseMessages.USER_UPDATE_FAILED.value,
            error=str(e),
        )
