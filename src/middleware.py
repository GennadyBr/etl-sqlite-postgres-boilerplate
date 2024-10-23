from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.core.colored_formatter import replace_formatter_4_all_loggers
from src.core.logger import logger


async def logger_request_info(request: Request) -> None:
    """Logger request info"""
    logger.info(f'Request method: {request.method=}')
    logger.info(f'Request url: {request.url=}')


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware"""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Dispatch"""
        # Replace root_formatter with colored_formatter
        replace_formatter_4_all_loggers()

        logger.info('Logging middleware')
        await logger_request_info(request)
        response = await call_next(request)
        logger.info(f'Response: {response.status_code}')
        return response
