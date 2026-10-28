import asyncio
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from psycopg import OperationalError
from psycopg_pool import PoolTimeout

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/healthz")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.get("/readyz")
async def ready(request: Request):
    try:
        async with asyncio.timeout(2):
            async with request.app.state.pool.connection() as conn:
                await conn.execute("SELECT 1")
    except (OperationalError, PoolTimeout, TimeoutError) as e:
        logger.warning("readiness check failed: %r", e)
        return JSONResponse(
            content={
                "error": "db unavailable",
            },
            status_code=503,
        )

    return JSONResponse(content={"status": "ok"}, status_code=200)
