@echo off
chcp 65001 >nul
title PetaniProxy - Panen Proxy Segar by @itzluthfi
cd /d "%~dp0"

echo ========================================================
echo  🌾 Starting PetaniProxy: Panen Proxy Cepat & Segar 🚜
echo ========================================================

:: Smart Python Detection (Local venv -> Global python)
set "PY_CMD=python"
if exist "d:\FREELANCE\grok-register\venv\Scripts\python.exe" (
    set "PY_CMD=d:\FREELANCE\grok-register\venv\Scripts\python.exe"
) else if exist "%~dp0venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0venv\Scripts\python.exe"
) else if exist "%~dp0..\grok-register\venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0..\grok-register\venv\Scripts\python.exe"
)

:: Check Python availability
%PY_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan di sistem Anda!
    echo Silakan install Python 3.8+ dari https://www.python.org/
    pause
    exit /b 1
)

:: Run Harvester Interactive Menu
%PY_CMD% main.py
pause
