#!/bin/bash

# Docker Configuration Test Script
set -e

echo "🐳 Testing Docker Configuration for Mattilda"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed or not in PATH"
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Check if .env.docker file exists, if not show error
if [ ! -f .env.docker ]; then
    echo "❌ .env.docker file not found. This is required for Docker development."
    echo "📄 The file should already exist with Docker development configuration."
    exit 1
fi

echo "✅ Environment files are properly configured"

# Test building the Docker image
echo "🔨 Testing Docker image build..."
if docker build -t mattilda-test:test -f Dockerfile . > /dev/null 2>&1; then
    echo "✅ Docker image builds successfully"
else
    echo "❌ Docker image build failed"
    exit 1
fi

# Test Docker Compose configuration
echo "🔧 Validating Docker Compose configuration..."
if docker-compose config > /dev/null 2>&1; then
    echo "✅ Docker Compose configuration is valid"
else
    echo "❌ Docker Compose configuration is invalid"
    exit 1
fi

# Test production Docker Compose configuration
echo "🔧 Validating Production Docker Compose configuration..."
if docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    echo "✅ Production Docker Compose configuration is valid"
else
    echo "❌ Production Docker Compose configuration is invalid"
    exit 1
fi

# Cleanup test image
echo "🧹 Cleaning up test image..."
docker rmi mattilda-test:test > /dev/null 2>&1 || true

echo ""
echo "🎉 All Docker configuration tests passed!"
echo ""
echo "Next steps:"
echo "1. Run 'make dev' to start the development environment"
echo "2. Access the API at http://localhost:8000"
echo "3. View API docs at http://localhost:8000/docs"
echo "4. Run 'make pgadmin' for database management"
