import os

os.environ.setdefault("DATABASE_URL", "postgresql://test@localhost/test")

import pytest
from fastapi.testclient import TestClient

from toy_service_py.app import app
from toy_service_py.store import get_store

from .fakestore import FakeItemsStore


@pytest.fixture
def client():
    store = FakeItemsStore()
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()
