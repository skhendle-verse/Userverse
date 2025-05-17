from fastapi import APIRouter, Depends, status, Query, Path
from fastapi.responses import JSONResponse

# Models
from app.models.generic_pagination import PaginatedResponse
from app.models.generic_response import GenericResponseModel
from app.models.company.roles import (
    RoleCreate,
    RoleDelete,
    RoleQueryParams,
    RoleRead,
    RoleUpdate,
    CompanyDefaultRoles,
)
from app.models.app_error import AppErrorResponseModel
from app.models.company.response_messages import CompanyResponseMessages

# Auth
from app.security.jwt import get_current_user_from_jwt_token
from app.models.user.user import UserRead

# Logic
from app.logic.company.company import CompanyService
from app.logic.company.role import RoleService


# Utils
from app.utils.app_error import AppError

router = APIRouter()
tag = "Company Role Management"


@router.post(
    "/company/{company_id}/role",
    tags=[tag],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": GenericResponseModel[RoleRead]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def create_role_api(
    payload: RoleCreate,
    company_id: int = Path(..., description="Company ID to update"),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Register a new role.
    """
    try:
        company_service = CompanyService()
        admin_user = company_service.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company_id,
            role=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )

        if not admin_user:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.ROLE_CREATION_FORBIDDEN.value,
            )
        role_service = RoleService()
        response = role_service.create_role(
            payload=payload,
            created_by=user,
            company_id=company_id,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": CompanyResponseMessages.ROLE_CREATION_SUCCESS.value,
                "data": response.model_dump(),
            },
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.patch(
    "/company/{company_id}/role/{name}",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        201: {"model": GenericResponseModel[RoleRead]},
        400: {"model": AppErrorResponseModel},
        404: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def update_role_api(
    payload: RoleUpdate,
    company_id: int = Path(..., description="Company ID to update"),
    name: str = Path(..., description="Role name to update"),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Update the description of a role by name for a company.
    Requires the user to be an administrator of the company.
    """
    try:
        company_service = CompanyService()
        admin_user = company_service.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company_id,
            role=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )
        if not admin_user:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.ROLE_CREATION_FORBIDDEN.value,
            )
        role_service = RoleService()
        response = role_service.update_role(
            company_id=company_id,
            name=name,
            payload=payload,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": CompanyResponseMessages.ROLE_UPDATED.value,
                "data": response.model_dump(),
            },
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.delete(
    "/company/{company_id}/role",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        201: {"model": GenericResponseModel[dict]},
        400: {"model": AppErrorResponseModel},
        404: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def delete_role_api(
    payload: RoleDelete,
    company_id: int = Path(..., description="Company ID to update"),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Delete a role and reassign all users to a replacement role (same company).
    """
    try:
        company_service = CompanyService()
        admin_user = company_service.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company_id,
            role=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )
        if not admin_user:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.ROLE_CREATION_FORBIDDEN.value,
            )
        response = RoleService.delete_role(
            payload=payload,
            deleted_by=user,
            company_id=company_id,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": CompanyResponseMessages.ROLE_DELETED.value,
                "data": response,
            },
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    "/company/{company_id}/roles",
    tags=[tag],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": GenericResponseModel[PaginatedResponse[RoleRead]]},
        400: {"model": AppErrorResponseModel},
        500: {"model": AppErrorResponseModel},
    },
)
def get_company_roles_api(
    company_id: int,
    query_params: RoleQueryParams = Depends(),
    user: UserRead = Depends(get_current_user_from_jwt_token),
):
    """
    Get paginated roles for a company.
    """
    try:
        company_service = CompanyService()
        admin_user = company_service.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company_id,
            role=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )

        if not admin_user:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.ROLE_CREATION_FORBIDDEN.value,
            )

        response = RoleService.get_company_roles(
            payload=query_params, company_id=company_id
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=GenericResponseModel(
                message=CompanyResponseMessages.ROLE_GET_SUCCESS.value,
                data=response,
            ).model_dump(),
        )
    except AppError as e:
        raise e
    except Exception as e:
        raise e
