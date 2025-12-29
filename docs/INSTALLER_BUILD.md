# Building the Windows Installer

This guide explains how to build a professional Windows installer for The Artificer - TTS Voice Generator.

## Prerequisites

### 1. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install Inno Setup

Download and install Inno Setup (free):
- **Download**: https://jrsoftware.org/isdl.php
- **Version**: Inno Setup 6 (recommended)
- **Install to**: Default location (C:\Program Files (x86)\Inno Setup 6\)

### 3. Download Voice Model

Download these files from https://github.com/rhasspy/piper/releases/tag/v1.2.0:
- `en_US-lessac-medium.onnx`
- `en_US-lessac-medium.onnx.json`

Place both in the `models/` folder.

## Quick Build (Recommended)

### One Command: Build Everything

```powershell
.\build-installer.bat
```

This script will:
1. ✅ Build the EXE with PyInstaller
2. ✅ Copy all necessary files (models, docs)
3. ✅ Create the installer with Inno Setup
4. ✅ Output installer to `installer_output/`

**Output**: `installer_output/TheArtificer-TTS-Setup-1.0.0.exe`

## Manual Build Process

If you prefer step-by-step control:

### Step 1: Build EXE

```powershell
# Build the PyInstaller EXE
pyinstaller ttrpg_voice_lab.spec

# Copy models
xcopy models dist\TTRPGVoiceLab\models\ /E /I /Y

# Copy docs (optional but recommended)
xcopy docs dist\TTRPGVoiceLab\docs\ /E /I /Y

# Copy license and readme
copy LICENSE dist\TTRPGVoiceLab\
copy README.md dist\TTRPGVoiceLab\
```

### Step 2: Build Installer

Right-click `installer.iss` and select "Compile" in Inno Setup.

Or from command line:

```powershell
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Step 3: Find Your Installer

The installer will be created in:
```
installer_output/TheArtificer-TTS-Setup-1.0.0.exe
```

## What the Installer Does

When users run the installer:

1. **License Agreement** - Shows MIT license
2. **Installation Location** - Defaults to `C:\Program Files\The Artificer - TTS Voice Generator\`
3. **Start Menu Shortcuts** - Creates shortcuts in Start Menu
4. **Desktop Icon** - Optional (user can choose)
5. **File Installation** - Copies all files to installation directory
6. **Add/Remove Programs** - Registers for easy uninstallation
7. **Launch Option** - Can launch app after installation

## Customizing the Installer

Edit `installer.iss` to customize:

### Change Version Number

```iss
#define MyAppVersion "1.0.0"  ; Change this
```

### Change Publisher/Author

```iss
#define MyAppPublisher "Your Name"
```

### Add Custom Icon

1. Create or obtain a `.ico` file
2. Place it in the project root (e.g., `icon.ico`)
3. Update the script:

```iss
SetupIconFile=icon.ico
```

### Change Default Install Location

```iss
DefaultDirName={autopf}\YourFolderName
```

### Disable Desktop Icon by Default

```iss
Name: "desktopicon"; ...; Flags: unchecked  ; Already set
```

Or make it default:

```iss
Name: "desktopicon"; ...; ; Remove Flags: unchecked
```

## Testing the Installer

### Install the Application

1. Run the installer:
   ```powershell
   .\installer_output\TheArtificer-TTS-Setup-1.0.0.exe
   ```

2. Follow the installation wizard

3. Check that:
   - [ ] Start Menu shortcut works
   - [ ] Desktop icon appears (if selected)
   - [ ] Application launches correctly
   - [ ] All features work (preview, export)

### Test Uninstallation

1. Go to Windows Settings → Apps → Installed Apps
2. Find "The Artificer - TTS Voice Generator"
3. Click Uninstall
4. Verify all files are removed
5. Verify Start Menu shortcuts are removed

## Distribution

### For End Users (Recommended)

Distribute the installer EXE:
- **File**: `TheArtificer-TTS-Setup-1.0.0.exe`
- **Size**: ~50-100 MB (depending on model size)
- **Advantages**:
  - Professional installation experience
  - Easy to uninstall
  - Automatic Start Menu integration
  - Single file to download

### For Power Users (Alternative)

Distribute the portable version:
- **Folder**: Zip `dist/TTRPGVoiceLab/`
- **Size**: Same as installer
- **Advantages**:
  - No installation required
  - Can run from USB drive
  - No admin rights needed

## Troubleshooting

### "Inno Setup not found"

**Solution**: Install Inno Setup from https://jrsoftware.org/isdl.php

Make sure it's installed to the default location or update the path in `build-installer.bat`.

### "File not found" during installer build

**Solution**: Make sure you ran PyInstaller first:
```powershell
pyinstaller ttrpg_voice_lab.spec
```

The `dist/TTRPGVoiceLab/` folder must exist before building the installer.

### Installer builds but application doesn't work

**Solution**: Test the EXE directly first:
```powershell
cd dist\TTRPGVoiceLab
.\TTRPGVoiceLab.exe
```

If the portable EXE works but the installed version doesn't, check file permissions.

### "Access denied" during installation

**Solution**: Run the installer as Administrator (right-click → Run as administrator).

### Installer is too large

**Solution**:
- The voice model files are the largest component (~50MB)
- Consider distributing without models and have users download them
- Or offer multiple installers with different voice models

## Continuous Integration

For automated builds, you can use GitHub Actions:

```yaml
# .github/workflows/build.yml
name: Build Installer

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build EXE
        run: pyinstaller ttrpg_voice_lab.spec
      - name: Install Inno Setup
        run: choco install innosetup
      - name: Build Installer
        run: iscc installer.iss
      - name: Upload installer
        uses: actions/upload-artifact@v3
        with:
          name: installer
          path: installer_output/*.exe
```

## Version Management

When releasing a new version:

1. Update version in `installer.iss`:
   ```iss
   #define MyAppVersion "1.1.0"
   ```

2. Update version in `src/ttrpg_voice_lab.py` (add version display)

3. Update `CHANGELOG.md`

4. Build new installer:
   ```powershell
   .\build-installer.bat
   ```

5. Test the new installer

6. Tag the release:
   ```bash
   git tag v1.1.0
   git push --tags
   ```

## File Sizes Reference

Approximate sizes:

- **PyInstaller EXE bundle**: ~30-40 MB
- **Voice model**: ~50 MB
- **Total installer**: ~80-100 MB

## Comparison with Your Node.js Projects

| Task | Electron Apps | This Python App |
|------|---------------|-----------------|
| Build EXE | `npm run build` | `pyinstaller ttrpg_voice_lab.spec` |
| Build Installer | `npm run dist` or electron-builder | Inno Setup (ISCC) |
| Installer Tool | electron-builder, Squirrel | Inno Setup |
| Output | Setup.exe | Setup.exe ✅ Same result! |

The end result is the same: a professional Windows installer!

---

**Questions?** Check the main README.md or SETUP.md for additional help.
