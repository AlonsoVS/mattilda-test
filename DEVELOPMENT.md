# Mattilda Test - Development Setup

This document provides instructions for setting up and running the full-stack development environment for the Mattilda School Management System.

## 🛠️ Prerequisites

- Docker and Docker Compose
- Git (for version control)

## 🚀 Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd mattilda-test
   ```

2. **Start the development environment**:
   ```bash
   ./start-dev.sh
   ```

   Or manually:
   ```bash
   docker-compose up --build -d
   ```

3. **Access the applications**:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database**: localhost:5435 (PostgreSQL)

## 🔐 Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📁 Project Structure

```
mattilda-test/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application code
│   ├── Dockerfile.dev         # Development Docker configuration
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React/Vite frontend
│   ├── src/                   # Source code
│   ├── Dockerfile.dev         # Development Docker configuration
│   └── package.json           # Node.js dependencies
├── docker-compose.yml         # Production Docker Compose
├── docker-compose.dev.yml     # Development Docker Compose
└── start-dev.sh              # Development startup script
```

## 🐳 Docker Services

### Database (PostgreSQL)
- **Port**: 5435 (external) → 5432 (internal)
- **Database**: `mattilda_db`
- **Username**: `postgres`
- **Password**: `postgres`

### Backend (FastAPI)
- **Port**: 8000
- **Hot Reload**: Enabled via volume mounting
- **Features**:
  - JWT Authentication
  - SQLAlchemy ORM
  - Automatic API documentation
  - CORS enabled for frontend

### Frontend (React/Vite)
- **Port**: 5173
- **Hot Reload**: Enabled via volume mounting
- **Features**:
  - TypeScript support
  - Modern React development
  - Vite build system
  - API integration

## 📊 Sample Data

The development environment includes pre-populated sample data:
- **Schools**: 11 schools (10 active, 1 inactive)
- **Students**: 26 students across different grade levels
- **Invoices**: 20 invoices with various payment statuses
- **Users**: Admin user for system access

## 🔧 Development Commands

### General
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Restart a specific service
docker-compose restart backend

# Rebuild and start (after code changes)
docker-compose up --build -d
```

### Backend Development
```bash
# Access backend container
docker-compose exec backend bash

# Run tests
docker-compose exec backend python -m pytest

# Check backend health
curl http://localhost:8000/docs
```

### Frontend Development
```bash
# Access frontend container
docker-compose exec frontend sh

# Install new dependencies
docker-compose exec frontend npm install <package-name>

# Check frontend status
curl http://localhost:5173
```

### Database Operations
```bash
# Access PostgreSQL database
docker-compose exec db psql -U postgres -d mattilda_db

# View database logs
docker-compose logs db

# Backup database
docker-compose exec db pg_dump -U postgres mattilda_db > backup.sql
```

## 🔄 Hot Reload Configuration

Both frontend and backend are configured for hot reload:
- **Backend**: Code changes in `backend/app/` are automatically detected
- **Frontend**: Code changes in `frontend/src/` trigger automatic rebuilds
- **Database**: Schema changes require container restart

## 🌐 API Testing

### Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### API Endpoints
```bash
# Get schools (requires authentication)
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/schools/

# Get students
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/students/

# Get invoices
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/invoices/
```

## 🐛 Troubleshooting

### Port Conflicts
If you encounter port conflicts:
- PostgreSQL (5435): Check if another PostgreSQL instance is running
- Backend (8000): Check if another application is using port 8000
- Frontend (5173): Check if another Vite/React app is running

### Container Issues
```bash
# Remove all containers and volumes
docker-compose down -v

# Remove Docker images
docker-compose down --rmi all

# Clean Docker system
docker system prune -a
```

### Database Connection Issues
```bash
# Check database health
docker-compose exec db pg_isready -U postgres

# Restart database
docker-compose restart db
```

## 📝 Notes

- The development environment uses different ports than production to avoid conflicts
- CORS is configured to allow requests from the frontend
- All services are connected via a Docker network for internal communication
- Volume mounting enables live code reloading without rebuilding containers
- The database includes automatic schema initialization and sample data seeding

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
