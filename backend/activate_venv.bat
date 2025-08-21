@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo To run the backend server:
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo To run tests:
echo   pytest tests/ -v
echo.
cmd /k
