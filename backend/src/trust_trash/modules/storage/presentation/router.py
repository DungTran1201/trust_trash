"""HTTP interface for storage; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/storage", tags=["storage"])

# Add endpoints only when the corresponding use cases exist.
