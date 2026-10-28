from psycopg_pool import AsyncConnectionPool

from .config import settings

pool = AsyncConnectionPool(
    settings.database_url.encoded_string(),
    open=False,
    check=AsyncConnectionPool.check_connection,
)
