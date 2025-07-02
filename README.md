# Mattilda Test Project - School Management System

A modern, full-stack school management system built with FastAPI and React.

## 🚀 Quick Start

The easiest way to get started is using the included Makefile:

```bash
# Start the complete development environment
make start

# Check service status
make status

# View all available commands
make help
```

## Project Structure

This project is organized as a monorepo with separate frontend and backend applications:

```
mattilda-test/
├── backend/          # FastAPI backend application
├── frontend/         # React frontend application
├── docker-compose.yml # Docker Compose configuration
├── Makefile          # Development commands
├── start-dev.sh      # Quick start script
├── DEVELOPMENT.md    # Detailed development guide
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Make (for using Makefile commands)

### Development with Docker (Recommended)

The fastest way to get up and running:

```bash
# Start everything (database, backend, frontend)
make start

# Check that all services are healthy
make health

# View development URLs and credentials
make urls

# View logs from all services
make logs

# Stop everything
make stop
```

### Available Makefile Commands

```bash
# Environment Management
make start              # Start full development environment
make stop               # Stop all services
make restart            # Restart all services
make status             # Show service status
make health             # Check service health

# Development
make build              # Build Docker images
make rebuild            # Rebuild without cache
make clean              # Clean up Docker resources
make reset              # Full reset (destructive)

# Logs and Monitoring
make logs               # All service logs
make logs-backend       # Backend logs only
make logs-frontend      # Frontend logs only
make logs-db            # Database logs only

# Shell Access
make shell              # Backend container shell
make shell-frontend     # Frontend container shell
make shell-db           # PostgreSQL shell

# Testing and Quality
make test               # Run backend tests
make lint               # Run code linting
make format             # Format code

# Database Operations
make backup             # Create database backup
make db-reset           # Reset database with sample data

# Utilities
make urls               # Show development URLs
make info               # Project information
make help               # Show all commands
```

### Manual Development

For manual setup without Docker:

### Backend Development

The backend is a FastAPI application with a clean architecture following Domain-Driven Design (DDD) principles.

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

See [backend/README.md](backend/README.md) for detailed backend documentation.

### Frontend Development

The frontend is a React application built with modern tools and best practices.

```bash
cd frontend
npm install
npm start
```

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## Architecture Overview

### Backend (FastAPI)
- **Clean Architecture** with Domain-Driven Design
- **Layered Structure**: Presentation → Application → Domain → Infrastructure
- **Authentication & Authorization** with JWT tokens
- **Database**: SQLite with SQLModel ORM
- **API Documentation**: Automatic OpenAPI/Swagger docs
- **Testing**: Comprehensive unit and integration tests

### Frontend (React)
- **Modern React** with functional components and hooks
- **TypeScript** for type safety
- **State Management**: Context API or Redux Toolkit
- **UI Components**: Material-UI or Tailwind CSS
- **API Client**: Axios with automatic error handling
- **Authentication**: JWT token management

## Features

- 👥 **User Management**: Registration, authentication, role-based access
- 🏫 **School Management**: Multiple schools, grades, and classes
- 👨‍🎓 **Student Management**: Student profiles, enrollment, and tracking
- 📄 **Invoice Management**: Billing, payments, and financial tracking
- 📊 **Reports & Analytics**: Student performance and financial reports
- 🔍 **Advanced Filtering**: Pagination and search across all entities
- 🔐 **Security**: JWT authentication, role-based permissions
- 📱 **Responsive Design**: Mobile-friendly interface
- 🐳 **Docker Support**: Containerized deployment

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh
- `GET /auth/me` - Current user profile
- `GET /auth/users` - List users (admin, with pagination/filtering)

### Students
- `GET /students` - List students (with pagination/filtering)
- `POST /students` - Create student
- `GET /students/{id}` - Get student details
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student
- `GET /students/{id}/account-statement` - Student account statement

### Schools & Invoices
- Full CRUD operations for schools and invoices
- Advanced filtering and pagination support

## Development

### Running with Docker

```bash
# Start the full stack
docker-compose up -d

# Backend only
docker-compose up backend

# Frontend only
docker-compose up frontend
```

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Production Deployment

```bash
# Build and deploy with Docker
docker-compose -f backend/docker-compose.prod.yml up -d
```

### Environment Variables

Copy the example environment files and configure:
- `.env` - Development environment
- `.env.docker` - Docker development environment  
- `.env.prod` - Production environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or support, please open an issue on GitHub.
