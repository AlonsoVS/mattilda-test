# Mattilda Development - Quick Reference

## 🚀 Essential Commands

```bash
make start          # Start everything (quickest way to begin)
make stop           # Stop all services
make status         # Check what's running
make health         # Check if services are healthy
make urls           # Show all development URLs
make help           # Show all available commands
```

## 🔧 Development Workflow

```bash
# Daily development routine
make quick-start    # Start + health check + URLs
make logs-backend   # Monitor backend during development
make shell          # Jump into backend container for debugging
make test           # Run tests before committing
make stop           # End development session
```

## 🐛 Troubleshooting

```bash
make clean          # Clean up Docker resources
make rebuild        # Rebuild images from scratch
make reset          # Nuclear option: reset everything
make health         # Check service health
make logs           # View all logs
```

## 💾 Database Operations

```bash
make backup         # Create database backup
make db-reset       # Reset database with fresh sample data
make shell-db       # Access PostgreSQL directly
```

## 📊 Monitoring & Quality

```bash
make stats          # Docker resource usage
make lint           # Code quality checks
make format         # Auto-format code
make test-coverage  # Run tests with coverage report
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5435

## 🔐 Default Credentials

- **Username**: admin
- **Password**: admin123

## 📁 Hot Reload

Both frontend and backend have hot reload enabled:
- Change files in `frontend/src/` → Frontend auto-reloads
- Change files in `backend/app/` → Backend auto-reloads
- Database schema changes → Restart backend: `make restart backend`

## 🎯 Sample Data

The system comes pre-loaded with:
- 11 schools (10 active, 1 inactive)
- 26 students across different grade levels  
- 20 invoices with various payment statuses
- Admin user for immediate testing
