from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.core.colored_formatter import replace_formatter_4_all_loggers
from src.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware"""

    async def dispatch(
        self, request: Request, call_next: Callable,
    ) -> Response:
        """Dispatch"""
        # Replace root_formatter with colored_formatter
        replace_formatter_4_all_loggers()

        logger.info('Logging middleware')
        logger.info(f'Request: {request.method} {request.url}')
        response = await call_next(request)
        logger.info(f'Response: {response.status_code}')
        return response
