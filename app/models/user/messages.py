from enum import Enum


class UserResponseMessages(str, Enum):
    USER_CREATED = "User created successfully"
    USER_CREATION_FAILED = "User creation failed"
    USER_ALREADY_EXISTS = "User already exists"

    

    USER_NOT_FOUND = "User not found"
    USER_FOUND = "User found"
    USER_UPDATED = "User updated successfully"
    USER_DELETED = "User deleted successfully"
    USER_LOGGED_IN = "User logged in successfully"
    USER_LOGGED_OUT = "User logged out successfully"
    PASSWORD_RESET = "Password reset successfully"
    EMAIL_VERIFIED = "Email verified successfully"
    INVALID_CREDENTIALS = "Invalid credentials"

    USER_UPDATE_FAILED = "User update failed"
    USER_DELETION_FAILED = "User deletion failed"
    PASSWORD_RESET_FAILED = "Password reset failed"
    EMAIL_VERIFICATION_FAILED = "Email verification failed"
    ACCOUNT_LOCKED = "Account is locked"
    INVALID_REQUEST_MESSAGE = "Invalid request"
