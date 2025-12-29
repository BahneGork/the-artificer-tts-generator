@echo off
REM Build script for The Artificer - TTS Voice Generator
REM Similar to "npm run build" for Node.js projects

echo ========================================
echo The Artificer - TTS Voice Generator
echo Build Script for Windows
echo ========================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

REM Clean previous build
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist\TTRPGVoiceLab rmdir /s /q dist\TTRPGVoiceLab
echo.

REM Run PyInstaller
echo Building executable...
pyinstaller ttrpg_voice_lab.spec
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

REM Copy models folder
echo Copying voice models to distribution...
if exist models (
    xcopy models dist\TTRPGVoiceLab\models\ /E /I /Y >nul
    echo Models copied successfully.
) else (
    echo WARNING: No models folder found!
    echo Please download a voice model and place it in the models/ folder.
)
echo.

REM Copy presets (should be auto-included but let's be sure)
if exist presets (
    xcopy presets dist\TTRPGVoiceLab\presets\ /E /I /Y >nul
)

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location:
echo   dist\TTRPGVoiceLab\TTRPGVoiceLab.exe
echo.
echo To test the application:
echo   cd dist\TTRPGVoiceLab
echo   TTRPGVoiceLab.exe
echo.
echo To distribute:
echo   Zip the entire 'dist\TTRPGVoiceLab' folder
echo ========================================
echo.
pause
