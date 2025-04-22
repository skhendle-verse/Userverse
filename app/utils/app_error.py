from fastapi import status
from fastapi.exceptions import HTTPException
import inspect
import traceback
import logging
from typing import Optional

# Configure your logger to output to console
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class AppError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: Optional[str] = "Request failed, please try again.",
        error: Optional[str] = None,
        log_error: bool = True,
        depth: int = 2,
    ):
        # Capture the caller's details
        caller_details = self.get_caller_details(depth)
        # Prepare the error detail
        detail = {
            "message": message,
            "error": error or f"An error occurred, {caller_details}",
        }

        # Log the error if needed
        if log_error:
            logging.error(
                f"AppError: {message} | Details: {error} | Location: {caller_details}"
            )
            # self.log_exception()

        super().__init__(status_code, detail=detail)

    @staticmethod
    def get_caller_details(depth):
        frame = inspect.currentframe()
        for _ in range(depth):
            frame = frame.f_back if frame else None

        caller_details = {
            "file": frame.f_code.co_filename if frame else "",
            "line": frame.f_lineno if frame else "",
            "function": frame.f_code.co_name if frame else "",
        }
        return caller_details

    def log_exception(self):
        # This method could be extended to integrate with external monitoring tools
        tb = traceback.format_exc()
        logging.error(f"StackTrace: {tb}")
