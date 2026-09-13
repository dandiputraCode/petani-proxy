@echo off
chcp 65001 >nul
title OmniProxy Harvester - by @itzluthfi
cd /d "%~dp0"

echo ========================================================
echo  🚀 Starting OmniProxy Harvester...
echo ========================================================

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan di sistem Anda!
    echo Silakan install Python 3.8+ dari https://www.python.org/
    pause
    exit /b 1
)

:: Install dependencies if colorama is missing
python -c "import colorama, httpx, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Menginstall dependensi yang dibutuhkan...
    pip install -r requirements.txt
)

:: Run Harvester Interactive Menu
python main.py
pause
