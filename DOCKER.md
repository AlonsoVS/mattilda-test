# Docker Configuration Guide

This document explains how to run the Mattilda school management system using Docker and Docker Compose.

## 🐳 Docker Setup

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Make (optional, for convenience commands)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd mattilda-test
   ```

2. **Start development environment**:
   ```bash
   make dev
   # OR
   docker-compose up -d
   ```

3. **Access the application**:
   - **API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## 📁 Docker Files Overview

### Core Files
- `Dockerfile` - Development container configuration
- `Dockerfile.prod` - Production optimized container
- `docker-compose.yml` - Development environment
- `docker-compose.prod.yml` - Production environment
- `Makefile` - Convenience commands

### Configuration
- `.env.example` - Development environment variables template
- `.env.prod.example` - Production environment variables template
- `docker/init-db/01-init.sh` - Database initialization script

## 🔧 Services

### Backend Service
- **Image**: Custom built from `Dockerfile`
- **Port**: 8000
- **Health Check**: GET /health
- **Auto-reload**: Enabled in development
- **Dependencies**: PostgreSQL database

### Database Service
- **Image**: postgres:15-alpine
- **Port**: 5432
- **Database**: mattilda_db
- **User**: mattilda_user
- **Persistent**: Data stored in Docker volume

### pgAdmin Service (Optional)
- **Image**: dpage/pgadmin4:latest
- **Port**: 5050
- **Profile**: tools (start with `make pgadmin`)
- **Purpose**: Database administration interface

## 🚀 Usage Commands

### Development

```bash
# Start development environment
make dev
# OR
docker-compose up -d

# View logs
make logs
make logs-backend  # Backend only
make logs-db       # Database only

# Run tests
make test

# Open backend shell
make shell

# Open database shell
make db-shell

# Start pgAdmin
make pgadmin
```

### Production

```bash
# Setup production environment
cp .env.prod.example .env.prod
# Edit .env.prod with production values

# Start production environment
make prod
# OR
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Maintenance

```bash
# Check service status
make status

# View resource usage
make stats

# Restart services
make restart

# Stop services
make down

# Clean up everything
make clean

# Backup database
make backup

# Restore database
make restore BACKUP_FILE=backups/backup_20240101_120000.sql
```

## 🔐 Environment Configuration

### Development (.env)

```bash
# Copy and modify
cp .env.example .env
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret (change in production!)
- `DEBUG` - Enable debug mode
- `ALLOWED_ORIGINS` - CORS allowed origins

### Production (.env.prod)

```bash
# Copy and modify with secure values
cp .env.prod.example .env.prod
```

**⚠️ Security Requirements:**
- Change `DATABASE_PASSWORD` to a strong password
- Generate a secure `SECRET_KEY` (32+ characters)
- Set proper `ALLOWED_ORIGINS` for your domains
- Use HTTPS in production

## 🌐 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Routes
- **Schools**: `/api/v1/schools/`
- **Students**: `/api/v1/students/`
- **Invoices**: `/api/v1/invoices/`

## 🐘 Database Management

### Access Database
```bash
# Using make command
make db-shell

# Direct docker command
docker-compose exec db psql -U mattilda_user -d mattilda_db
```

### Using pgAdmin
```bash
# Start pgAdmin
make pgadmin

# Access at http://localhost:5050
# Email: admin@mattilda.com
# Password: admin123
```

### Database Connection in pgAdmin
- **Host**: db (or localhost if connecting from host)
- **Port**: 5432
- **Database**: mattilda_db
- **Username**: mattilda_user
- **Password**: mattilda_password

## 📊 Monitoring and Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f db

# Using make
make logs
make logs-backend
make logs-db
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready -U mattilda_user -d mattilda_db
```

### Resource Monitoring
```bash
# Service status
make status

# Resource usage
make stats
```

## 🔧 Development Workflow

### 1. Setup Development Environment
```bash
make dev
```

### 2. Make Code Changes
- Code changes are automatically reflected (hot reload)
- Database schema changes require restart

### 3. Run Tests
```bash
make test
```

### 4. Check Logs
```bash
make logs-backend
```

### 5. Database Operations
```bash
# View data
make db-shell

# Or use pgAdmin
make pgadmin
```

## 🚀 Production Deployment

### 1. Prepare Environment
```bash
cp .env.prod.example .env.prod
# Edit .env.prod with production values
```

### 2. Deploy
```bash
make prod
```

### 3. Verify Deployment
```bash
curl https://yourdomain.com/health
```

### 4. Monitor
```bash
make logs
make status
```

## 🔄 Data Persistence

### Development
- Database data persists in Docker volume `postgres_data`
- Application code is mounted for hot reload

### Production
- Database data persists in Docker volume
- Application code is copied into container

### Backup and Restore
```bash
# Create backup
make backup

# Restore from backup
make restore BACKUP_FILE=backups/backup_20240101_120000.sql
```

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5432

# Stop conflicting services
make down
```

#### Database Connection Issues
```bash
# Check database health
docker-compose exec db pg_isready -U mattilda_user -d mattilda_db

# Restart database
docker-compose restart db
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Reset Everything
```bash
# Clean up and start fresh
make clean
make dev
```

## 📈 Performance Optimization

### Development
- Hot reload enabled for fast development
- Debug mode enabled
- Single worker process

### Production
- Multi-worker Uvicorn setup
- Optimized Docker image with multi-stage build
- Health checks and restart policies
- Resource limits (configure as needed)

## 🔒 Security Considerations

### Development
- Default passwords (change for production)
- Debug mode enabled
- Permissive CORS settings

### Production
- Strong passwords required
- Debug mode disabled
- Restricted CORS settings
- HTTPS recommended
- Regular security updates

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
