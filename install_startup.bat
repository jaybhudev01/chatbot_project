@echo off
title Chatbot Startup Installer
echo ====================================================
echo   Setting up Chatbot Server to Run Permanently
echo ====================================================
echo.

set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set VBS_PATH=%STARTUP_DIR%\launch_chatbot.vbs

echo [INFO] Creating startup configuration...
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run "cmd /c ""d:\chatboat\run_silent.bat""", 0, False
) > "%VBS_PATH%"

echo [INFO] Startup script registered at:
echo %VBS_PATH%
echo.

echo [INFO] Starting the chatbot server in the background now...
wscript "%VBS_PATH%"

echo.
echo ====================================================
echo   SUCCESS! The chatbot server is now running.
echo   It will start automatically every time Windows boots.
echo   You can access it at: http://127.0.0.1:8000
echo ====================================================
echo.
pause
