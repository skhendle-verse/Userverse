import string, random

# models
from app.logic.mailer import MailService
from app.models.generic_response import GenericResponseModel

# repository
from app.logic.user.repository.user import UserRepository
from app.logic.user.repository.password import UserPasswordRepository

# UTILS
from app.utils.app_error import AppError
from app.utils.email.renderer import render_email_template
from app.utils.email.sender import send_email


class UserPasswordService:
    SEND_OTP_EMAIL_TEMPLATE = "reset_user_password.html"
    OTP_EMAIL_SUBJECT = "Password Reset OTP"

    @classmethod
    def generate_random_string(cls, length=10):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @classmethod
    def request_password_reset(cls, user_email: str) -> GenericResponseModel:
        """
        Request a password reset by sending an OTP to the user's email.
        """
        # check if user exists
        user_repository = UserRepository()
        user = user_repository.get_user_by_email(user_email)
        if not user:
            raise ValueError("User not found")
        # reset token
        token = cls.generate_random_string(length=6)
        # populate the token in the database for the user
        user_password_repository = UserPasswordRepository()
        user_password_repository.update_password_reset_token(
            user_email=user.email,
            token=token,
        )
        # send email
        MailService.send_template_email(
            to=user.email,
            subject=cls.OTP_EMAIL_SUBJECT,
            template_name=cls.SEND_OTP_EMAIL_TEMPLATE,
            context={
                "user_name": user.first_name + " " + user.last_name,
                "otp": token,
            },
        )

        return GenericResponseModel(
            message="OTP sent to email",
            data=None,
        )

    @classmethod
    def validate_otp_and_change_password(
        cls, user_email: str, otp: str, new_password
    ) -> GenericResponseModel:
        """
        Validate the OTP sent to the user's email. Ensure that the OTP is valid and not expired.
        Return token for the next step(Change Password).
        """
        # check if user exists
        user_repository = UserRepository()
        user = user_repository.get_user_by_email(user_email)
        if not user:
            raise ValueError("User not found")

        # populate the token in the database for the user
        user_password_repository = UserPasswordRepository()
        if user_password_repository.verify_password_reset_token(
            user_email=user.email,
            token=otp,
        ):
            # OTP is valid, proceed to change password
            user_password_repository.update_password(
                user_email=user.email,
                new_password=new_password,
            )
            return GenericResponseModel(
                message="Password changed successfully",
                data=None,
            )

        raise AppError(
            status_code=400,
            message="Invalid OTP",
            error="Invalid OTP, does not match or expired",
        )
