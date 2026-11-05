from fastapi import FastAPI

from trust_trash.bootstrap.module_registry import register_module_routers
from trust_trash.shared.infrastructure.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Modular API starter for the Trust Trash platform.",
    )
    register_module_routers(app, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {"name": settings.app_name, "status": "starter"}

    return app


app = create_app()
