@echo off
REM Build script for The Artificer - TTS Voice Generator (NSIS Version)
REM Creates installer using NSIS instead of Inno Setup

echo ========================================
echo The Artificer - TTS Voice Generator
echo Complete Build: EXE + NSIS Installer
echo ========================================
echo.

REM Step 1: Check for PyInstaller
echo [Step 1/4] Checking dependencies...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)
echo.

REM Step 2: Build EXE with PyInstaller
echo [Step 2/4] Building EXE with PyInstaller...
if exist build rmdir /s /q build
if exist dist\TTRPGVoiceLab rmdir /s /q dist\TTRPGVoiceLab

python -m PyInstaller ttrpg_voice_lab.spec
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

if exist presets (
    xcopy presets dist\TTRPGVoiceLab\presets\ /E /I /Y >nul
    echo   - Presets copied
) else (
    echo   WARNING: No presets folder found!
)

REM Bundle source code for GPL compliance
echo   - Bundling source code for GPL compliance...
if not exist dist\TTRPGVoiceLab\source mkdir dist\TTRPGVoiceLab\source

REM Copy Python source files
xcopy src dist\TTRPGVoiceLab\source\src\ /E /I /Y >nul

REM Copy preset configurations
xcopy presets dist\TTRPGVoiceLab\source\presets\ /E /I /Y >nul

REM Copy license and documentation to source folder
copy LICENSE dist\TTRPGVoiceLab\source\ >nul 2>&1
copy THIRD_PARTY_LICENSES.txt dist\TTRPGVoiceLab\source\ >nul 2>&1
copy README.md dist\TTRPGVoiceLab\source\ >nul 2>&1
copy SOURCE_README.txt dist\TTRPGVoiceLab\source\ >nul 2>&1
copy requirements.txt dist\TTRPGVoiceLab\source\ >nul 2>&1

REM Copy build scripts
copy build.bat dist\TTRPGVoiceLab\source\ >nul 2>&1
copy build-installer-nsis.bat dist\TTRPGVoiceLab\source\ >nul 2>&1
copy ttrpg_voice_lab.spec dist\TTRPGVoiceLab\source\ >nul 2>&1
copy TheArtificer-Installer.nsi dist\TTRPGVoiceLab\source\ >nul 2>&1

REM Copy top-level license files for easy access
copy LICENSE dist\TTRPGVoiceLab\ >nul 2>&1
copy THIRD_PARTY_LICENSES.txt dist\TTRPGVoiceLab\ >nul 2>&1
copy SOURCE_README.txt dist\TTRPGVoiceLab\ >nul 2>&1
echo   - Source code bundled
echo.

REM Step 4: Check for NSIS and build installer
echo [Step 4/4] Building installer with NSIS...

REM Check if NSIS is installed
set "NSIS_PATH="
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files (x86)\NSIS\makensis.exe"
) else if exist "C:\Program Files\NSIS\makensis.exe" (
    set "NSIS_PATH=C:\Program Files\NSIS\makensis.exe"
)

if not defined NSIS_PATH (
    echo.
    echo WARNING: NSIS not found!
    echo.
    echo The EXE is ready in dist\TTRPGVoiceLab\
    echo.
    echo To create an installer:
    echo   1. Download NSIS from: https://nsis.sourceforge.io/Download
    echo   2. Install NSIS
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

REM Create output directory for installer
if not exist installer_output mkdir installer_output

REM Build installer with NSIS
"%NSIS_PATH%" TheArtificer-Installer.nsi
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
