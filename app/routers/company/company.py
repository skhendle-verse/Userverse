from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

# Models
from app.models.generic_response import GenericResponseModel
from app.models.company.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.models.app_error import AppErrorResponseModel
from app.models.company.response_messages import CompanyResponseMessages

# Auth
from app.security.jwt import get_current_user_from_jwt_token
from app.models.user.user import UserRead

# Logic
from app.logic.company.company import CompanyService

# Utils
from app.utils.app_error import AppError

router = APIRouter()
tag = "Company Management"


@router.post(
    "/company",
    tags=[tag],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": GenericResponseModel[CompanyRead]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def create_company_api(
    payload: CompanyCreate,
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Register a new company and store its address in primary_meta_data.
    Also sets up default roles (Administrator, Viewer).
    """
    try:
        response = CompanyService().create_company(payload, created_by=user)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": CompanyResponseMessages.COMPANY_CREATED.value,
                "data": response.model_dump(),
            },
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise AppError.internal(str(e))
