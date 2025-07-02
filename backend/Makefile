# Mattilda Docker Operations Makefile

.PHONY: help build up down logs clean test dev prod restart local

# Default target
help:
	@echo "Available commands:"
	@echo "  make local      - Run application locally (without Docker)"
	@echo "  make dev        - Start development environment (Docker)"
	@echo "  make prod       - Start production environment (Docker)"
	@echo "  make build      - Build Docker images"
	@echo "  make rebuild    - Rebuild Docker images (no cache, for dependency changes)"
	@echo "  make up         - Start services"
	@echo "  make down       - Stop services"
	@echo "  make restart    - Restart services"
	@echo "  make logs       - Show logs"
	@echo "  make clean      - Clean up containers, images, and volumes"
	@echo "  make test       - Run tests in Docker"
	@echo "  make shell      - Open shell in backend container"
	@echo "  make db-shell   - Open PostgreSQL shell"
	@echo "  make pgadmin    - Start pgAdmin (development only)"

# Local development (without Docker)
local:
	@echo "🏠 Starting local development environment..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found. Please check the environment files."; \
		exit 1; \
	fi
	@echo "📋 Using .env.local configuration"
	@echo "🗄️  Make sure PostgreSQL is running locally"
	@echo "🚀 Starting application..."
	ENV_FILE=.env uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
	@echo "✅ Application is running at http://localhost:8000"

# Development environment
dev:
	@echo "🚀 Starting development environment..."
	@echo "🔨 Building Docker images (in case dependencies changed)..."
	cd .. && docker-compose build
	cd .. && docker-compose up -d
	@echo "✅ Development environment is running!"
	@echo "🌐 Backend API: http://localhost:8000"
	@echo "📊 API Docs: http://localhost:8000/docs"
	@echo "🔧 Run 'make logs' to see logs"

# Production environment
prod:
	@echo "🚀 Starting production environment..."
	@if [ ! -f .env.prod ]; then \
		echo "❌ .env.prod file not found. Please configure it for production."; \
		exit 1; \
	fi
	docker compose -f docker compose.prod.yml up -d
	@echo "✅ Production environment is running!"

# Build images
build:
	@echo "🔨 Building Docker images..."
	cd .. && docker-compose build

# Build images without cache (useful when dependencies change)
rebuild:
	@echo "🔨 Rebuilding Docker images (no cache)..."
	cd .. && docker-compose build --no-cache

# Start services
up:
	@echo "⬆️ Starting services..."
	docker compose up -d

# Stop services
down:
	@echo "⬇️ Stopping services..."
	docker compose down

# Restart services
restart:
	@echo "🔄 Restarting services..."
	docker compose restart

# Show logs
logs:
	@echo "📋 Showing logs (Ctrl+C to exit)..."
	docker compose logs -f

# Show backend logs only
logs-backend:
	@echo "📋 Showing backend logs (Ctrl+C to exit)..."
	docker compose logs -f backend

# Show database logs only
logs-db:
	@echo "📋 Showing database logs (Ctrl+C to exit)..."
	docker compose logs -f db

# Clean up everything
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker compose down -v --remove-orphans
	docker system prune -f
	docker volume prune -f
	@echo "✅ Cleanup completed!"

# Run tests in Docker
test:
	@echo "🧪 Running tests in Docker..."
	docker compose exec backend python run_tests.py domain --verbose

# Open shell in backend container
shell:
	@echo "🐚 Opening shell in backend container..."
	docker compose exec backend bash

# Open PostgreSQL shell
db-shell:
	@echo "🐘 Opening PostgreSQL shell..."
	docker compose exec db psql -U mattilda_user -d mattilda_db

# Start pgAdmin for database management
pgadmin:
	@echo "🔧 Starting pgAdmin..."
	docker compose --profile tools up -d pgadmin
	@echo "✅ pgAdmin is running at http://localhost:5050"
	@echo "📧 Email: admin@mattilda.com"
	@echo "🔑 Password: admin123"

# Check service status
status:
	@echo "📊 Service Status:"
	docker compose ps

# View resource usage
stats:
	@echo "📈 Resource Usage:"
	docker stats

# Backup database
backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker compose exec -T db pg_dump -U mattilda_user mattilda_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

# Restore database (usage: make restore BACKUP_FILE=backups/backup_20240101_120000.sql)
restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify BACKUP_FILE. Example: make restore BACKUP_FILE=backups/backup_20240101_120000.sql"; \
		exit 1; \
	fi
	@echo "📥 Restoring database from $(BACKUP_FILE)..."
	docker compose exec -T db psql -U mattilda_user -d mattilda_db < $(BACKUP_FILE)
	@echo "✅ Database restored!"

# Update dependencies
update-deps:
	@echo "📦 Updating dependencies..."
	docker compose exec backend pip install --upgrade pip
	docker compose exec backend pip list --outdated

# Run linting
lint:
	@echo "🔍 Running linting..."
	docker compose exec backend python -m flake8 app/
	docker compose exec backend python -m black --check app/

# Format code
format:
	@echo "✨ Formatting code..."
	docker compose exec backend python -m black app/
	docker compose exec backend python -m isort app/
