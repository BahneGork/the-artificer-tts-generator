# Simple Build Guide - 3 Steps

## First Time Setup (5 minutes)

### Step 1: Install Prerequisites

Download and install these two programs:

1. **Python 3.10+**
   - Download: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **Inno Setup** (for creating the installer)
   - Download: https://jrsoftware.org/isdl.php
   - Just click Next, Next, Install

### Step 2: Setup Project

Open PowerShell in the project folder and run:

```powershell
# Install Python packages
pip install -r requirements.txt

# Download voice model automatically
python setup_voice_model.py
```

That's it! First-time setup complete.

### Step 3: Build

```powershell
# Build everything (EXE + Installer)
.\build-installer.bat
```

**Done!** Your installer is in: `installer_output/TheArtificer-TTS-Setup-1.0.0.exe`

---

## Every Time After That

```powershell
# Pull latest code
git pull

# Build
.\build-installer.bat
```

---

## Quick Test (Without Building)

Want to test the app without building an installer?

```powershell
python src\ttrpg_voice_lab.py
```

---

## Troubleshooting

### "python not found"
Install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH"

### "Inno Setup not found"
Install from https://jrsoftware.org/isdl.php
Or just run `.\build.bat` for portable EXE (no installer needed)

### Voice model download fails
Download manually:
1. Go to: https://github.com/rhasspy/piper/releases/tag/v1.2.0
2. Download `en_US-lessac-medium.onnx` and `en_US-lessac-medium.onnx.json`
3. Place both files in the `models/` folder

---

## Summary

**First time:**
1. Install Python + Inno Setup (5 min)
2. Run `pip install -r requirements.txt` (2 min)
3. Run `python setup_voice_model.py` (1 min)
4. Run `.\build-installer.bat` (2 min)

**Every time after:**
1. `git pull`
2. `.\build-installer.bat`

That's it!
