# Windows Build Workflow - Quick Reference

## 🚀 Complete Workflow (WSL → Windows)

### On WSL (Development)

```bash
# Make changes to code
git add .
git commit -m "Your changes"
git push
```

### On Windows (Build & Test)

```powershell
# Pull latest code
git pull

# First time only: Install dependencies
pip install -r requirements.txt

# First time only: Download voice model
# Visit: https://github.com/rhasspy/piper/releases/tag/v1.2.0
# Download: en_US-lessac-medium.onnx and .onnx.json
# Place in: models/ folder

# First time only: Install Inno Setup
# Download from: https://jrsoftware.org/isdl.php
# Install to default location

# Build installer (one command!)
.\build-installer.bat
```

**Output**: `installer_output/TheArtificer-TTS-Setup-1.0.0.exe`

## 📋 Comparison with Your Node.js Projects

| Step | Your Electron Apps | This Python App |
|------|-------------------|-----------------|
| **Develop** | WSL | WSL ✅ Same |
| **Push** | `git push` | `git push` ✅ Same |
| **Pull** | `git pull` | `git pull` ✅ Same |
| **Install deps** | `npm install` | `pip install -r requirements.txt` |
| **Build** | `npm run build` | `.\build-installer.bat` ✅ Similar! |
| **Output** | `dist/Setup.exe` | `installer_output/TheArtificer-TTS-Setup-1.0.0.exe` |
| **Install** | Run Setup.exe | Run Setup.exe ✅ Same! |

## 🎯 What You Get

### Professional Windows Installer

- ✅ Installation wizard (Next, Next, Finish)
- ✅ Installs to Program Files
- ✅ Start Menu shortcuts
- ✅ Desktop icon (optional)
- ✅ Add/Remove Programs entry
- ✅ Proper uninstaller

### Same Experience as Your Other Apps!

The installer behaves exactly like your Electron apps:
- Users download one `.exe` file
- Double-click to install
- Shows up in Start Menu
- Can be uninstalled properly

## 🔧 Build Options

### Option 1: Full Installer (Recommended)

```powershell
.\build-installer.bat
```

Creates: `TheArtificer-TTS-Setup-1.0.0.exe` (~80-100 MB)

### Option 2: Portable EXE

```powershell
.\build.bat
```

Creates: `dist/TTRPGVoiceLab/` folder (portable, no install needed)

## 🧪 Testing

### Test the Installer

```powershell
# Run the installer
.\installer_output\TheArtificer-TTS-Setup-1.0.0.exe

# Install it
# Launch from Start Menu
# Test the app
# Uninstall from Windows Settings
```

### Test the App Directly (Before Building)

```powershell
# Run Python app directly
python src\ttrpg_voice_lab.py
```

## 📦 Distribution

Share the installer with users:

1. **Upload to GitHub Releases**:
   ```bash
   gh release create v1.0.0 installer_output/TheArtificer-TTS-Setup-1.0.0.exe
   ```

2. **Or upload to file hosting**:
   - Google Drive
   - Dropbox
   - Your website

3. **Users download and install**:
   - One click to download
   - Double-click to install
   - Done!

## 🔄 Typical Development Cycle

```powershell
# 1. Pull latest code from WSL
git pull

# 2. Make Windows-specific fixes (if needed)
code src\ttrpg_voice_lab.py

# 3. Test locally
python src\ttrpg_voice_lab.py

# 4. Build installer
.\build-installer.bat

# 5. Test installer
.\installer_output\TheArtificer-TTS-Setup-1.0.0.exe

# 6. Distribute or push changes back to WSL
```

## ⚡ Quick Commands Cheat Sheet

```powershell
# Test app
python src\ttrpg_voice_lab.py

# Build portable EXE
.\build.bat

# Build installer
.\build-installer.bat

# Clean build artifacts
rmdir /s /q build dist installer_output
```

## 🛠️ One-Time Setup

These steps only need to be done once:

1. **Install Python** (3.8+)
2. **Install Inno Setup** (https://jrsoftware.org/isdl.php)
3. **Install project dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Download voice model** (see WINDOWS_BUILD_INSTRUCTIONS.md)

After that, it's just:
```powershell
git pull
.\build-installer.bat
```

## 📁 Output Locations

After building:

```
project/
├── dist/
│   └── TTRPGVoiceLab/
│       └── TTRPGVoiceLab.exe    ← Portable EXE
├── installer_output/
│   └── TheArtificer-TTS-Setup-1.0.0.exe    ← INSTALLER (distribute this!)
└── build/                        ← Temp files (can delete)
```

## 🎓 Learning Resources

- **Inno Setup**: https://jrsoftware.org/ishelp/
- **PyInstaller**: https://pyinstaller.org/en/stable/
- **Python on Windows**: https://docs.python.org/3/using/windows.html

---

**TL;DR**: After first-time setup, it's just `git pull` → `.\build-installer.bat` → distribute the Setup.exe!
