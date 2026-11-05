"""HTTP interface for analytics; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Add endpoints only when the corresponding use cases exist.
