#!/bin/bash
# Quick start script for The Artificer - TTS Voice Generator

echo "=== The Artificer - TTS Voice Generator ==="
echo ""

# Check if models exist
if [ ! -d "models" ] || [ -z "$(ls -A models/*.onnx 2>/dev/null)" ]; then
    echo "⚠ No voice models found!"
    echo ""
    read -p "Would you like to download a voice model now? (y/n): " download

    if [ "$download" = "y" ] || [ "$download" = "Y" ]; then
        ./download_models.sh
    else
        echo ""
        echo "Please download a voice model manually:"
        echo "Run: ./download_models.sh"
        echo "Or download from: https://github.com/rhasspy/piper/releases"
        exit 1
    fi
fi

echo ""
echo "Starting TTRPG Voice Lab..."
echo ""

# Run the application
python3 src/ttrpg_voice_lab.py
