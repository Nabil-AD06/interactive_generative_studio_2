@echo off
title Install FFmpeg
setlocal enabledelayedexpansion

echo ============================================
echo   Installation de FFmpeg
echo ============================================
echo.

:: Check if both executables already exist
if exist "backend\ffmpeg.exe" if exist "backend\ffprobe.exe" (
    echo [OK] FFmpeg et FFprobe deja installes dans backend\
    goto :check_global
)

:: Download FFmpeg
echo [1/3] Telechargement de FFmpeg...
set URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
set ZIP=%TEMP%\ffmpeg.zip

echo  - Source: %URL%
echo  - Destination: %ZIP%
echo.

powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%URL%' -OutFile '%ZIP%' -UseBasicParsing"

if %errorlevel% neq 0 (
    echo [ERREUR] Echec du telechargement
    echo.
    echo Solution manuelle :
    echo   1. Allez sur https://www.gyan.dev/ffmpeg/builds/
    echo   2. Telechargez ffmpeg-release-essentials.zip
    echo   3. Extrayez ffmpeg.exe dans le dossier backend/
    pause
    exit /b 1
)
echo [OK] Telechargement termine

:: Extract ffmpeg.exe and ffprobe.exe
echo.
echo [2/3] Extraction de FFmpeg et FFprobe...

powershell -Command "$zip='%ZIP%'; $extract='%TEMP%\ffmpeg_extract'; Expand-Archive -Path $zip -DestinationPath $extract -Force; $binDir=Get-ChildItem $extract -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1 -ExpandProperty DirectoryName; if ($binDir) { Copy-Item (Join-Path $binDir 'ffmpeg.exe') 'backend\ffmpeg.exe' -Force; Copy-Item (Join-Path $binDir 'ffprobe.exe') 'backend\ffprobe.exe' -Force; Write-Host ' [OK] Extrait vers backend/' } else { Write-Host ' [ERREUR] ffmpeg.exe introuvable dans l''archive'; exit 1 }"

if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'extraction
    echo.
    echo Solution manuelle :
    echo   1. Extrayez ffmpeg-release-essentials.zip
    echo   2. Copiez ffmpeg.exe et ffprobe.exe dans backend\
    pause
    exit /b 1
)
echo [OK] Extraction terminee

:: Cleanup
del "%ZIP%" 2>nul
rmdir /s /q "%TEMP%\ffmpeg_extract" 2>nul

:: Verify
echo.
echo [3/3] Verification...
if exist "backend\ffmpeg.exe" (
    for %%F in ("backend\ffmpeg.exe") do echo [OK] FFmpeg  : %%~zF octets
) else (
    echo [ERREUR] ffmpeg.exe introuvable
    pause
    exit /b 1
)
if exist "backend\ffprobe.exe" (
    for %%F in ("backend\ffprobe.exe") do echo [OK] FFprobe : %%~zF octets
) else (
    echo [ERREUR] ffprobe.exe introuvable
    pause
    exit /b 1
)

:check_global
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] FFmpeg disponible dans le PATH systeme
) else (
    echo.
    echo [INFO] FFmpeg n'est pas dans le PATH systeme.
    echo        Les executables dans backend/ sont utilises automatiquement.
)

echo.
echo ============================================
echo   Installation terminee !
echo ============================================
echo.
echo Redemarrez l'application avec run.bat
echo Le warning PyDub aura disparu.
echo.
pause
