"""HTTP interface for resources; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/resources", tags=["resources"])

# Add endpoints only when the corresponding use cases exist.
