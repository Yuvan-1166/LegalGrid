#!/bin/bash

# LegalGrid Quick Start Script

echo "🚀 Starting LegalGrid Smart Legal System..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start Qdrant
echo "📦 Starting Qdrant vector database..."
cd backend
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Failed to start Qdrant. Make sure Docker is running."
    exit 1
fi
echo "✅ Qdrant started"
echo ""

# Wait for Qdrant to be ready
echo "⏳ Waiting for Qdrant to be ready..."
sleep 3

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from example..."
    cp .env.example .env
    echo "📝 Please edit backend/.env and add your GROQ_API_KEY"
    echo "   Get your free API key from: https://console.groq.com"
    echo ""
fi

# Activate virtual environment and start backend
echo "🐍 Starting backend server..."
source .venv/bin/activate

# Run setup test
echo "🧪 Running setup verification..."
python test_setup.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Setup verification failed. Please fix the issues above."
    exit 1
fi
echo ""

# Seed data if collections are empty
echo "📚 Checking if sample data needs to be seeded..."
python scripts/seed_data.py
echo ""

# Start backend in background
echo "🚀 Starting FastAPI backend..."
python main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# Start frontend
cd ../frontend
echo "⚛️  Starting React frontend..."
pnpm dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   App: http://localhost:5173"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ LegalGrid is now running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   Qdrant:    http://localhost:6333"
echo ""
echo "🛑 To stop all services, press Ctrl+C"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker-compose -f backend/docker-compose.yml stop; echo '✅ All services stopped'; exit 0" INT

wait
