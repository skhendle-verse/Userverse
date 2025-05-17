from enum import Enum


class CompanyResponseMessages(str, Enum):
    # company creation
    COMPANY_CREATED = "Company created successfully"
    COMPANY_CREATION_FAILED = "Company creation failed"
    COMPANY_ALREADY_EXISTS = "Company already exists"
    # company get
    COMPANY_NOT_FOUND = "Company not found"
    COMPANY_FOUND = "Company found"
    UNAUTHORIZED_COMPANY_ACCESS = "Unauthorized access to company"
    COMPANY_ID_OR_EMAIL_REQUIRED = "Either company_id or email is required"
    # company update
    COMPANY_UPDATED = "Company updated successfully"
    COMPANY_UPDATE_FAILED = "Company update failed"
    # company delete
    COMPANY_DELETED = "Company deleted successfully"
    COMPANY_DELETION_FAILED = "Company deletion failed"
    # Role creation
    ROLE_CREATION_SUCCESS = "Role created successfully"
    ROLE_CREATION_FORBIDDEN = "Role creation is forbidden"
    ROLE_CREATION_FAILED = "Role creation failed"
    ROLE_GET_SUCCESS = "Roles retrieved successfully"
    ROLE_NOT_FOUND = "Role not found"
    ROLE_DELETION_FAILED = "Role deletion failed"
    ROLE_DELETED = "Role deleted successfully"
    ROLE_UPDATED = "Role updated successfully"
    ROLE_UPDATE_FAILED = "Role update failed"
    ROLE_ALREADY_EXISTS = "Role already exists"
