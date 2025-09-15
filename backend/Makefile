.PHONY: help install dev test lint clean docker-up docker-down migrate seed

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install Python dependencies
	pip install -r requirements.txt

dev: ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest-watch -- --cov=app --cov-report=term-missing

lint: ## Run linting
	flake8 app/
	black --check app/
	isort --check-only app/

format: ## Format code
	black app/
	isort app/

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/
	rm -rf .pytest_cache/

docker-up: ## Start all Docker services
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-build: ## Build Docker images
	docker-compose build

## Removed Alembic-based migration commands (PostgreSQL dropped)
## migrate: ## Run database migrations
## 	alembic upgrade head

## migrate-create: ## Create new migration
## 	@read -p "Enter migration message: " message; \\
## 	alembic revision --autogenerate -m "$$message"

## migrate-rollback: ## Rollback last migration
## 	alembic downgrade -1

seed: ## Seed database with initial data
	python -m app.utils.seed_data

shell: ## Start Python shell
	python -c "from app.main import app; from app.core.database import SessionLocal; db = SessionLocal(); print('Database session ready: db')"

health: ## Check application health
	curl -f http://localhost:8000/health || echo "Application not healthy"

api-docs: ## Open API documentation
	open http://localhost:8000/docs

neo4j-browser: ## Open Neo4j browser
	open http://localhost:7474

redis-cli: ## Connect to Redis CLI
	docker-compose exec redis redis-cli

## db-connect: ## Connect to PostgreSQL database
## 	docker-compose exec db psql -U flawfinder -d flawfinder_db

setup: ## Complete setup for development
	@echo "Setting up FlawFinder AI backend..."
	make install
	make docker-up
	@echo "Waiting for services to start..."
	sleep 10
	@echo "Neo4j-only setup complete! Access the API at http://localhost:8000"

reset: ## Reset everything and start fresh
	make docker-down
	docker volume prune -f
	make setup

production: ## Production deployment
	docker-compose -f docker-compose.prod.yml up -d