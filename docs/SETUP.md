# The Artificer - TTS Generator Setup Guide

## Prerequisites

- Python 3.8 or higher
- Windows 10/11 (for EXE build) or Linux with WSL
- At least 500MB free disk space for voice models

## Installation

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd the-artificer-tts-generator
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download Piper Voice Model

1. Visit the [Piper Voice Library](https://github.com/rhasspy/piper/releases)
2. Download a voice model (recommended: `en_US-lessac-medium`)
3. Download both files:
   - `[voice-name].onnx`
   - `[voice-name].onnx.json`
4. Place both files in the `models/` directory

**Example:**
```bash
cd models/
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/voice_en_US_lessac_medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/voice_en_US_lessac_medium.onnx.json
```

### Step 4: Install Piper TTS

#### On Linux/WSL:
```bash
pip install piper-tts
```

#### On Windows:
Download the Piper executable from the releases page and add it to your PATH, or install via pip:
```bash
pip install piper-tts
```

## Running the Application

### Development Mode

```bash
python src/ttrpg_voice_lab.py
```

### Building Windows EXE

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller ttrpg_voice_lab.spec
```

3. Find the executable in:
```
dist/TTRPGVoiceLab/TTRPGVoiceLab.exe
```

4. **Important**: Copy the `models/` folder into the `dist/TTRPGVoiceLab/` directory before distributing.

## Troubleshooting

### "No Voice Model Found" Error
- Ensure you've downloaded both `.onnx` and `.onnx.json` files
- Verify files are in the `models/` directory
- Check that filenames match exactly

### Audio Not Playing
- Verify pygame is installed: `pip install pygame`
- Check your system audio settings
- Try running with administrator privileges (Windows)

### Piper Command Not Found
- Ensure piper-tts is installed: `pip install piper-tts`
- On Windows, you may need to download the standalone executable
- Add Piper to your system PATH

### Effects Not Working
- Verify pedalboard installation: `pip install pedalboard`
- On Linux, you may need: `sudo apt-get install libsndfile1`

### WSL GUI Issues
- Install WSLg: `wsl --update`
- Or use X11 forwarding with VcXsrv

## WSL/Windows Workflow

### Development in WSL
```bash
# In WSL terminal
cd /home/exit/dev/projects/the-artificer-tts-generator
python src/ttrpg_voice_lab.py
```

### Testing on Windows
```bash
# In Windows PowerShell
cd C:\path\to\project
python src\ttrpg_voice_lab.py
```

### Building EXE on Windows
```bash
# In Windows PowerShell
pyinstaller ttrpg_voice_lab.spec
```

## Voice Model Recommendations

### For Best Quality:
- `en_US-lessac-high` (larger file, best quality)
- `en_US-ljspeech-high`

### For Balanced Performance:
- `en_US-lessac-medium` (recommended)
- `en_US-amy-medium`

### For Speed:
- `en_US-lessac-low`
- `en_US-ryan-low`

## Next Steps

1. Load a voice preset from the sidebar
2. Enter your NPC dialogue in the text box
3. Adjust the effect sliders to customize the sound
4. Click "Preview" to hear the result
5. Click "Export WAV" to save for use in your video editor

## Additional Resources

- [Piper TTS Documentation](https://github.com/rhasspy/piper)
- [Pedalboard Documentation](https://github.com/spotify/pedalboard)
- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
