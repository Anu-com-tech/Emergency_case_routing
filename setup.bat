@echo off
REM Emergency Routing System - Startup Script for Windows

echo.
echo 🚑 Emergency Routing System Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "emergency_env" (
    echo ⏳ Creating Python virtual environment...
    python -m venv emergency_env
)

REM Activate virtual environment
echo ⏳ Activating virtual environment...
call emergency_env\Scripts\activate.bat

REM Install/upgrade dependencies
echo ⏳ Installing Python dependencies...
pip install -r requirements.txt

REM Install frontend dependencies
if not exist "frontend\node_modules" (
    echo ⏳ Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo.
echo ✅ Setup complete!
echo.
echo To start the application, run these commands in separate terminals:
echo.
echo 📍 Terminal 1 (Backend):
echo    emergency_env\Scripts\activate
echo    python app.py
echo.
echo 📍 Terminal 2 (Frontend):
echo    cd frontend
echo    npm start
echo.
echo ✅ Frontend will open at: http://localhost:3000
echo ✅ Backend API at: http://localhost:5000
echo ✅ API Docs at: http://localhost:5000/docs
echo.
pause
