#!/bin/bash
# Script to download Piper TTS voice models

echo "=== Piper Voice Model Downloader ==="
echo ""

# Create models directory if it doesn't exist
mkdir -p models

echo "Available voice models:"
echo "1. en_US-lessac-medium (Recommended - Good quality, balanced performance)"
echo "2. en_US-lessac-high (Best quality, larger file)"
echo "3. en_US-lessac-low (Fastest, lower quality)"
echo "4. en_US-amy-medium (Alternative female voice)"
echo "5. en_US-ryan-medium (Alternative male voice)"
echo ""

read -p "Select a model (1-5): " choice

case $choice in
    1)
        MODEL="en_US-lessac-medium"
        ;;
    2)
        MODEL="en_US-lessac-high"
        ;;
    3)
        MODEL="en_US-lessac-low"
        ;;
    4)
        MODEL="en_US-amy-medium"
        ;;
    5)
        MODEL="en_US-ryan-medium"
        ;;
    *)
        echo "Invalid selection. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Downloading $MODEL..."
echo ""

BASE_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0"

# Download .onnx file
echo "Downloading ${MODEL}.onnx..."
wget -O "models/${MODEL}.onnx" "${BASE_URL}/${MODEL}.onnx"

# Download .onnx.json file
echo "Downloading ${MODEL}.onnx.json..."
wget -O "models/${MODEL}.onnx.json" "${BASE_URL}/${MODEL}.onnx.json"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Model downloaded successfully to models/${MODEL}.onnx"
    echo "✓ You can now run the application!"
else
    echo ""
    echo "✗ Download failed. Please check your internet connection and try again."
    exit 1
fi
