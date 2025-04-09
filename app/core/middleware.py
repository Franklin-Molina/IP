from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar la cantidad de peticiones por IP.
    """
    def __init__(self, app, max_requests: int = 20, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        window = self.clients.get(ip, [])
        # Eliminar timestamps fuera de la ventana
        window = [t for t in window if now - t < self.window_seconds]
        if len(window) >= self.max_requests:
            return JSONResponse(
                {"detail": "Demasiadas peticiones, intenta más tarde."},
                status_code=429
            )
        window.append(now)
        self.clients[ip] = window
        response = await call_next(request)
        return response
