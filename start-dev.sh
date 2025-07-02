#!/bin/bash

# Mattilda Test - Development Environment Startup Script
echo "🚀 Starting Mattilda School Management System Development Environment..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Start all services
echo "🔨 Building and starting all services..."
docker-compose up --build -d

# Wait a moment for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo "✅ Development environment is ready!"
echo ""
echo "🌐 Services available at:"
echo "   Frontend (React/Vite): http://localhost:5173"
echo "   Backend API (FastAPI): http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Database (PostgreSQL): localhost:5435"
echo ""
echo "🔐 Default admin credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "💻 Useful commands:"
echo "   View logs: docker-compose logs -f [service_name]"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   View backend logs: docker-compose logs -f backend"
echo "   View frontend logs: docker-compose logs -f frontend"
echo ""
echo "🎯 The system includes sample data for testing:"
echo "   - 11 schools (10 active, 1 inactive)"
echo "   - 26 students across different grade levels"
echo "   - 20 invoices with various statuses"
