@echo off
REM Windows launcher script for Minecraft Modpack Sync

REM Try to find Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python run.py
    pause
    exit /b
)

where python3 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python3 run.py
    pause
    exit /b
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py run.py
    pause
    exit /b
)

echo ERROR: Python not found! Please install Python 3.10 or later.
echo Download from: https://www.python.org/downloads/
pause
