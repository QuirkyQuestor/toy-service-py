from toy_service_py.app import app
from toy_service_py.db import get_pool

from .fakepool import FakePool


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_readyz(client):
    app.dependency_overrides[get_pool] = lambda: FakePool()
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_db_down(client):
    app.dependency_overrides[get_pool] = lambda: FakePool(fail=True)
    response = client.get("/readyz")
    assert response.status_code == 503
    assert response.json() == {"error": "db unavailable"}
