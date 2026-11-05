"""HTTP interface for connector_registry; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/connector-registry", tags=["connector registry"])

# Add endpoints only when the corresponding use cases exist.
