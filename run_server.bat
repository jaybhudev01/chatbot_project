@echo off
title EasyLearn Academy Chatbot Runner
echo ===================================================
echo   EasyLearn Academy Chatbot Server Startup Script
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python from https://www.python.org/ and check the
    echo option to "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Install required dependencies to ensure they are present
echo [INFO] Verifying Python dependencies...
python -m pip install fastapi uvicorn pydantic

:: Ask user for port preference (default to 8000)
echo.
echo Please specify the port you want to run the server on.
echo - Press ENTER to use the default port (8000)
echo - Type 800 if you want to use port 800
echo.
set /p PORT="Enter port number [default: 8000]: "

if "%PORT%"=="" (
    set PORT=8000
)

echo.
echo [INFO] Starting chatbot server on port %PORT%...
echo [INFO] Automatically opening your browser to http://127.0.0.1:%PORT%...
echo.

:: Wait 2 seconds and open the browser
start "" "http://127.0.0.1:%PORT%"

:: Run the FastAPI application
python main.py %PORT%

pause
