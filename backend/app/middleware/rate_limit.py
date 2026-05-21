"""
middleware/rate_limit.py
Simple sliding-window in-memory rate limiter.
For production: replace store with Redis via slowapi.
"""
import time
import logging
from collections import defaultdict, deque
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

_store: dict[tuple, deque] = defaultdict(deque)

LIMITS = {
    "/api/v1/jobs":     (5,   60),
    "/api/v1/articles": (60,  60),
    "/api/v1/admin":    (30,  60),
    "default":          (120, 60),
}


def _get_limit(path: str) -> tuple[int, int]:
    for prefix, lim in LIMITS.items():
        if prefix != "default" and path.startswith(prefix):
            return lim
    return LIMITS["default"]


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in {"/", "/docs", "/openapi.json", "/api/v1/health"}:
            return await call_next(request)

        ip  = request.client.host if request.client else "unknown"
        max_req, window = _get_limit(request.url.path)
        key = (ip, request.url.path[:30])
        now = time.time()
        ts  = _store[key]
        while ts and ts[0] < now - window:
            ts.popleft()
        if len(ts) >= max_req:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded", "retry_after": window},
                headers={"Retry-After": str(window)},
            )
        ts.append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"]     = str(max_req)
        response.headers["X-RateLimit-Remaining"] = str(max_req - len(ts))
        return response