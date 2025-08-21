#!/bin/bash
# Setup script for Unix/Linux/macOS - Creates virtual environment and installs dependencies

echo "🚀 Setting up Python virtual environment for Cinei-Reader Backend..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

echo "✅ Python found"
python3 --version

# Remove existing venv if it exists
if [ -d "venv" ]; then
    echo "🧹 Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "📈 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check requirements.txt and try again"
    exit 1
fi

echo
echo "✅ Virtual environment setup complete!"
echo
echo "📋 Next steps:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Set up your .env file (copy from env.template)"
echo "  3. Run database migrations: alembic upgrade head"
echo "  4. Start the server: uvicorn app.main:app --reload --host 127.0.0.1 --port 8003"
echo
echo "🧪 To run tests:"
echo "  pytest tests/ -v"
echo
