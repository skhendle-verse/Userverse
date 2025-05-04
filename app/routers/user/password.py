import traceback
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.configs import configs
from app.models.user.user import UserLogin
from app.models.user.password import (
    PasswordResetRequest,
    OTPValidationRequest,
)

from app.security.basic_auth import get_basic_auth_credentials
from app.utils.app_error import AppError
from app.models.user.messages import UserResponseMessages
from app.logic.user.password import UserPasswordService


router = APIRouter()
tag = "User Password Management"


# This should trigger the sending of an email
@router.patch("/user/password-reset/request", tags=[tag], response_model=str)
def password_reset_request_api(
    input: PasswordResetRequest,
):
    try:
        password_reset_response = UserPasswordService().request_password_reset(
            input.email
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=password_reset_response.model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.patch("/user/password-reset/validate-otp", tags=[tag], response_model=str)
def password_reset_validate_otp(
    input: OTPValidationRequest,
    credentials: UserLogin = Depends(get_basic_auth_credentials),
):
    try:
        password_validate_otp_response = UserPasswordService().validate_otp_and_change_password(
            user_email=credentials.email,
            new_password=credentials.password,
            otp=input.otp,
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=password_validate_otp_response.model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


# # This should validate the OTP sent to the email,
# # and return a token for the next step
# @router.patch("/user/password-reset-validate-otp", tags=[tag], response_model=str)
# def password_reset_validate_otp_api(
#     user: OTPValidationRequest,
# ):
#     try:
#         pass
#     except Exception as e:
#         traceback.print_exc()
#         raise AppError(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message=UserResponseMessages.EMAIL_VERIFICATION_FAILED.value,
#             error=str(e),
#         )


# # This should update the password, username is the token from the previous step
# @router.patch("/user/password-reset-confirm", tags=[tag], response_model=str)
# def password_reset_confirm_api(
#     credentials: UserLogin = Depends(get_basic_auth_credentials),
# ):
#     try:
#         update_password = PasswordResetConfirm(
#             token=credentials.username, new_password=credentials.password
#         )
#         pass
#     except Exception as e:
#         traceback.print_exc()
#         raise AppError(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message=UserResponseMessages.PASSWORD_RESET_FAILED.value,
#             error=str(e),
#         )
