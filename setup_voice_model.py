#!/usr/bin/env python3
"""
Voice Model Setup Script
Downloads the recommended Piper TTS voice model automatically.
"""

import os
import sys
import urllib.request
from pathlib import Path


def download_file(url, destination, description):
    """Download a file with progress indicator"""
    print(f"Downloading {description}...")

    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(downloaded * 100 / total_size, 100)
            sys.stdout.write(f"\r  Progress: {percent:.1f}%")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, destination, progress_hook)
        print()  # New line after progress
        return True
    except Exception as e:
        print(f"\n  Error: {e}")
        return False


def main():
    print("=" * 50)
    print("Voice Model Setup for The Artificer TTS Generator")
    print("=" * 50)
    print()

    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    # Check if model already exists
    model_file = models_dir / "en_US-lessac-medium.onnx"
    config_file = models_dir / "en_US-lessac-medium.onnx.json"

    if model_file.exists() and config_file.exists():
        print("✓ Voice model already downloaded!")
        print(f"  Location: {model_file}")
        print()
        print("Setup complete. You can now run:")
        print("  .\\build-installer.bat")
        return 0

    print("This will download the recommended voice model:")
    print("  Model: en_US-lessac-medium")
    print("  Size: ~50 MB")
    print("  Quality: Medium (good balance of quality and speed)")
    print()

    # Base URL for Piper voice models
    # Note: Voice models are in separate releases from the main Piper releases
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium"

    # Download .onnx file
    print("Step 1/2: Downloading voice model...")
    success = download_file(
        f"{base_url}/en_US-lessac-medium.onnx",
        model_file,
        "voice model (.onnx)"
    )

    if not success:
        print()
        print("Download failed. Please download manually:")
        print("  1. Visit: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/lessac/medium")
        print("  2. Download: en_US-lessac-medium.onnx")
        print("  3. Download: en_US-lessac-medium.onnx.json")
        print(f"  4. Place both files in: {models_dir}")
        return 1

    # Download .onnx.json file
    print()
    print("Step 2/2: Downloading model configuration...")
    success = download_file(
        f"{base_url}/en_US-lessac-medium.onnx.json",
        config_file,
        "model config (.onnx.json)"
    )

    if not success:
        print()
        print("Download failed. Please download manually:")
        print("  1. Visit: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/lessac/medium")
        print("  2. Download: en_US-lessac-medium.onnx.json")
        print(f"  3. Place in: {models_dir}")
        return 1

    print()
    print("=" * 50)
    print("✓ Voice model setup complete!")
    print("=" * 50)
    print()
    print(f"Model installed to: {model_file}")
    print()
    print("You can now build the application:")
    print("  .\\build-installer.bat    (Creates installer)")
    print("  .\\build.bat              (Creates portable EXE)")
    print()
    print("Or test it directly:")
    print("  python src\\ttrpg_voice_lab.py")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
