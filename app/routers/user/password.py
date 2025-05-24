from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

# Tags & Models
from app.models.app_error import AppErrorResponseModel
from app.models.generic_response import GenericResponseModel
from app.models.tags import UserverseApiTag
from app.models.user.user import UserLogin
from app.models.user.password import PasswordResetRequest, OTPValidationRequest

# Auth & Logic
from app.security.basic_auth import get_basic_auth_credentials
from app.logic.user.password import UserPasswordService

# Error Handling
from app.utils.app_error import AppError

router = APIRouter()
tag = UserverseApiTag.USER_PASSWORD_MANAGEMENT.name


@router.patch(
    "/password-reset/request",
    tags=[tag],
    responses={
        202: {"model": GenericResponseModel},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def password_reset_request_api(
    input: PasswordResetRequest,
):
    """
    Trigger a password reset request.

    - **Sends**: OTP code to user's email
    - **Returns**: Success message
    """
    try:
        response = UserPasswordService().request_password_reset(input.email)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=response.model_dump(),
        )
    except (AppError, Exception) as e:
        raise e


@router.patch(
    "/password-reset/validate-otp",
    tags=[tag],
    responses={
        202: {"model": GenericResponseModel},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def password_reset_validate_otp_api(
    input: OTPValidationRequest,
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    """
    Validate OTP and reset password.

    - **Requires**: Basic Auth (email as username, new password as password)
    - **Also requires**: OTP provided in request body
    - **Returns**: Success message
    """
    try:
        response = UserPasswordService().validate_otp_and_change_password(
            user_email=credentials.email,
            new_password=credentials.password,
            otp=input.otp,
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=response.model_dump(),
        )
    except (AppError, Exception) as e:
        raise e
