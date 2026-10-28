from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import health, items
from .db import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open(wait=True, timeout=5)
    app.state.pool = pool
    yield
    await pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(items.router)
