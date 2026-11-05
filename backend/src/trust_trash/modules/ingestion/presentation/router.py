"""HTTP interface for ingestion; keep route handlers thin."""

from fastapi import APIRouter

router = APIRouter(prefix="/ingestion", tags=["ingestion"])

# Add endpoints only when the corresponding use cases exist.
