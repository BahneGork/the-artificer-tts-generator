@echo off
REM Quick start script for The Artificer - TTS Voice Generator (Windows)

echo === The Artificer - TTS Voice Generator ===
echo.

REM Check if models directory exists and has files
if not exist "models\*.onnx" (
    echo WARNING: No voice models found!
    echo.
    echo Please download a voice model:
    echo 1. Visit: https://github.com/rhasspy/piper/releases
    echo 2. Download a voice model e.g., en_US-lessac-medium.onnx
    echo 3. Also download the .onnx.json file
    echo 4. Place both files in the 'models' folder
    echo.
    pause
    exit /b 1
)

echo Starting TTRPG Voice Lab...
echo.

REM Run the application
python src\ttrpg_voice_lab.py

pause
