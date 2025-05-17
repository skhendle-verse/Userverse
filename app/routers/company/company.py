from fastapi import APIRouter, Depends, status, Query, Path
from fastapi.responses import JSONResponse

# Models
from app.models.company.roles import CompanyDefaultRoles
from app.models.generic_pagination import PaginatedResponse
from app.models.generic_response import GenericResponseModel
from app.models.company.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.models.app_error import AppErrorResponseModel
from app.models.company.response_messages import CompanyResponseMessages

# Auth
from app.security.jwt import get_current_user_from_jwt_token
from app.models.user.user import UserQueryParams, UserRead

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
        raise e


@router.get(
    "/company",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": GenericResponseModel[CompanyRead]},
        400: {"model": AppErrorResponseModel},
        404: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def get_company_api(
    email: str = Query(None, description="(Optional) Lookup company by email"),
    company_id: int = Query(None, description="(Optional) Lookup company by ID"),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Retrieve a company by email or company_id.
    Priority: email > company_id.
    """
    try:
        if email:
            company = CompanyService().get_company(user=user, email=email)
        elif company_id:
            company = CompanyService().get_company(user=user, company_id=company_id)
        else:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_ID_OR_EMAIL_REQUIRED.value,
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=GenericResponseModel(
                message=CompanyResponseMessages.COMPANY_FOUND.value,
                data=company.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.patch(
    "/company/{company_id}",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        201: {"model": GenericResponseModel[CompanyRead]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def update_user_api(
    company_updates: CompanyUpdate,
    company_id: int = Path(..., description="Company ID to update"),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Update a company by its ID.
    Requires the user to be an administrator of the company.
    """
    try:
        response = CompanyService().update_company(
            payload=company_updates,
            company_id=company_id,
            user=user,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=GenericResponseModel(
                message=CompanyResponseMessages.COMPANY_UPDATED.value,
                data=response.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    "/company/{company_id}/users",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": GenericResponseModel[PaginatedResponse[UserRead]]},
        400: {"model": AppErrorResponseModel},
        404: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def get_company_users_api(
    company_id: int,
    params: UserQueryParams = Depends(),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Retrieve a company by email or company_id.
    Priority: email > company_id.
    """
    try:
        company_service = CompanyService()
        response = company_service.get_company_user(
            company_id=company_id,
            params=params,
            user=user,
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=GenericResponseModel(
                message=CompanyResponseMessages.GET_COMPANY_USERS.value,
                data=response.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e
