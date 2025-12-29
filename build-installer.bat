@echo off
REM Complete build script: EXE + Installer
REM Similar to electron-builder workflow

echo ========================================
echo The Artificer - TTS Voice Generator
echo Complete Build: EXE + Installer
echo ========================================
echo.

REM Step 1: Check for PyInstaller
echo [Step 1/4] Checking dependencies...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
echo.

REM Step 2: Build EXE with PyInstaller
echo [Step 2/4] Building EXE with PyInstaller...
if exist build rmdir /s /q build
if exist dist\TTRPGVoiceLab rmdir /s /q dist\TTRPGVoiceLab

pyinstaller ttrpg_voice_lab.spec
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)
echo.

REM Step 3: Copy additional files
echo [Step 3/4] Copying additional files...
if exist models (
    xcopy models dist\TTRPGVoiceLab\models\ /E /I /Y >nul
    echo   - Models copied
) else (
    echo   WARNING: No models folder found!
)

if exist docs (
    xcopy docs dist\TTRPGVoiceLab\docs\ /E /I /Y >nul
    echo   - Documentation copied
)

copy LICENSE dist\TTRPGVoiceLab\ >nul 2>&1
copy README.md dist\TTRPGVoiceLab\ >nul 2>&1
echo.

REM Step 4: Check for Inno Setup and build installer
echo [Step 4/4] Building installer with Inno Setup...

REM Check if Inno Setup is installed
set INNO_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
)

if not defined INNO_PATH (
    echo.
    echo WARNING: Inno Setup not found!
    echo.
    echo The EXE is ready in dist\TTRPGVoiceLab\
    echo.
    echo To create an installer:
    echo   1. Download Inno Setup from: https://jrsoftware.org/isdl.php
    echo   2. Install Inno Setup
    echo   3. Run this script again
    echo.
    echo ========================================
    echo Build Complete (EXE Only)
    echo ========================================
    echo.
    echo Executable location:
    echo   dist\TTRPGVoiceLab\TTRPGVoiceLab.exe
    echo.
    pause
    exit /b 0
)

REM Build installer with Inno Setup
"%INNO_PATH%" installer.iss
if errorlevel 1 (
    echo.
    echo ERROR: Installer build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Portable EXE:
echo   dist\TTRPGVoiceLab\TTRPGVoiceLab.exe
echo.
echo Installer:
echo   installer_output\TheArtificer-TTS-Setup-1.0.0.exe
echo.
echo To test installer:
echo   Run installer_output\TheArtificer-TTS-Setup-1.0.0.exe
echo.
echo To distribute:
echo   Share the installer EXE (recommended)
echo   OR zip the dist\TTRPGVoiceLab folder (portable)
echo ========================================
echo.
pause
