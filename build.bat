@echo off
REM Build script for The Artificer - TTS Voice Generator
REM Similar to "npm run build" for Node.js projects

echo ========================================
echo The Artificer - TTS Voice Generator
echo Build Script for Windows
echo ========================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    echo.
)

REM Clean previous build
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist\TTRPGVoiceLab rmdir /s /q dist\TTRPGVoiceLab
echo.

REM Run PyInstaller
echo Building executable...
python -m PyInstaller ttrpg_voice_lab.spec
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

REM Copy source code for GPL compliance
echo Bundling source code for GPL compliance...
if not exist dist\TTRPGVoiceLab\source mkdir dist\TTRPGVoiceLab\source

REM Copy Python source files
xcopy src dist\TTRPGVoiceLab\source\src\ /E /I /Y >nul

REM Copy preset configurations
xcopy presets dist\TTRPGVoiceLab\source\presets\ /E /I /Y >nul

REM Copy license and documentation
copy LICENSE dist\TTRPGVoiceLab\source\ >nul 2>&1
copy THIRD_PARTY_LICENSES.txt dist\TTRPGVoiceLab\source\ >nul 2>&1
copy README.md dist\TTRPGVoiceLab\source\ >nul 2>&1
copy SOURCE_README.txt dist\TTRPGVoiceLab\source\ >nul 2>&1
copy requirements.txt dist\TTRPGVoiceLab\source\ >nul 2>&1

REM Copy build scripts
copy build.bat dist\TTRPGVoiceLab\source\ >nul 2>&1
copy ttrpg_voice_lab.spec dist\TTRPGVoiceLab\source\ >nul 2>&1

REM Copy top-level license files for easy access
copy LICENSE dist\TTRPGVoiceLab\ >nul 2>&1
copy THIRD_PARTY_LICENSES.txt dist\TTRPGVoiceLab\ >nul 2>&1
copy SOURCE_README.txt dist\TTRPGVoiceLab\ >nul 2>&1

echo Source code bundled successfully.
echo.

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
