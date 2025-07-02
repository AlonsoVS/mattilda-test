# Mattilda School Management System - Development Makefile
# This Makefile provides convenient commands for managing the full-stack development environment

.PHONY: help start stop restart status logs clean build test shell format lint backup install-deps
.DEFAULT_GOAL := help

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Mattilda School Management System - Development Commands$(NC)"
	@echo "$(YELLOW)============================================================$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# 🚀 ENVIRONMENT MANAGEMENT
start: ## Start the full development environment (database, backend, frontend)
	@echo "$(GREEN)🚀 Starting Mattilda development environment...$(NC)"
	@if ! docker info >/dev/null 2>&1; then \
		echo "$(RED)❌ Docker is not running. Please start Docker first.$(NC)"; \
		exit 1; \
	fi
	@./start-dev.sh

stop: ## Stop all services
	@echo "$(YELLOW)🛑 Stopping all services...$(NC)"
	@docker-compose down

restart: ## Restart all services
	@echo "$(YELLOW)🔄 Restarting all services...$(NC)"
	@docker-compose down
	@docker-compose up -d
	@echo "$(GREEN)✅ All services restarted!$(NC)"

status: ## Show status of all services
	@echo "$(GREEN)📊 Service Status:$(NC)"
	@docker-compose ps

# 📋 LOGS AND MONITORING
logs: ## Show logs for all services (use Ctrl+C to exit)
	@echo "$(GREEN)📋 Showing all logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f

logs-backend: ## Show backend logs only
	@echo "$(GREEN)📋 Showing backend logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f backend

logs-frontend: ## Show frontend logs only
	@echo "$(GREEN)📋 Showing frontend logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f frontend

logs-db: ## Show database logs only
	@echo "$(GREEN)📋 Showing database logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f db

# 🔨 BUILD AND DEVELOPMENT
build: ## Build all Docker images
	@echo "$(GREEN)🔨 Building Docker images...$(NC)"
	@docker-compose build

rebuild: ## Rebuild all Docker images without cache
	@echo "$(GREEN)🔨 Rebuilding Docker images (no cache)...$(NC)"
	@docker-compose build --no-cache

clean: ## Clean up containers, images, and volumes
	@echo "$(YELLOW)🧹 Cleaning up Docker resources...$(NC)"
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@docker volume prune -f
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

reset: ## Full reset - clean everything and restart fresh
	@echo "$(RED)🔥 Full reset - this will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo ""; \
		make clean; \
		make start; \
	else \
		echo ""; \
		echo "$(YELLOW)Reset cancelled.$(NC)"; \
	fi

# 🧪 TESTING
test: ## Run backend tests
	@echo "$(GREEN)🧪 Running backend tests...$(NC)"
	@docker-compose exec backend python run_tests.py

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)🧪 Running tests with coverage...$(NC)"
	@docker-compose exec backend python -m pytest --cov=app --cov-report=html tests/

# 🐚 SHELL ACCESS
shell: ## Open shell in backend container
	@echo "$(GREEN)🐚 Opening shell in backend container...$(NC)"
	@docker-compose exec backend bash

shell-frontend: ## Open shell in frontend container
	@echo "$(GREEN)🐚 Opening shell in frontend container...$(NC)"
	@docker-compose exec frontend sh

shell-db: ## Open PostgreSQL shell
	@echo "$(GREEN)🐘 Opening PostgreSQL shell...$(NC)"
	@docker-compose exec db psql -U postgres -d mattilda_db

# 💾 DATABASE OPERATIONS
backup: ## Create database backup
	@echo "$(GREEN)💾 Creating database backup...$(NC)"
	@mkdir -p backups
	@docker-compose exec -T db pg_dump -U postgres mattilda_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup created in backups/ directory$(NC)"

restore: ## Restore database (usage: make restore BACKUP_FILE=backups/backup_20240101_120000.sql)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)❌ Please specify BACKUP_FILE. Example: make restore BACKUP_FILE=backups/backup_20240101_120000.sql$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)📥 Restoring database from $(BACKUP_FILE)...$(NC)"
	@docker-compose exec -T db psql -U postgres -d mattilda_db < $(BACKUP_FILE)
	@echo "$(GREEN)✅ Database restored!$(NC)"

db-reset: ## Reset database (drop and recreate with sample data)
	@echo "$(YELLOW)🔄 Resetting database...$(NC)"
	@docker-compose restart backend
	@echo "$(GREEN)✅ Database reset completed!$(NC)"

# 🔍 CODE QUALITY
lint: ## Run linting on backend code
	@echo "$(GREEN)🔍 Running linting...$(NC)"
	@docker-compose exec backend python -m flake8 app/ || true
	@docker-compose exec backend python -m mypy app/ || true

format: ## Format backend code
	@echo "$(GREEN)✨ Formatting backend code...$(NC)"
	@docker-compose exec backend python -m black app/
	@docker-compose exec backend python -m isort app/

lint-frontend: ## Run linting on frontend code
	@echo "$(GREEN)🔍 Running frontend linting...$(NC)"
	@docker-compose exec frontend npm run lint || true

format-frontend: ## Format frontend code
	@echo "$(GREEN)✨ Formatting frontend code...$(NC)"
	@docker-compose exec frontend npm run format || true

# 📦 DEPENDENCIES
install-deps: ## Install/update dependencies for all services
	@echo "$(GREEN)📦 Installing/updating dependencies...$(NC)"
	@echo "$(YELLOW)Backend dependencies...$(NC)"
	@docker-compose exec backend pip install --upgrade pip
	@echo "$(YELLOW)Frontend dependencies...$(NC)"
	@docker-compose exec frontend npm update

deps-backend: ## Show backend dependency info
	@echo "$(GREEN)📦 Backend Dependencies:$(NC)"
	@docker-compose exec backend pip list

deps-frontend: ## Show frontend dependency info
	@echo "$(GREEN)📦 Frontend Dependencies:$(NC)"
	@docker-compose exec frontend npm list --depth=0

# 🌐 DEVELOPMENT HELPERS
open: ## Open all development URLs in browser
	@echo "$(GREEN)🌐 Opening development URLs...$(NC)"
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:5173')" 2>/dev/null || \
	python -c "import webbrowser; webbrowser.open('http://localhost:5173')" 2>/dev/null || \
	echo "$(YELLOW)Please open http://localhost:5173 manually$(NC)"
	@sleep 2
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:8000/docs')" 2>/dev/null || \
	python -c "import webbrowser; webbrowser.open('http://localhost:8000/docs')" 2>/dev/null || \
	echo "$(YELLOW)Please open http://localhost:8000/docs manually$(NC)"

urls: ## Show all development URLs
	@echo "$(GREEN)🌐 Development URLs:$(NC)"
	@echo "$(YELLOW)Frontend (React):$(NC)     http://localhost:5173"
	@echo "$(YELLOW)Backend API:$(NC)          http://localhost:8000"
	@echo "$(YELLOW)API Docs:$(NC)             http://localhost:8000/docs"
	@echo "$(YELLOW)Database:$(NC)             localhost:5435"
	@echo ""
	@echo "$(GREEN)🔐 Default Credentials:$(NC)"
	@echo "$(YELLOW)Username:$(NC) admin"
	@echo "$(YELLOW)Password:$(NC) admin123"

health: ## Check health of all services
	@echo "$(GREEN)🏥 Checking service health...$(NC)"
	@echo -n "$(YELLOW)Database:$(NC) "
	@if docker-compose exec db pg_isready -U postgres >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Healthy$(NC)"; \
	else \
		echo "$(RED)❌ Unhealthy$(NC)"; \
	fi
	@echo -n "$(YELLOW)Backend:$(NC)  "
	@if curl -s http://localhost:8000/docs >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Healthy$(NC)"; \
	else \
		echo "$(RED)❌ Unhealthy$(NC)"; \
	fi
	@echo -n "$(YELLOW)Frontend:$(NC) "
	@if curl -s http://localhost:5173 >/dev/null 2>&1; then \
		echo "$(GREEN)✅ Healthy$(NC)"; \
	else \
		echo "$(RED)❌ Unhealthy$(NC)"; \
	fi

# 🔧 DEVELOPMENT WORKFLOW
dev: ## Complete development setup (stop, clean, build, start)
	@echo "$(GREEN)🔧 Setting up complete development environment...$(NC)"
	@make stop
	@make build
	@make start
	@sleep 5
	@make health
	@make urls

# 📊 MONITORING
stats: ## Show Docker resource usage
	@echo "$(GREEN)📊 Docker Resource Usage:$(NC)"
	@docker stats --no-stream

# 🎯 QUICK ACTIONS
quick-start: start health urls ## Quick start with health check and URLs display

quick-restart: stop start health ## Quick restart with health check

# 📖 INFO
info: ## Show project information
	@echo "$(GREEN)📖 Mattilda School Management System$(NC)"
	@echo "$(YELLOW)=================================$(NC)"
	@echo "A full-stack school management system built with:"
	@echo "• Backend: FastAPI + SQLAlchemy + PostgreSQL"
	@echo "• Frontend: React + TypeScript + Vite"
	@echo "• Containerization: Docker + Docker Compose"
	@echo ""
	@echo "$(GREEN)Key Features:$(NC)"
	@echo "• Student and school management"
	@echo "• Invoice generation and tracking"
	@echo "• JWT authentication"
	@echo "• Real-time dashboard"
	@echo "• RESTful API with auto-documentation"
	@echo ""
	@echo "Run '$(YELLOW)make help$(NC)' to see all available commands"
