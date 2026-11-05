"""HTTP interface for processing; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/processing", tags=["processing"])

# Add endpoints only when the corresponding use cases exist.
