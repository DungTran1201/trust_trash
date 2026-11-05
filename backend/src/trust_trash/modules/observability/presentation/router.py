from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["observability"])


@router.get("")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "trust-trash-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
