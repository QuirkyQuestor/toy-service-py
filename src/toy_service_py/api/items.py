from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
async def list_items():
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"detail": "This endpoint is not yet implemented"},
    )
