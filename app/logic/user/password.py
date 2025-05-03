import string, random
# repository
from app.logic.user.repository.user import UserRepository
from app.logic.user.repository.password import UserPasswordRepository
# UTILS 
from app.utils.app_error import AppError
from app.utils.email.renderer import render_email_template
from app.utils.email.sender import send_email



class UserPasswordService:  
    SEND_OTP_EMAIL_TEMPLATE = "reset_user_password.html"

    @classmethod
    def generate_random_string(cls, length=10):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @classmethod
    def request_password_reset(cls, user_email):
        
        user_repository = UserRepository()
        user = user_repository.get_user_by_email(user_email)
        if not user:
            raise ValueError("User not found")
        token = cls.generate_random_string()

        # Add token to the database 
        # in user primary_meta_data field 
        # for validation later
        user_password_repository = UserPasswordRepository()
        user_password_repository.update_password_reset_token(
            user_email=user.email,
            token=token,
        )

        # send email
        email_template = render_email_template(
            cls.SEND_OTP_EMAIL_TEMPLATE,
            {
                "user_name": user.first_name,
                "otp": token,
            },
        )
        send_email(
            to=user.email,
            subject="Password Reset OTP",
            html_body=email_template,
        )
        return "OTP sent to email"