# NSIS Installer Build Guide

This project now uses **NSIS (Nullsoft Scriptable Install System)** for creating Windows installers.

## Why NSIS?

- ✅ **Truly free for commercial use** - No license purchase required, ever
- ✅ **zlib/libpng license** - No ethical grey area for commercial distribution
- ✅ **Professional quality** - Used by Firefox, VLC, WinAmp, and many major applications
- ✅ **Modern UI** - Clean, professional installer experience
- ✅ **Full-featured** - Everything Inno Setup offers

## One-Time Setup

### 1. Download NSIS

**Download from:** https://nsis.sourceforge.io/Download

**Recommended:** NSIS 3.10 or later

### 2. Install NSIS

1. Run the downloaded installer
2. Follow the installation wizard
3. Default installation location: `C:\Program Files (x86)\NSIS\`
4. No special configuration needed

**Installation size:** ~10 MB

## Building the Installer

### Simple Method (Recommended)

Just run the build script:

```cmd
build-installer-nsis.bat
```

This script will:
1. Check dependencies (PyInstaller)
2. Build the EXE with PyInstaller
3. Copy additional files (models, docs, source code)
4. Build the installer with NSIS
5. Output installer to `installer_output\`

### Manual Method

If you prefer to build manually:

```cmd
# 1. Build the EXE
python -m PyInstaller ttrpg_voice_lab.spec

# 2. Copy files (models, docs, source)
# See build-installer-nsis.bat for exact commands

# 3. Compile the NSIS installer
"C:\Program Files (x86)\NSIS\makensis.exe" TheArtificer-Installer.nsi
```

## Output Files

After building, you'll have:

**Portable EXE:**
- `dist\TTRPGVoiceLab\TTRPGVoiceLab.exe`
- Can be zipped and distributed as portable version

**Installer:**
- `installer_output\TheArtificer-TTS-Setup-1.0.0.exe`
- Full Windows installer with Start Menu shortcuts
- Proper Add/Remove Programs integration
- Desktop shortcut option

## Installer Features

The NSIS installer includes:

- ✅ Modern UI with GPL v3 license display
- ✅ Installation to Program Files
- ✅ Start Menu shortcuts (The Artificer + Uninstall)
- ✅ Optional desktop shortcut
- ✅ Complete uninstaller
- ✅ Add/Remove Programs integration
- ✅ Source code bundled for GPL compliance
- ✅ "Launch after install" option

## Customizing the Installer

Edit `TheArtificer-Installer.nsi` to customize:

**Application Info (Lines 9-18):**
```nsis
!define APPNAME "The Artificer - TTS Voice Generator"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
```

**URLs (Lines 14-16):**
```nsis
!define HELPURL "https://github.com/..."
!define UPDATEURL "https://github.com/..."
!define ABOUTURL "https://github.com/..."
```

**After editing, just recompile:**
```cmd
"C:\Program Files (x86)\NSIS\makensis.exe" TheArtificer-Installer.nsi
```

## Troubleshooting

### "NSIS not found" error

**Solution:** Install NSIS from https://nsis.sourceforge.io/Download

### Build script can't find makensis.exe

The script checks these locations:
- `C:\Program Files (x86)\NSIS\makensis.exe`
- `C:\Program Files\NSIS\makensis.exe`

If NSIS is installed elsewhere, edit `build-installer-nsis.bat` and update the path.

### Installer build fails

**Check:**
1. `dist\TTRPGVoiceLab\` folder exists with all files
2. `LICENSE` file exists in project root
3. No special characters in file paths
4. Run as Administrator if needed

## Comparing to Inno Setup

Both `installer.iss` (Inno Setup) and `TheArtificer-Installer.nsi` (NSIS) are included in this project.

**Use NSIS if:**
- You want zero licensing concerns for commercial use
- You prefer widely-used open source tools

**Use Inno Setup if:**
- You're already familiar with it
- You don't mind purchasing a license if selling commercially

Both produce identical installers with the same features.

## License

**NSIS License:** zlib/libpng
**Your App License:** GNU GPL v3

NSIS does not impose any licensing restrictions on installers you create. Your app remains GPL v3 licensed regardless of which installer tool you use.

## Resources

- **NSIS Website:** https://nsis.sourceforge.io/
- **NSIS Documentation:** https://nsis.sourceforge.io/Docs/
- **NSIS Examples:** `C:\Program Files (x86)\NSIS\Examples\`
- **Modern UI Documentation:** https://nsis.sourceforge.io/Docs/Modern%20UI%202/Readme.html

## Quick Command Reference

```cmd
# Full build (EXE + Installer)
build-installer-nsis.bat

# Just the portable EXE
build.bat

# Manual NSIS compile
makensis TheArtificer-Installer.nsi

# Check NSIS version
makensis /VERSION
```

---

**That's it!** NSIS setup is simple and gives you full control over your installer with zero licensing concerns.
