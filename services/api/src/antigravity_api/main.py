from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from antigravity_api.infrastructure.settings import get_settings
from antigravity_api.presentation.http.health_router import router as health_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AntiGravity API",
        version=settings.version,
        description="Agent orchestration API for the AntiGravity autonomous company builder.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix="/v1")

    return app
