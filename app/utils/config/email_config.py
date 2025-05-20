from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.utils.config.loader import ConfigLoader
from app.utils.logging import logger


class EmailSettings(BaseModel):
    host: str = Field(..., alias="HOST")
    port: int = Field(..., alias="PORT")
    username: EmailStr = Field(..., alias="USERNAME")
    password: str = Field(..., alias="PASSWORD")


class EmailConfig:
    REQUIRED_FIELDS = ["HOST", "PORT", "USERNAME", "PASSWORD"]

    @classmethod
    def load(cls) -> Optional[EmailSettings]:
        config_data = ConfigLoader().get_config()
        environment = config_data.get("environment")

        if environment == "test_environment":
            logger.warning("Skipping email config in test environment.")
            return None

        email_raw = config_data.get("email", {})
        if not email_raw:
            logger.warning("Email configuration section is missing.")
            return None

        missing = [field for field in cls.REQUIRED_FIELDS if not email_raw.get(field)]
        if missing:
            logger.warning(f"Missing email config fields: {missing}")
            return None

        try:
            return EmailSettings(**email_raw)
        except Exception as e:
            logger.error("Invalid email configuration: %s", e)
            raise
