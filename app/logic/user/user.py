from fastapi import status

# utils
from app.security.jwt import JWTManager
from app.utils.app_error import AppError

# repository
from app.logic.user.repository.user import UserRepository

# models
from app.models.user.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserLogin,
    TokenResponseModel,
)
from app.models.user.response_messages import UserResponseMessages


class UserService:

    @staticmethod
    def user_login(user_credentials: UserLogin) -> TokenResponseModel:
        user_repository = UserRepository()
        user = user_repository.get_user_by_email(
            user_credentials.email, user_credentials.password
        )
        if not user:
            raise AppError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=UserResponseMessages.INVALID_CREDENTIALS.value,
            )
        return JWTManager().sign_jwt(user)

    @staticmethod
    def get_user(user_id: int = None, user_email: str = None) -> UserRead:
        user_repository = UserRepository()
        if user_id:
            return user_repository.get_user_by_id(user_id)
        elif user_email:
            return user_repository.get_user_by_email(user_email)
        else:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=UserResponseMessages.USER_NOT_FOUND.value,
            )

    @staticmethod
    def create_user(user_credentials: UserLogin, user_data: UserCreate) -> UserRead:
        user_repository = UserRepository()
        data = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_credentials.email,
            "phone_number": user_data.phone_number,
            "password": user_credentials.password,
        }
        return user_repository.create_user(data)

    @classmethod
    def update_user(cls, user_id, user_data: UserUpdate):
        data = {}
        if user_data.first_name:
            data["first_name"] = user_data.first_name
        if user_data.last_name:
            data["last_name"] = user_data.last_name
        if user_data.phone_number:
            data["phone_number"] = user_data.phone_number
        if user_data.password:
            data["password"] = user_data.password

        if not data:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=UserResponseMessages.INVALID_REQUEST_MESSAGE.value,
            )
        user_repository = UserRepository()
        return user_repository.update_user(user_id, data)
