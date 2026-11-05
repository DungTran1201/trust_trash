.PHONY: infra-up infra-down api test lint

infra-up:
	docker compose -f infra/compose/docker-compose.yml up -d postgres

infra-down:
	docker compose -f infra/compose/docker-compose.yml down

api:
	cd backend && uvicorn trust_trash.bootstrap.app:app --reload

test:
	cd backend && pytest

lint:
	cd backend && ruff check src tests
