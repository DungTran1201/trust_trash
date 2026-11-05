"""HTTP interface for identity; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/identity", tags=["identity"])

# Add endpoints only when the corresponding use cases exist.
