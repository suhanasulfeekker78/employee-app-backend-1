
from fastapi.middleware.cors import CORSMiddleware
from middleware.logger import RequestLoggingMiddleware

from fastapi import FastAPI
def configure_middleware(app: FastAPI) -> None:
    """
    Register ASGI middleware. Last added is outermost (runs first on the request path).

    Stack (request): CORS -> request logging -> process time -> routes.
    """
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time"],
    )