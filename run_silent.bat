@echo off
cd /d "d:\chatboat"
:: Check if port 8000 is already in use. If it is, free it up.
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)
:: Start the server on port 8000
python main.py 8000
