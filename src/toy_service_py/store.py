from typing import Annotated, Protocol

from fastapi import Depends
from psycopg.rows import class_row
from psycopg_pool import AsyncConnectionPool

from .db import PoolDep
from .schemas import Item, ItemIn


class ItemsStore(Protocol):
    async def get_one(self, item_id: int) -> Item | None: ...
    async def get_all(self) -> list[Item]: ...
    async def add(self, item_name: str) -> Item: ...
    async def update(self, item_id: int, item: ItemIn) -> Item | None: ...
    async def delete(self, item_id: int) -> bool: ...


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
        async with (
            self._pool.connection() as conn,
            conn.cursor(row_factory=class_row(Item)) as cur,
        ):
            await cur.execute(
                "INSERT INTO items (name) VALUES (%s) RETURNING id, name",
                (item_name,),
            )
            new_row = await cur.fetchone()
            assert new_row is not None
        return new_row

    async def update(self, item_id: int, item: ItemIn) -> Item | None:
        async with (
            self._pool.connection() as conn,
            conn.cursor(row_factory=class_row(Item)) as cur,
        ):
            await cur.execute(
                "UPDATE items SET name = %s WHERE id = %s RETURNING id, name",
                (item.name, item_id),
            )
            updated_row = await cur.fetchone()
        return updated_row

    async def delete(self, item_id: int) -> bool:
        async with (
            self._pool.connection() as conn,
            conn.cursor() as cur,
        ):
            await cur.execute(
                "DELETE FROM items WHERE id = %s",
                (item_id,),
            )
            return cur.rowcount == 1


def get_store(pool: PoolDep) -> ItemsStore:
    return PostgresItemsStore(pool)


StoreDep = Annotated[ItemsStore, Depends(get_store)]
