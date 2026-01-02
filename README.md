# The Artificer - TTS Voice Generator

> A powerful desktop application for generating high-quality NPC voices for TTRPG content creators

![Status](https://img.shields.io/badge/status-beta-yellow)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-GPL%20v3-blue)

## Overview

The Artificer is a desktop application designed for TTRPG content creators to generate professional-quality NPC voices for pre-recorded sessions, actual plays, and video content. Using local, offline TTS generation combined with professional audio effects, you can create distinctive character voices without cloud dependencies or subscription fees.

### Key Features

- **🎭 Voice Presets**: Pre-configured profiles for Clockwork, Dragons, Ghosts, Demons, and more
- **🌍 Multi-Language**: Supports **Danish, German, Spanish, French, Japanese, and 30+ languages**! [See Guide](docs/MULTILANGUAGE_GUIDE.md)
- **🎚️ 10 Audio Controls**: Speech rate, pitch, distortion, filters, chorus, delay, and more
- **🔊 Preview System**: Instant playback to test your settings
- **💾 High-Quality Export**: Crystal-clear WAV files ready for video editing
- **🖥️ Offline Processing**: Runs completely locally with no internet required
- **⚡ Non-blocking UI**: Threaded generation keeps the interface responsive
- **🎨 Dark Mode Interface**: Professional customtkinter GUI

## Quick Start

### Windows (Recommended)

```powershell
# 1. Clone the repository
git clone https://github.com/BahneGork/the-artificer-tts-generator.git
cd the-artificer-tts-generator

# 2. Install Python packages
pip install -r requirements.txt

# 3. Download voice model (automatic)
python setup_voice_model.py

# 4. Run the app
python src\ttrpg_voice_lab.py
```

**See [SIMPLE_BUILD_GUIDE.md](SIMPLE_BUILD_GUIDE.md) for building the installer.**

### Linux/WSL

```bash
# Install dependencies
pip install -r requirements.txt

# Download voice model
./download_models.sh

# Run the application
python src/ttrpg_voice_lab.py
```

## Voice Presets

### Included Presets

1. **Clockwork** - Mechanical construct with metallic resonance
2. **Ancient Dragon** - Deep, slow voice with cavernous reverb and delay
3. **Ghostly Apparition** - Ethereal, otherworldly with heavy chorus and reverb
4. **Demon Lord** - Dark, distorted voice with heavy processing
5. **Goblin** - Fast, high-pitched, nasally creature voice
6. **Orc Warrior** - Gruff, aggressive voice with distortion
7. **Lich** - Ancient undead with hollow echo and chorus
8. **Fey Creature** - Magical, whimsical voice with shimmer
9. **Giant** - Enormous, very slow booming voice with low-pass filter
10. **Elemental (Fire)** - Crackling, intense voice with distortion
11. **Vampire** - Seductive, menacing voice with slight echo
12. **Construct Guardian** - Heavy mechanical voice with deep tone

### Full Audio Control (10 Sliders)

**Row 1:**
- **Speech Rate**: 0.5x to 2.0x (speed of talking)
- **Pitch Shift**: -12 to +12 semitones
- **Distortion**: 0 to 20 dB (grit and aggression)
- **Mechanical Frequency**: 0 to 200 Hz (ring modulator)
- **Volume Boost**: 0 to +12 dB

**Row 2:**
- **Echo Level**: 0% to 100% (reverb wetness)
- **Chorus Depth**: 0% to 100% (ethereal effect)
- **Delay Time**: 0 to 500ms (distinct echo)
- **Low-pass Filter**: 1000 to 8000 Hz (muffled/distant)
- **High-pass Filter**: 50 to 500 Hz (tinny/radio effect)

Every preset has unique combinations that make characters truly distinctive!

## Project Structure

```
the-artificer-tts-generator/
├── src/
│   └── ttrpg_voice_lab.py    # Main application
├── presets/
│   └── voice_presets.json     # Voice preset configurations
├── models/                     # Piper TTS voice models (.onnx files)
├── exports/                    # Default export location for WAV files
├── docs/
│   ├── SETUP.md               # Detailed setup instructions
│   └── USER_GUIDE.md          # Complete user guide
├── requirements.txt            # Python dependencies
├── ttrpg_voice_lab.spec       # PyInstaller spec for EXE build
├── download_models.sh         # Model download helper script
├── run.sh                     # Quick start script
├── CLAUDE.md                  # Project instructions for Claude Code
└── README.md                  # This file
```

## Technology Stack

- **GUI**: [customtkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern dark mode interface
- **TTS Engine**: [piper-tts](https://github.com/rhasspy/piper) - Fast, local, offline speech synthesis
- **Audio FX**: [pedalboard](https://github.com/spotify/pedalboard) - Spotify's professional audio effects library
- **Audio Processing**: [pydub](https://github.com/jiaaro/pydub) & [numpy](https://numpy.org/)
- **Playback**: [pygame](https://www.pygame.org/) - Preview audio playback

## Usage

### Basic Workflow

1. **Select a Preset**: Click a preset in the left sidebar (e.g., "Ancient Dragon")
2. **Enter Dialogue**: Type your NPC's dialogue in the text box
3. **Customize Effects**: Adjust the three sliders to fine-tune the voice
4. **Preview**: Click 🔊 Preview to hear the result
5. **Export**: Click 💾 Export WAV to save the final audio file

### Example Use Cases

- **Actual Play Videos**: Generate distinct voices for recurring NPCs
- **Podcast Production**: Create memorable character voices
- **TTRPG Prep**: Pre-record important NPC dialogue
- **Content Creation**: Add professional voice-overs to TTRPG content

## Building the Installer

### Simple 3-Step Process

1. **Install Prerequisites** (first time only)
   - Python 3.10+ from https://www.python.org/downloads/
   - Inno Setup from https://jrsoftware.org/isdl.php

2. **Setup** (first time only)
   ```powershell
   pip install -r requirements.txt
   python setup_voice_model.py
   ```

3. **Build**
   ```powershell
   .\build-installer.bat
   ```

**Output**: `installer_output/TheArtificer-TTS-Setup-1.0.0.exe`

**See [SIMPLE_BUILD_GUIDE.md](SIMPLE_BUILD_GUIDE.md) for complete instructions.**

### Alternative: Portable EXE (No Installer)

```powershell
.\build.bat
```

**Output**: `dist/TTRPGVoiceLab/TTRPGVoiceLab.exe`

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation, troubleshooting, and building
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage instructions and tips

## Why Local Processing?

Unlike cloud-based TTS services, The Artificer generates audio **digitally** rather than recording your system output. This means:

- ✅ No background noise or system sounds
- ✅ Consistent quality regardless of system performance
- ✅ No internet connection required
- ✅ No usage limits or API costs
- ✅ Complete privacy - your content never leaves your machine

## Technical Details

### Audio Processing Pipeline

1. **TTS Generation**: Piper generates base speech from text
2. **Pitch Shifting**: Tonal adjustments for character voice
3. **Ring Modulation**: Creates mechanical/robotic effects
4. **Distortion**: Adds aggression and grit
5. **Chorus**: Ethereal, layered sound effects
6. **Low-Pass Filtering**: Spectral quality for ghosts/spirits
7. **Reverb**: Spatial processing and echo

### Output Specifications

- **Format**: WAV (uncompressed)
- **Sample Rate**: 22050 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono

## Troubleshooting

### Common Issues

**"No Voice Model Found"**
- Run `./download_models.sh` to download a model
- Or manually download from [Piper releases](https://github.com/rhasspy/piper/releases)

**Audio Not Playing**
- Check system audio settings
- Verify pygame is installed: `pip install pygame`

**Piper Command Not Found**
- Install piper-tts: `pip install piper-tts`
- On Windows, you may need the standalone executable

See [docs/SETUP.md](docs/SETUP.md) for detailed troubleshooting.

## Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Additional voice presets
- [ ] Custom preset saving/loading
- [ ] Batch text processing
- [ ] Additional voice model support
- [ ] Real-time preview during editing
- [ ] MIDI controller integration

## License

Copyright © 2025 Michael (BahneGork)

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program in the [LICENSE](LICENSE) file. If not, see https://www.gnu.org/licenses/.

### Why GPL v3?

This application uses [Pedalboard](https://github.com/spotify/pedalboard) (GPL v3) and Piper's espeak-ng phonemizer (GPL), which require the entire application to be licensed under GPL v3 due to copyleft requirements.

### Commercial Use

✅ **You CAN sell this software commercially**
✅ **You CAN charge for distribution or support**
⚠️ **You MUST provide source code to recipients**
⚠️ **You MUST include GPL v3 license and attribution**

The GPL v3 license allows commercial use, but requires that recipients have access to the source code.

### Third-Party Licenses

This application uses the following open-source libraries:

- **Pedalboard** (Spotify AB) - GPL v3 ⚖️
- **Piper TTS** (Rhasspy) - MIT (with GPL espeak-ng)
- **CustomTkinter** (Tom Schimansky) - MIT
- **Pydub** - MIT
- **NumPy** - BSD 3-Clause
- **PyInstaller** - GPL v2 with exceptions
- **audioop-lts** - PSF License

See [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt) for complete license text and attribution.

### Voice Models

Voice models are downloaded separately from [HuggingFace](https://huggingface.co/rhasspy/piper-voices) and are **NOT** distributed with this application. Each voice model has its own license (typically CC0, CC BY 4.0, or MIT). Users should review individual voice model licenses before commercial use.

## Credits

Built with:
- [Piper TTS](https://github.com/rhasspy/piper) by Rhasspy
- [Pedalboard](https://github.com/spotify/pedalboard) by Spotify (GPL v3)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky

## Acknowledgments

Special thanks to the TTRPG content creator community and the open-source audio processing community.

---

**Created**: 2025-12-29
**Status**: Beta - Ready for testing
**Version**: 1.0.0

**Happy voice generation! May your NPCs sound legendary!** 🎭✨
