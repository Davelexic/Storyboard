#!/bin/bash
# Activate virtual environment script for Unix/Linux/macOS

echo "🔧 Activating virtual environment..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup_venv.sh first to create the virtual environment."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated!"
echo
echo "📋 Available commands:"
echo "  🚀 Start server:     uvicorn app.main:app --reload --host 127.0.0.1 --port 8003"
echo "  🧪 Run tests:       pytest tests/ -v"
echo "  📊 Run test server: python test_server.py"
echo "  🔍 Check imports:   python -c \"import app.main; print('✅ All imports working')\""
echo "  📝 Database migration: alembic upgrade head"
echo
echo "💡 Type 'deactivate' to exit the virtual environment"
echo

# Start a new shell session with the virtual environment activated
exec $SHELL
