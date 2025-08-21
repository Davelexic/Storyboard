@echo off
REM Activate virtual environment script for Windows

echo 🔧 Activating virtual environment...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup_venv.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated!
echo.
echo 📋 Available commands:
echo   🚀 Start server:     uvicorn app.main:app --reload --host 127.0.0.1 --port 8003
echo   🧪 Run tests:       pytest tests/ -v
echo   📊 Run test server: python test_server.py
echo   🔍 Check imports:   python -c "import app.main; print('✅ All imports working')"
echo   📝 Database migration: alembic upgrade head
echo.
echo 💡 Type 'deactivate' to exit the virtual environment
echo.
cmd /k
