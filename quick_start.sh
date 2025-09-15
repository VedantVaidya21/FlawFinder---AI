#!/bin/bash

# FlawFinder AI - Quick Start Script
# This script provides a quick way to set up and start the FlawFinder AI application

set -e  # Exit on any error

echo "🚀 FlawFinder AI - Quick Start Setup"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed and running
check_docker() {
    print_status "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+ first."
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    required_version="3.11"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        print_warning "Python $python_version detected. Python 3.11+ is recommended."
    fi
    
    print_success "Python is installed"
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        echo "Visit: https://nodejs.org/"
        exit 1
    fi
    
    print_success "Node.js is installed"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Install setup dependencies
    pip3 install -r requirements_setup.txt
    
    # Install backend dependencies
    cd backend
    pip3 install -r requirements.txt
    cd ..
    
    print_success "Python dependencies installed"
}

# Install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."
    
    cd client
    npm install
    cd ..
    
    print_success "Node.js dependencies installed"
}

# Set up database
setup_database() {
    print_status "Setting up database..."
    
    # Run the database setup script
    python3 setup_database.py
    
    if [ $? -eq 0 ]; then
        print_success "Database setup completed"
    else
        print_error "Database setup failed. Please check the manual setup instructions."
        exit 1
    fi
}

# Start the application
start_application() {
    print_status "Starting FlawFinder AI application..."
    
    # Start backend in background
    print_status "Starting backend server..."
    cd backend
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 5
    
    # Start frontend
    print_status "Starting frontend server..."
    cd client
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Application started successfully!"
    echo ""
    echo "🌐 Application URLs:"
    echo "   Frontend: http://localhost:5173"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 Database Services:"
    echo "   PostgreSQL: localhost:5432"
    echo "   Redis: localhost:6379"
    echo "   Neo4j: http://localhost:7474"
    echo ""
    echo "🔑 Default Login Credentials:"
    echo "   Email: admin@flawfinder.ai"
    echo "   Password: admin123"
    echo ""
    echo "Press Ctrl+C to stop the application"
    
    # Wait for user to stop
    wait
}

# Cleanup function
cleanup() {
    print_status "Stopping application..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    print_success "Application stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "Starting FlawFinder AI setup..."
    echo ""
    
    # Run checks
    check_docker
    check_python
    check_node
    
    # Install dependencies
    install_python_deps
    install_node_deps
    
    # Set up database
    setup_database
    
    # Start application
    start_application
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "FlawFinder AI - Quick Start Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --setup-only   Only run setup, don't start the application"
        echo "  --start-only   Skip setup and start the application"
        echo ""
        echo "This script will:"
        echo "  1. Check system requirements (Docker, Python, Node.js)"
        echo "  2. Install dependencies"
        echo "  3. Set up database infrastructure"
        echo "  4. Start the application"
        echo ""
        echo "Prerequisites:"
        echo "  - Docker and Docker Compose"
        echo "  - Python 3.11+"
        echo "  - Node.js 16+"
        echo "  - Internet connection"
        exit 0
        ;;
    --setup-only)
        print_status "Running setup only..."
        check_docker
        check_python
        check_node
        install_python_deps
        install_node_deps
        setup_database
        print_success "Setup completed! Run '$0 --start-only' to start the application."
        exit 0
        ;;
    --start-only)
        print_status "Starting application only..."
        start_application
        ;;
    *)
        main
        ;;
esac
