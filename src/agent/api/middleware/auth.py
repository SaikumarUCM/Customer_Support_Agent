"""API key / Bearer token authentication middleware."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from agent.core.config import get_settings
from agent.core.logging import get_logger

log = get_logger(__name__)

_SKIP_PATHS = {"/health", "/ready", "/docs", "/openapi.json", "/redoc"}


class AuthMiddleware(BaseHTTPMiddleware):
    """Require a valid API key on all routes except health/docs."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in _SKIP_PATHS:
            return await call_next(request)

        settings = get_settings()
        token: str | None = None

        # Accept X-API-Key header or Authorization: Bearer <token>
        api_key_header = request.headers.get("X-API-Key")
        auth_header = request.headers.get("Authorization", "")

        if api_key_header:
            token = api_key_header
        elif auth_header.startswith("Bearer "):
            token = auth_header[7:]

        if not token or token != settings.api_key:
            log.warning(
                "auth: rejected request",
                path=request.url.path,
                ip=request.client.host if request.client else "unknown",
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or missing API key"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await call_next(request)
