import traceback
from fastapi import APIRouter, Depends, status
from app.configs import configs
from app.database import DatabaseSessionManager
from app.utils.app_error import AppError

router = APIRouter()
tag = "Reset Password"


# b TODO: add the correct import for the CompanySecurityModel
@router.get("/company", tags=[tag])
def get_company_api(
    company: CompanySecurityModel = Depends(authenticate_company),
    user: dict = Depends(get_current_user),
):
    try:
        pass
    except Exception as e:
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=invalid_request_message,
            error=str(e),
        )


@router.patch("/company", tags=[tag])
def update_company_api(
    company: CompanySecurityModel = Depends(authenticate_company),
    user: dict = Depends(get_current_user),
):
    try:
        pass
    except Exception as e:
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=invalid_request_message,
            error=str(e),
        )


@router.delete("/company", tags=[tag])
def delete_company_api(
    company: CompanySecurityModel = Depends(authenticate_company),
    user: dict = Depends(get_current_user),
):
    try:
        pass
    except Exception as e:
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=invalid_request_message,
            error=str(e),
        )
