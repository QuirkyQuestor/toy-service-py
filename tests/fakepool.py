from contextlib import asynccontextmanager

from psycopg import OperationalError


class FakeConn:
    async def execute(self, sql): ...


class FakePool:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    @asynccontextmanager
    async def connection(self):
        if self.fail:
            raise OperationalError("db down")
        yield FakeConn()
