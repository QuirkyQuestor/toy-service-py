.PHONY: run run-dev

run-dev:
	uv run fastapi dev src/toy_service_py/app.py

run:
	uv run toy-service-py