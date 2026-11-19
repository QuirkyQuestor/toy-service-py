.PHONY: run run-dev postgres-up postgres-down

run-dev:
	uv run fastapi dev src/toy_service_py/app.py

run:
	uv run toy-service-py

postgres-up:
	docker compose up -d

postgres-down:
	docker compose down
