from fastapi import APIRouter, Depends, status, Query, Path
from fastapi.responses import JSONResponse

# Models
from app.models.company.user import CompanyUserAdd, CompanyUserRead, CompanyUserRead
from app.models.generic_pagination import PaginatedResponse
from app.models.generic_response import GenericResponseModel
from app.models.company.company import CompanyRead
from app.models.app_error import AppErrorResponseModel
from app.models.company.response_messages import CompanyUserResponseMessages

# Auth
from app.security.jwt import get_current_user_from_jwt_token
from app.models.user.user import UserQueryParams, UserRead

# Logic
from app.logic.company.user import CompanyUserService

# Utils
from app.utils.app_error import AppError

router = APIRouter()
tag = "Company User Management"


@router.get(
    "/company/{company_id}/users",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": GenericResponseModel[PaginatedResponse[CompanyUserRead]]},
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
    Retrieve company users.
    """
    try:
        company_service = CompanyUserService()
        response = company_service.get_company_user(
            company_id=company_id,
            params=params,
            user=user,
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=GenericResponseModel(
                message=CompanyUserResponseMessages.GET_COMPANY_USERS.value,
                data=response.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.post(
    "/company/{company_id}/users",
    tags=[tag],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": GenericResponseModel[PaginatedResponse[CompanyRead]]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def add_user_to_company_api(
    company_id: int,
    payload: CompanyUserAdd,
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Register a user to a company with a role available within in the company.
    """
    try:
        response = CompanyUserService().add_user_to_company(
            company_id=company_id, payload=payload, added_by=user
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=GenericResponseModel(
                message=CompanyUserResponseMessages.ADD_USER_SUCCESS.value,
                data=response.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.delete(
    "/company/{company_id}/user/{user_id}",
    tags=[tag],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": GenericResponseModel[CompanyUserRead]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def delete_user_from_company_api(
    company_id: int,
    user_id: int,
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Remove a user from a company.
    """
    try:
        response = CompanyUserService().remove_user_from_company(
            company_id=company_id, user_id=user_id, removed_by=user
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=GenericResponseModel(
                message=CompanyUserResponseMessages.REMOVE_USER_SUCCESS.value,
                data=response.model_dump(),
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e
