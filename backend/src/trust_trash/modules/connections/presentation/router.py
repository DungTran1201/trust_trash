from fastapi import APIRouter

router = APIRouter(prefix="/connections", tags=["connections"])


@router.get("")
async def list_connections() -> dict[str, object]:
    """Placeholder: returns no persisted connections in the starter."""
    return {"items": [], "total": 0, "implementation_status": "placeholder"}
