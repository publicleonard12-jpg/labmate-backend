@echo off
echo ========================================
echo    LabMate AI - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if requirements are installed
echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and add your API keys!
    echo Press any key to open .env in notepad...
    pause > nul
    notepad .env
    echo.
)

REM Start the server
echo ========================================
echo    Starting LabMate AI Backend Server
echo ========================================
echo.
echo Server will run on: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python app.py
