@echo off
title Interactive Generative Studio - Setup

echo ============================================
echo   Interactive Generative Studio - Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo          Veuillez installer Python 3.8 ou superieur depuis python.org
    pause
    exit /b 1
)

echo [OK] Python trouve : 
python --version

:: Create virtual environment if not exists
if not exist "venv\Scripts\python.exe" (
    echo.
    echo [1/4] Creation de l'environnement virtuel...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERREUR] Echec de la creation du venv
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
) else (
    echo [OK] Environnement virtuel existe deja
)

:: Install dependencies
echo.
echo [2/4] Installation des dependances...
call venv\Scripts\pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)
echo [OK] Dependances installees

:: Create media folders
echo.
echo [3/4] Creation des dossiers media...
if not exist "media\audio" mkdir media\audio
if not exist "media\generated" mkdir media\generated
if not exist "media\uploads" mkdir media\uploads
echo [OK] Dossiers media crees

:: Create static plots folder
echo.
echo [4/4] Creation du dossier plots...
if not exist "frontend\static\plots" mkdir frontend\static\plots
echo [OK] Dossier plots cree

echo.
echo ============================================
echo   Setup termine avec succes !
echo ============================================
echo.
echo Pour lancer l'application :
echo     run.bat
echo.
echo Ou manuellement :
echo     venv\Scripts\activate ^&^& python backend\app.py
echo.
echo Optionnel - Installer FFmpeg pour l'audio :
echo     install_ffmpeg.bat
echo.
pause
