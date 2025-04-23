from enum import Enum

class UserErrorMessages(str, Enum):
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    INVALID_CREDENTIALS = "Invalid credentials"
    USER_CREATION_FAILED = "User creation failed"
    USER_UPDATE_FAILED = "User update failed"
    USER_DELETION_FAILED = "User deletion failed"
    PASSWORD_RESET_FAILED = "Password reset failed"
    EMAIL_VERIFICATION_FAILED = "Email verification failed"
    ACCOUNT_LOCKED = "Account is locked"
    INVALID_REQUEST_MESSAGE = "Invalid request"