.PHONY: help setup install test clean docker-up docker-down backend-test frontend-test

help:
	@echo "AI Allied Health Assessment Automator - Development Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup          - Initial project setup"
	@echo "  make install        - Install all dependencies"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up      - Start all services with Docker"
	@echo "  make docker-down    - Stop all Docker services"
	@echo "  make docker-logs    - View Docker logs"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test           - Run all tests"
	@echo "  make backend-test   - Run backend tests"
	@echo "  make frontend-test  - Run frontend tests"
	@echo ""
	@echo "Development Commands:"
	@echo "  make backend-dev    - Start backend development server"
	@echo "  make frontend-dev   - Start frontend development server"
	@echo "  make celery-dev     - Start Celery worker"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-migrate     - Create new migration"
	@echo "  make db-upgrade     - Apply migrations"
	@echo "  make db-downgrade   - Rollback last migration"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean          - Remove generated files"

setup:
	@echo "Setting up project..."
	cp backend/.env.example backend/.env
	cp frontend/.env.example frontend/.env
	@echo "Please edit backend/.env and frontend/.env with your configuration"
	@echo "Then run 'make install'"

install:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

test: backend-test frontend-test

backend-test:
	cd backend && . venv/bin/activate && pytest -v

frontend-test:
	cd frontend && npm test

backend-dev:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

frontend-dev:
	cd frontend && npm run dev

celery-dev:
	cd backend && . venv/bin/activate && celery -A app.celery_app worker --loglevel=info

db-migrate:
	cd backend && . venv/bin/activate && alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	cd backend && . venv/bin/activate && alembic upgrade head

db-downgrade:
	cd backend && . venv/bin/activate && alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".hypothesis" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
