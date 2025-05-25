import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from .logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )

        try:
            response = await call_next(request)

            process_time = time.time() - start_time

            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Process Time: {process_time:.3f}s"
            )

            return response

        except Exception as e:
            logger.error(
                f"Error processing request: {request.method} {request.url.path} "
                f"Error: {str(e)}"
            )
            raise
