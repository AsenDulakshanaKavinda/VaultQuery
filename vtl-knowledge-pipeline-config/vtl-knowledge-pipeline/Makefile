.PHONY: help up down logs sync lint format typecheck test test-unit test-security test-integration seed ingest

help:
	@echo "make up|down|logs        - local services (qdrant, postgres, minio, rabbitmq)"
	@echo "make sync                - install deps with uv"
	@echo "make lint|format|typecheck"
	@echo "make test                - unit + contract + security"
	@echo "make test-security       - permission tests only (must always pass)"
	@echo "make test-integration    - needs services up"
	@echo "make seed                - load mock VTL data"
	@echo "make ingest              - run a backfill"

up:
	docker compose up -d --wait

down:
	docker compose down

logs:
	docker compose logs -f

sync:
	uv sync --all-extras

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run mypy

test:
	uv run pytest -m "unit or contract or security"

test-unit:
	uv run pytest -m unit

test-security:
	uv run pytest -m security

test-integration:
	uv run pytest -m integration

seed:
	uv run python scripts/seed_mock_data.py

ingest:
	uv run python -m vtl_pipeline.pipeline.backfill
