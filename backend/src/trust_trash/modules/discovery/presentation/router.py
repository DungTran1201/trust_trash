from fastapi import APIRouter, HTTPException, status

from trust_trash.shared.contracts.search import SearchRequest

router = APIRouter(prefix="/search", tags=["discovery"])


@router.post("")
async def search(request: SearchRequest) -> dict[str, str]:
    """Placeholder only; no connector fan-out or index search is implemented yet."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Universal Search is not implemented in this starter. "
            f"Received query: {request.query!r}"
        ),
    )
