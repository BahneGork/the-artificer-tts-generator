# Changelog

All notable changes to The Artificer - TTS Voice Generator will be documented in this file.

## [1.1.0] - 2025-01-05

### Added
- **Discord Integration**: Send voices directly to Discord voice chat
  - "Send to Discord" button with automatic audio device switching
  - VB-CABLE virtual audio cable support
  - Cancel & Restore Mic button for immediate stop
  - Emergency Reset Audio Device button
  - Comprehensive HTML setup guide (vb-cable-setup.html)
  - Discord Setup Guide button in sidebar
- **Multi-Language Support**: 30+ languages including:
  - Spanish, French, German, Japanese, Italian, Portuguese, Russian, and more
  - Voice downloader dialog to browse 400+ available voices
  - Language-specific voice catalog with samples
  - Multi-language documentation guide
- **Enhanced Audio Controls**: Expanded from 3 to 11 sliders
  - Speech Rate (0.5x to 2.0x) - NEW
  - Sentence Pause (0s to 2.0s) - NEW (verified Piper feature)
  - Distortion (0 to 20 dB) - NEW
  - Volume Boost (0 to +12 dB) - NEW
  - Chorus Depth (0% to 100%) - NEW
  - Delay Time (0 to 500ms) - NEW
  - Low-pass Filter (1000 to 8000 Hz) - NEW
  - High-pass Filter (50 to 500 Hz) - NEW
  - Pitch Shift (-12 to +12 semitones) - ENHANCED
  - Mechanical Frequency (0 to 200 Hz) - RETAINED
  - Echo Level (0% to 100%) - RETAINED
- **7 New Voice Presets**: Total 12 presets
  - Orc Warrior - Gruff, aggressive voice
  - Lich - Ancient undead with hollow echo
  - Fey Creature - Magical, whimsical voice
  - Giant - Enormous, slow booming voice
  - Elemental (Fire) - Crackling, intense voice
  - Vampire - Seductive, menacing voice
  - Construct Guardian - Heavy mechanical voice
  - Clockwork (renamed from Warforged) - Updated preset
- **GPL v3 Compliance**: Full open source compliance
  - Complete GNU GPL v3 license
  - Source code bundled with all distributions
  - THIRD_PARTY_LICENSES.txt with dependency attribution
  - About/License dialog in app
  - SOURCE_README.txt for recipients
- **NSIS Installer**: Alternative to Inno Setup
  - Truly free for commercial use (zlib/libpng license)
  - Professional Modern UI installer
  - Complete build automation (build-installer-nsis.bat)
  - NSIS_BUILD_GUIDE.md documentation
- **Comprehensive Documentation**:
  - TEXT_CONTROL_GUIDE.md - What works with Piper TTS
  - MULTILANGUAGE_GUIDE.md - Language support guide
  - Completely rewritten USER_GUIDE.md
  - Updated README with all features
  - VB-CABLE HTML setup wizard

### Changed
- **Window Size**: Increased from 1280x700 to 1280x1280 for Discord buttons
- **License**: Changed from MIT to GNU GPL v3
- **Preset Name**: "Warforged" renamed to "Clockwork"
- **Models Path**: Fixed to correctly find models in installed version
- **Audio Processing Pipeline**: Expanded with 8 additional effect stages
- **UI Layout**: Reorganized into 3 rows (Speech/Timing/Effects)

### Fixed
- Models directory not found in installed applications
- Window too small to display all UI elements with new features
- Improved path handling for frozen executables

### Technical Details
- Sample rate: 22050 Hz (unchanged)
- Bit depth: 16-bit (unchanged)
- Channels: Mono (unchanged)
- Output format: WAV uncompressed (unchanged)
- New dependencies: pycaw, comtypes (Discord integration)
- Enhanced Pedalboard effects chain with 12 processing stages

### Documentation
- TEXT_CONTROL_GUIDE.md explains Piper TTS text limitations
- MULTILANGUAGE_GUIDE.md covers 30+ language support
- USER_GUIDE.md completely rewritten for v1.1.0
- NSIS_BUILD_GUIDE.md for alternative installer
- VB-CABLE setup wizard (HTML) for Discord integration
- Updated README with all current features

## [1.0.0] - 2024-12-29

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
- Inno Setup installer script
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
- ✅ Custom preset saving/loading (v1.1.0)
- Batch text processing
- Additional voice models support (✅ v1.1.0 - 400+ models)
- Real-time preview during editing
- Effect preset library
- MIDI controller support
