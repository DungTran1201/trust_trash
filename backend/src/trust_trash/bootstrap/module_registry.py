from fastapi import FastAPI

from trust_trash.modules.connections.presentation.router import router as connections_router
from trust_trash.modules.discovery.presentation.router import router as discovery_router
from trust_trash.modules.observability.presentation.router import router as observability_router


def register_module_routers(app: FastAPI, prefix: str) -> None:
    """Composition root: register public HTTP interfaces of enabled modules."""
    app.include_router(observability_router, prefix=prefix)
    app.include_router(connections_router, prefix=prefix)
    app.include_router(discovery_router, prefix=prefix)
