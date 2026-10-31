from typing import Annotated, Protocol

from fastapi import Depends
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from .db import PoolDep
from .schemas import Item


class ItemsStore(Protocol):
    async def get_one(self, item_id: int) -> Item | None: ...
    async def get_all(self) -> list[Item]: ...
    async def add(self, item_name: str) -> Item: ...
    async def update(self, item: Item) -> Item: ...


class PostgresItemsStore:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self._pool = pool

    async def get_one(self, item_id: int) -> Item | None:
        async with (
            self._pool.connection() as conn,
            conn.cursor(row_factory=class_row(Item)) as cur,
        ):
            await cur.execute("SELECT id, name FROM items WHERE id = %s", (item_id,))
            row = await cur.fetchone()
        return row

    async def get_all(self) -> list[Item]:
        async with (
            self._pool.connection() as conn,
            conn.cursor(row_factory=class_row(Item)) as cur,
        ):
            await cur.execute("SELECT id, name FROM items ORDER BY id")
            rows = await cur.fetchall()
        return rows

    async def add(self, item_name: str) -> Item:
        raise NotImplementedError

    async def update(self, item: Item) -> Item:
        raise NotImplementedError


def get_store(pool: PoolDep) -> ItemsStore:
    return PostgresItemsStore(pool)


StoreDep = Annotated[ItemsStore, Depends(get_store)]
