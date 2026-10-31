import asyncio
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from psycopg import OperationalError
from psycopg_pool import PoolTimeout

from ..db import PoolDep

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/healthz")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.get("/readyz")
async def ready(pool: PoolDep):
    try:
        async with asyncio.timeout(2):
            async with pool.connection() as conn:
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
