# Toy Service (Python)

Items API in Python: FastAPI, async psycopg 3 with a connection pool, pydantic-settings.
Twin of the Go version: [toy-service](https://github.com/QuirkyQuestor/toy-service). Same API contract and schema.

## Run

```
docker compose up -d
docker compose exec -T db psql -U postgres -d toy_service < migration/001-ItemsTable.sql
export DATABASE_URL=postgres://postgres:password@localhost:5432/toy_service
make run        # or: make run-dev (auto-reload)
```

## Test

```
curl -i http://localhost:8000/healthz
curl -i http://localhost:8000/readyz    # 503 when Postgres is down
```

## Status

Working: health and readiness probes (readiness checks Postgres via the pool), items list and get by id.<br>
Next: items create, update, delete, tests, graceful shutdown.
