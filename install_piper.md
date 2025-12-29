# Installing Piper TTS (Windows)

Piper is a **standalone executable**, not a Python package.

## Quick Install

### Option 1: Download and Add to Project (Easiest)

1. **Download Piper**:
   - Go to: https://github.com/rhasspy/piper/releases/latest
   - Download: `piper_windows_amd64.zip`
   - Extract the zip file

2. **Copy to Project**:
   ```powershell
   # Copy piper.exe to your project folder
   copy path\to\extracted\piper.exe W:\GitHub\the-artificer-tts-generator\
   ```

3. **Done!** The app will find piper.exe in the current directory.

### Option 2: Add to System PATH

1. **Download Piper** (same as above)

2. **Create a folder**:
   ```powershell
   mkdir C:\Tools\piper
   copy piper.exe C:\Tools\piper\
   ```

3. **Add to PATH**:
   - Windows Search → "Environment Variables"
   - Edit "Path" variable
   - Add: `C:\Tools\piper`
   - Click OK

4. **Verify**:
   ```powershell
   piper --version
   ```

## Testing

Once installed, test it:

```powershell
# Should show help/version info
piper --help
```

## For the Build

When building the installer, make sure `piper.exe` is in the project folder or system PATH so PyInstaller can find it.
