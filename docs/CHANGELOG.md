# Changelog

All notable changes to The Artificer - TTS Voice Generator will be documented in this file.

## [1.0.0] - 2025-12-29

### Added
- Initial release of The Artificer - TTS Voice Generator
- CustomTkinter-based dark mode GUI
- Dual-pane layout with preset sidebar and main control area
- 5 pre-configured voice presets:
  - Warforged (mechanical construct)
  - Ancient Dragon (deep, resonant)
  - Ghostly Apparition (ethereal)
  - Demon Lord (dark, distorted)
  - Goblin (high-pitched creature)
- Three dynamic effect sliders:
  - Pitch Shift (-12 to +12 semitones)
  - Mechanical Frequency (0-200 Hz ring modulation)
  - Echo Level (0-100% reverb)
- Piper TTS integration for local, offline speech generation
- Pedalboard audio effects processing:
  - Pitch shifting
  - Ring modulation
  - Distortion
  - Chorus
  - Low-pass filtering
  - Reverb
- Preview system with pygame.mixer playback
- High-quality WAV export functionality
- Threading for non-blocking TTS generation
- Automatic temporary file cleanup
- JSON-based preset system
- PyInstaller spec file for Windows EXE builds
- Comprehensive documentation:
  - Setup guide
  - User guide
  - README with quick start
- Helper scripts:
  - download_models.sh for easy model installation
  - run.sh for Linux/WSL quick start
  - run.bat for Windows quick start

### Technical Details
- Sample rate: 22050 Hz
- Bit depth: 16-bit
- Channels: Mono
- Output format: WAV (uncompressed)

### Known Issues
- Piper must be installed separately and accessible in PATH
- Voice models must be downloaded manually on first run
- WSL users may need WSLg or X11 forwarding for GUI

### Future Enhancements
- Custom preset saving/loading
- Batch text processing
- Additional voice models support
- Real-time preview during editing
- Effect preset library
- MIDI controller support
