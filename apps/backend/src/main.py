"""FastAPI application factory."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.upload import router as upload_router

_DEFAULT_ALLOW_ORIGINS = "http://localhost:5173"


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    CORS origins are resolved from the ``ALLOW_ORIGINS`` environment variable
    at creation time so the module can be imported in tests without requiring
    all secrets to be present (those are injected via dependency overrides).
    """
    allow_origins = os.getenv("ALLOW_ORIGINS", _DEFAULT_ALLOW_ORIGINS).split(",")

    app = FastAPI(
        title="File Upload API",
        description="Streams uploaded files to Azure Blob Storage.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=False,
        allow_methods=["POST"],
        allow_headers=["*"],
    )

    app.include_router(upload_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        """Liveness probe."""
        return {"status": "ok"}

    return app


app = create_app()
