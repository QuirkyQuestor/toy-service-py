from typing import Annotated

from fastapi import Depends, Request
from psycopg_pool import AsyncConnectionPool

from .config import settings

pool = AsyncConnectionPool(
    settings.database_url.encoded_string(),
    open=False,
    check=AsyncConnectionPool.check_connection,
)


def get_pool(request: Request) -> AsyncConnectionPool:
    return request.app.state.pool


PoolDep = Annotated[AsyncConnectionPool, Depends(get_pool)]
