@echo off
title Interactive Generative Studio

:: Check if venv exists
if not exist "venv\Scripts\activate" (
    echo [ERREUR] Environnement virtuel introuvable.
    echo          Lancez d'abord setup.bat pour installer les dependances.
    pause
    exit /b 1
)

:: Check if requirements changed
call venv\Scripts\pip install -q -r backend\requirements.txt 2>nul

echo.
echo ============================================
echo   Interactive Generative Studio
echo ============================================
echo.
echo Demarrage du serveur...
echo Acceder a : http://127.0.0.1:5000
echo Ctrl+C pour arreter
echo.

:: Run the application
call venv\Scripts\python backend\app.py

pause
