@echo off
echo Starting Cinematic Reading Engine Backend...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Test the setup first
echo Testing setup...
python test_setup.py

REM Start the server
echo.
echo Starting server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
