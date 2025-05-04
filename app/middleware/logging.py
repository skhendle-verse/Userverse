import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.configs import ConfigLoader

class LogRouteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())

        # Add context to log records
        logger = logging.getLogger()
        old_factory = logger.makeRecord

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.request_id = request_id
            return record

        logger.makeRecord = record_factory
        configs = ConfigLoader().get_config()
        app_name = configs.get("app_name", "userverse")
        version = configs.get("version", "1.0.0")

        # Log request
        logging.info(
            f"Request started",
            extra={
                "app_name": app_name,
                "version": version,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
                "request_id": request_id
            }
        )

        response = await call_next(request)

        # Log response
        logging.info(
            f"Request completed",
            extra={
                "status_code": response.status_code,
                "request_id": request_id
            }
        )

        # Restore original record factory
        logger.makeRecord = old_factory

        return response