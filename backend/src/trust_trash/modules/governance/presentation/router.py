"""HTTP interface for governance; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/governance", tags=["governance"])

# Add endpoints only when the corresponding use cases exist.
