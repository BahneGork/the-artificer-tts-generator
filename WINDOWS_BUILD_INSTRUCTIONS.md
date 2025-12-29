# Windows Build & Test Instructions

## After Pulling from WSL

### Step 1: Install Dependencies

Open PowerShell or Command Prompt in the project directory:

```powershell
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Piper Voice Model

You have two options:

#### Option A: Manual Download (Recommended for Windows)
1. Visit: https://github.com/rhasspy/piper/releases/tag/v1.2.0
2. Download these two files:
   - `en_US-lessac-medium.onnx`
   - `en_US-lessac-medium.onnx.json`
3. Place both files in the `models/` folder

#### Option B: Use wget (if installed)
```powershell
cd models
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json
```

### Step 3: Install Piper TTS

```powershell
pip install piper-tts
```

**Note**: If `piper-tts` doesn't install correctly via pip on Windows, download the standalone executable from the Piper releases page and add it to your PATH.

### Step 4: Test the Application

```powershell
# Run the application
python src\ttrpg_voice_lab.py

# Or use the batch script
.\run.bat
```

### Step 5: Test Basic Functionality

1. **GUI Opens**: Verify the CustomTkinter interface loads
2. **Select Preset**: Click "Warforged" in the sidebar
3. **Enter Text**: Type "Greetings, adventurer" in the text box
4. **Preview**: Click the 🔊 Preview button
   - Should take 2-5 seconds to generate
   - Audio should play through speakers
5. **Export**: Click 💾 Export WAV
   - Choose save location
   - Verify WAV file is created

### Step 6: Build Windows EXE

```powershell
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller ttrpg_voice_lab.spec

# Find output in: dist\TTRPGVoiceLab\
```

**IMPORTANT**: After building, copy the `models\` folder into `dist\TTRPGVoiceLab\` so the EXE can find the voice models.

```powershell
# Copy models to distribution folder
xcopy models dist\TTRPGVoiceLab\models\ /E /I /Y
```

### Step 7: Test the EXE

```powershell
cd dist\TTRPGVoiceLab
.\TTRPGVoiceLab.exe
```

## Common Windows Issues

### Issue: "piper command not found"

**Solution**: Download standalone Piper executable:
1. Go to https://github.com/rhasspy/piper/releases
2. Download `piper_windows_amd64.zip`
3. Extract `piper.exe`
4. Add to PATH or place in project directory

### Issue: "No module named 'pedalboard'"

**Solution**: Ensure you're in the virtual environment:
```powershell
.\venv\Scripts\activate
pip install pedalboard
```

### Issue: Audio not playing

**Solutions**:
- Check Windows audio settings
- Verify pygame is installed: `pip install pygame`
- Try running as administrator
- Check that speakers/headphones are connected

### Issue: GUI looks wrong/broken

**Solutions**:
- Update customtkinter: `pip install --upgrade customtkinter`
- Ensure you have the latest Python (3.8+)
- Try running with different DPI settings

### Issue: PyInstaller build fails

**Solutions**:
- Ensure all dependencies are installed
- Try: `pip install --upgrade pyinstaller`
- Check that the spec file path is correct
- Run from project root directory

## Performance Expectations

- **First TTS Generation**: 3-8 seconds (model loading)
- **Subsequent Generations**: 2-5 seconds
- **Preview Playback**: Instant after generation
- **Export**: Same time as preview generation

## Testing Checklist

- [ ] GUI opens without errors
- [ ] All 5 presets load correctly
- [ ] Sliders move and update labels
- [ ] Preview button generates and plays audio
- [ ] Export button saves WAV file
- [ ] WAV file plays in Windows Media Player
- [ ] No error popups or crashes
- [ ] Temporary files are cleaned up
- [ ] EXE builds successfully
- [ ] EXE runs without Python installed

## Next Steps After Testing

1. Report any issues or bugs
2. Test different voice models
3. Try creating custom voice combinations
4. Test with longer dialogue passages
5. Integrate exported audio with video editor

## Notes

- The application generates audio digitally, not by recording system audio
- Longer text = longer processing time (this is normal)
- WAV files are uncompressed for maximum quality
- The UI stays responsive during generation thanks to threading

---

**Questions or Issues?** Check docs/SETUP.md for detailed troubleshooting.
