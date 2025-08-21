@echo off
REM Setup script for Windows - Creates virtual environment and installs dependencies

echo 🚀 Setting up Python virtual environment for Cinei-Reader Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Remove existing venv if it exists
if exist "venv" (
    echo 🧹 Removing existing virtual environment...
    rmdir /s /q venv
)

REM Create new virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo 📈 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)

echo.
echo ✅ Virtual environment setup complete!
echo.
echo 📋 Next steps:
echo   1. Activate the environment: activate_venv.bat
echo   2. Set up your .env file (copy from env.template)
echo   3. Run database migrations: alembic upgrade head
echo   4. Start the server: uvicorn app.main:app --reload --host 127.0.0.1 --port 8003
echo.
echo 🧪 To run tests:
echo   pytest tests/ -v
echo.
pause
