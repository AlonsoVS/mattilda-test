# Mattilda - School Management System

A modern school management system built with FastAPI, PostgreSQL, and clean architecture principles.

## 🏗️ Architecture

This project follows **Domain-Driven Design (DDD)** and **Clean Architecture** principles:

```
app/
├── core/           # Application configuration and shared utilities
├── domain/         # Business logic and domain models
├── application/    # Application services and DTOs
├── infrastructure/ # External concerns (database, persistence)
└── presentation/   # API controllers and routes
```

## 🚀 Quick Start

### Choose Your Development Environment

This project supports three different development environments:

#### 🏠 **Local Development** (without Docker)
```bash
# Requires local PostgreSQL installation
# Use .env configuration

# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up local environment (optional helper)
python setup_env.py

# 3. Run the application
make local
# OR
uvicorn app.main:app --reload
```

#### 🐳 **Docker Development** 
```bash
# Complete containerized environment
# Use .env.docker configuration

# Start development environment
make dev

# Access the application
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - DB Admin: make pgadmin → http://localhost:5050
```

#### 🚀 **Docker Production**
```bash
# Production-ready deployment
# Use .env.prod configuration

# 1. Configure production environment
# Edit .env.prod with secure values

# 2. Deploy
make prod
```

### Environment Configuration Helper

Use the interactive setup tool to choose and configure your environment:

```bash
python setup_env.py
```

## 📊 Features

### Core Entities
- **Schools**: Complete school management with address, contact info, and principal details
- **Students**: Student records with enrollment, grade levels, and contact information  
- **Invoices**: Billing system with payment tracking and status management

### API Capabilities
- **CRUD Operations**: Full Create, Read, Update, Delete for all entities
- **Advanced Filtering**: Filter by any field with partial matching
- **Pagination**: Configurable page size and navigation
- **Validation**: Comprehensive business rule validation
- **Type Safety**: Full type hints and Pydantic models

### Filtering Examples
```bash
# Filter schools by state and city
GET /api/v1/schools/?state=CA&city=Los%20Angeles&page=1&size=10

# Filter students by grade and school
GET /api/v1/students/?grade_level=10&school_id=1&is_active=true

# Filter invoices by status and date range
GET /api/v1/invoices/?status=pending&amount_min=100&amount_max=1000
```

## 🛠️ Development

### Local Development (Docker)
```bash
# Start development environment
make dev

# View logs
make logs-backend

# Run tests
make test

# Open backend shell
make shell

# Open database shell  
make db-shell
```

### Local Development (Native)
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your database settings

# Run the application
uvicorn app.main:app --reload

# Run tests
python run_tests.py domain --verbose
```

## 🐘 Database

### Schema
- **schools**: School information and metadata
- **students**: Student records linked to schools
- **invoices**: Billing records linked to students and schools

### Management
```bash
# Access database shell
make db-shell

# Start pgAdmin for GUI management
make pgadmin

# Create backup
make backup

# Restore from backup
make restore BACKUP_FILE=backups/backup_20240101_120000.sql
```

## 🧪 Testing

### Unit Tests (72 total tests)
- **Domain Models**: Complete business logic validation
- **Test Coverage**: 100% coverage of domain layer
- **Test Categories**: Validation, business methods, boundary values

```bash
# Run all domain tests
make test
# OR
python run_tests.py domain --verbose

# Run specific test file
pytest tests/unit/domain/test_school_model.py -v

# Run with coverage
python run_tests.py coverage
```

## 🚀 Production Deployment

### 1. Prepare Environment
```bash
# Copy and configure production environment
cp .env.prod.example .env.prod

# Edit .env.prod with secure production values:
# - Strong DATABASE_PASSWORD
# - Secure SECRET_KEY (32+ chars)
# - Proper ALLOWED_ORIGINS
# - Production database settings
```

### 2. Deploy
```bash
# Start production environment
make prod

# OR manually
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### 3. Verify Deployment
```bash
# Check health
curl https://yourdomain.com/health

# Monitor services
make status
make logs
```

## 📖 API Documentation

### Endpoints

#### Schools
- `GET /api/v1/schools/` - List schools with filtering
- `POST /api/v1/schools/` - Create new school
- `GET /api/v1/schools/{id}` - Get school by ID
- `PUT /api/v1/schools/{id}` - Update school
- `DELETE /api/v1/schools/{id}` - Delete school

#### Students  
- `GET /api/v1/students/` - List students with filtering
- `POST /api/v1/students/` - Create new student
- `GET /api/v1/students/{id}` - Get student by ID
- `PUT /api/v1/students/{id}` - Update student
- `DELETE /api/v1/students/{id}` - Delete student

#### Invoices
- `GET /api/v1/invoices/` - List invoices with filtering
- `POST /api/v1/invoices/` - Create new invoice
- `GET /api/v1/invoices/{id}` - Get invoice by ID
- `PUT /api/v1/invoices/{id}` - Update invoice
- `DELETE /api/v1/invoices/{id}` - Delete invoice

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Files

The project uses different environment files for different scenarios:

- **`.env`** - Default environment
- **`.env.docker`** - Docker development environment  
- **`.env.prod`** - Docker production environment

#### Local Development (.env)
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/mattilda_db
ENVIRONMENT=development
DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000
```

#### Docker Development (.env.docker)
```bash
DATABASE_URL=postgresql://mattilda_user:mattilda_password@db:5432/mattilda_db
ENVIRONMENT=development
DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
```

#### Docker Production (.env.prod)
```bash
DATABASE_URL=postgresql://prod_user:SECURE_PASSWORD@db:5432/mattilda_prod
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=VERY_LONG_SECURE_KEY_32_PLUS_CHARACTERS
ALLOWED_ORIGINS=https://yourdomain.com
```

### Environment Variables

#### Database
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_HOST` - Database host
- `DATABASE_PORT` - Database port (default: 5432)
- `DATABASE_NAME` - Database name
- `DATABASE_USER` - Database username
- `DATABASE_PASSWORD` - Database password

#### Application
- `ENVIRONMENT` - Environment mode (development/production)
- `DEBUG` - Debug mode (true/false)
- `SECRET_KEY` - JWT signing key (**CHANGE IN PRODUCTION!**)
- `ALLOWED_ORIGINS` - CORS allowed origins
- `APP_HOST` - Application host (127.0.0.1 for local, 0.0.0.0 for Docker)
- `APP_PORT` - Application port (default: 8000)

## 📋 Available Commands

### Docker Commands (via Makefile)
```bash
make local       # Run locally without Docker
make dev         # Start Docker development environment
make prod        # Start Docker production environment  
make build       # Build Docker images
make up          # Start services
make down        # Stop services
make restart     # Restart services
make logs        # Show all logs
make logs-backend # Show backend logs
make logs-db     # Show database logs
make clean       # Clean up everything
make test        # Run tests
make shell       # Open backend shell
make db-shell    # Open database shell
make pgadmin     # Start pgAdmin
make status      # Check service status
make backup      # Create database backup
make restore     # Restore database
```

### Environment Commands
```bash
python setup_env.py          # Interactive environment setup
python setup_env.py info     # Show environment information
python setup_env.py check    # Check environment files
python setup_env.py status   # Show current configuration
```

### Test Commands
```bash
python run_tests.py domain    # Run domain tests
python run_tests.py coverage  # Run with coverage
python run_tests.py specific --test-path tests/unit/domain/test_school_model.py
```

## 🏗️ Project Structure

```
mattilda-test/
├── app/
│   ├── core/                 # Configuration and utilities
│   ├── domain/              # Domain models and business logic
│   │   ├── models/          # Domain entities
│   │   ├── repositories/    # Repository interfaces
│   │   └── enums.py         # Domain enums
│   ├── application/         # Application layer
│   │   ├── dtos/           # Data transfer objects
│   │   └── services/       # Application services
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── database/       # Database connection
│   │   ├── persistence/    # Database entities
│   │   ├── repositories/   # Repository implementations
│   │   └── mappers/        # Domain/Entity mappers
│   └── presentation/        # Presentation layer
│       └── api/v1/         # API controllers
├── tests/
│   └── unit/domain/        # Domain model tests
├── docker/                 # Docker configuration
├── backups/               # Database backups
├── Dockerfile             # Development container
├── Dockerfile.prod        # Production container
├── docker-compose.yml     # Development orchestration
├── docker-compose.prod.yml # Production orchestration
├── Makefile              # Convenience commands
└── requirements.txt      # Python dependencies
```
