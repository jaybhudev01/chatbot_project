@echo off
title Stop Chatbot Server
echo ====================================================
echo   Stopping Chatbot Server...
echo ====================================================
echo.

:: Find the PID using port 8000 and terminate it
set FOUND=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
    set FOUND=1
)

:: Also clean up any loose pythonw/python processes running main.py
wmic process where "commandline like '%%main.py%%'" call terminate >nul 2>&1

echo.
if %FOUND%==1 (
    echo [SUCCESS] The chatbot server running on port 8000 has been stopped.
) else (
    echo [INFO] No running chatbot server was found on port 8000.
)
echo.
pause
