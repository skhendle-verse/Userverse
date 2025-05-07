# href: https://www.sheshbabu.com/posts/fastapi-structured-json-logging/

from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.config_logging import logger

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": { "method": request.method, "url": str(request.url) },
                "res": { "status_code": response.status_code, },
            },
        )
        return response