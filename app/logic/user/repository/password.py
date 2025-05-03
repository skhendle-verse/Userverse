from fastapi import status
from datetime import datetime, timedelta, timezone

# utils
from app.utils.app_error import AppError

# database
from app.database import DatabaseSessionManager
from app.database.user import User

# models
from app.models.user.user import UserRead
from app.models.user.messages import UserResponseMessages

class UserPasswordRepository:
    """
    This class handles user password management, including updating,
    verifying, resetting, and changing passwords.
    """

    def __init__(self):
        self.db_manager = DatabaseSessionManager()

    def update_password_reset_token(self, user_email: str, token: str) -> None:
        """
        Update the password reset token for a user.
        """
        with self.db_manager.session_object() as session:
            user = session.query(User).filter(User.email == user_email).first()
            if not user:
                raise AppError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message=UserResponseMessages.USER_NOT_FOUND.value,
                )
            
            user.update_json_field(
                session=session,
                record_id=user.id,
                column_name="primary_meta_data",
                key="password_reset",
                value={
                    "password_reset_token": token,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
                
            )
            session.commit()