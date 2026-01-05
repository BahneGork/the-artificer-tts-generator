# The Artificer - TTS Voice Generator User Guide

## Overview

The Artificer is a desktop application designed for TTRPG content creators to generate high-quality NPC voices for pre-recorded sessions, actual plays, and video content. With 12 voice presets, 11 audio controls, multi-language support, and Discord integration, you can create distinctive character voices without cloud dependencies or subscription fees.

## Key Features

- **🎭 12 Voice Presets** - From Clockwork constructs to Ancient Dragons
- **🎚️ 11 Audio Controls** - Complete creative control over every voice
- **🌍 30+ Languages** - Danish, German, Spanish, French, Japanese, and more
- **🎙️ Discord Integration** - Send voices directly to Discord voice chat
- **🔊 Preview & Export** - Test voices instantly, export high-quality WAV files
- **📥 Voice Downloader** - Browse and download 400+ voice models
- **🖥️ Offline** - Runs completely locally, no internet required

## Getting Started

### Interface Overview

**Left Sidebar:**
- Voice preset buttons (12 presets)
- Download Voice Models button
- Emergency Reset Audio button (Discord feature)
- Discord Setup Guide button
- About/License button

**Main Area:**
- Text input box (type your NPC dialogue here)
- 11 audio control sliders (3 rows)
- Preview and Export buttons
- Send to Discord button
- Status label (shows generation progress)

**Right Sidebar:**
- Voice model selector (choose language/voice)
- Voice description
- Preset information

## Using the Application

### Basic Workflow

#### Step 1: Select a Voice Model

Click the **voice dropdown** in the right sidebar to select a language and voice:
- English (US) - lessac (medium) - Default
- Spanish, French, German, Japanese, etc.
- Download more voices using the "Download Voice Models" button

**See [MULTILANGUAGE_GUIDE.md](MULTILANGUAGE_GUIDE.md) for language options.**

#### Step 2: Choose a Preset (Optional)

Click a preset button in the left sidebar to load pre-configured settings:

1. **Clockwork** - Mechanical construct with metallic resonance
2. **Ancient Dragon** - Deep, slow voice with cavernous reverb
3. **Ghostly Apparition** - Ethereal, otherworldly with heavy effects
4. **Demon Lord** - Dark, distorted voice with heavy processing
5. **Goblin** - Fast, high-pitched, nasally creature voice
6. **Orc Warrior** - Gruff, aggressive with distortion
7. **Lich** - Ancient undead with hollow echo and chorus
8. **Fey Creature** - Magical, whimsical with shimmer
9. **Giant** - Enormous, slow booming voice
10. **Elemental (Fire)** - Crackling, intense with distortion
11. **Vampire** - Seductive, menacing with slight echo
12. **Construct Guardian** - Heavy mechanical with deep tone

**Or start from scratch** by adjusting sliders manually.

#### Step 3: Enter Dialogue

Type your NPC's dialogue in the text box. The application works best with:
- Natural, conversational text
- Proper punctuation (periods, commas)
- Sentences or short paragraphs

**Important:** See [TEXT_CONTROL_GUIDE.md](TEXT_CONTROL_GUIDE.md) for what text formatting actually works with Piper TTS.

**Text Tips:**
- ✅ "Stop. Listen carefully." - Works naturally
- ❌ "Stop... ... listen." - Doesn't create extra pauses
- ✅ Use Sentence Pause slider instead of punctuation tricks

#### Step 4: Adjust Audio Controls

Use the 11 sliders to customize the voice:

**Row 1 - Speech Controls:**

1. **Speech Rate** (0.5x to 2.0x)
   - Controls speaking speed
   - 0.5x = Very slow, dramatic
   - 1.0x = Normal speed
   - 2.0x = Very fast, frantic

2. **Pitch Shift** (-12 to +12 semitones)
   - -12 to -6 = Deep, menacing voices
   - 0 = Natural pitch
   - +6 to +12 = High-pitched creatures

3. **Distortion** (0 to 20 dB)
   - Adds grit and aggression
   - 0 dB = Clean
   - 10 dB = Moderate grit
   - 20 dB = Heavy distortion

4. **Mechanical** (0 to 200 Hz)
   - Ring modulator effect
   - 0 Hz = Off
   - 50 Hz = Robotic quality
   - 100+ Hz = Heavy mechanical

5. **Volume** (0 to +12 dB)
   - Boost output volume
   - 0 dB = Quiet
   - +3 dB = Normal (default)
   - +12 dB = Very loud

**Row 2 - Speech Timing:**

6. **Sentence Pause** (0s to 2.0s)
   - Controls pause between sentences
   - 0s = No pause, rapid speech
   - 0.75s = Natural (default)
   - 2.0s = Dramatic, slow pacing

**Row 3 - Audio Effects:**

7. **Echo Level** (0% to 100%)
   - Reverb/echo amount
   - 0% = Dry, intimate
   - 30% = Natural room
   - 100% = Cavernous, otherworldly

8. **Chorus Depth** (0% to 100%)
   - Ethereal, layered effect
   - 0% = Off
   - 50% = Moderate shimmer
   - 100% = Heavy otherworldly effect

9. **Delay Time** (0 to 500ms)
   - Distinct echo delay
   - 0ms = Off
   - 200ms = Moderate echo
   - 500ms = Long echo tail

10. **Low-pass Filter** (1000 to 8000 Hz)
    - Removes high frequencies
    - 1000 Hz = Very muffled
    - 8000 Hz = Off (default)
    - Creates distant, underwater sound

11. **High-pass Filter** (50 to 500 Hz)
    - Removes low frequencies
    - 50 Hz = Off (default)
    - 200 Hz = Tinny, radio effect
    - 500 Hz = Extreme tinny sound

#### Step 5: Preview

Click **🔊 Preview** to:
1. Generate TTS audio (2-10 seconds)
2. Apply all effects
3. Play through your speakers

The preview button disables during generation to prevent overlapping processes.

#### Step 6: Export

Click **💾 Export WAV** to:
1. Choose save location
2. Generate final audio
3. Save as high-quality .WAV file

**Export Quality:**
- Sample Rate: 22050 Hz
- Bit Depth: 16-bit
- Channels: Mono
- Format: WAV (uncompressed)

The exported file is a **digital render**, not a recording - crystal clear with no background noise.

## Discord Integration

### Send Voices to Discord

The **🎙️ Send to Discord** button lets you play NPC voices directly into Discord voice chat during live TTRPG sessions.

**Requirements:**
- VB-CABLE virtual audio cable (free)
- Discord input set to "Default"

**How to Use:**

1. Click **📖 Discord Setup Guide** in the sidebar for complete setup instructions
2. Join a Discord voice channel
3. Type your NPC dialogue and adjust settings
4. Click **🎙️ Send to Discord**
5. The app automatically switches to virtual cable, plays audio, and restores your mic

**Controls:**
- **⏹️ Cancel & Restore Mic** - Stops playback immediately
- **🔧 Reset Audio Device** - Emergency mic restore if something goes wrong

**See [vb-cable-setup.html](vb-cable-setup.html) for detailed setup guide.**

## Multi-Language Support

The Artificer supports **30+ languages** including:
- 🇺🇸 English (US/UK)
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇯🇵 Japanese
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- And many more!

**To use different languages:**

1. Click **Download Voice Models** button
2. Browse available voices by language
3. Select voices to download
4. Click **Download Selected Voices**
5. Use the voice dropdown to select downloaded voices

**See [MULTILANGUAGE_GUIDE.md](MULTILANGUAGE_GUIDE.md) for complete language guide.**

## Advanced Techniques

### Creating Custom Voice Profiles

1. Start with a preset that's close to your vision
2. Adjust sliders to taste
3. Note your settings for future use
4. Consider creating a preset file (see QUICK_REFERENCE.md)

### Effect Combinations

**Undead/Spectral:**
- Speech Rate: 0.8x (slower)
- Pitch: 0 to -2
- Sentence Pause: 1.2s (dramatic)
- Echo: 80%
- Chorus: 60%
- Low-pass: 4000 Hz (distant)

**Robot/AI:**
- Speech Rate: 1.0x
- Pitch: -2
- Mechanical: 50 Hz
- Echo: 10%
- High-pass: 150 Hz (tinny)

**Monstrous Creature:**
- Speech Rate: 0.7x (menacing)
- Pitch: -6 to -8 (size-dependent)
- Distortion: 8 dB (growl)
- Echo: 30%

**Ancient Deity:**
- Speech Rate: 0.6x (slow, deliberate)
- Pitch: -6
- Sentence Pause: 1.8s
- Echo: 100%
- Delay: 300ms
- Chorus: 40%

**Frantic Goblin:**
- Speech Rate: 1.6x (fast)
- Pitch: +8
- Sentence Pause: 0.2s
- Mechanical: 80 Hz (nasally)
- Distortion: 3 dB

### Batch Production Workflow

For multiple NPCs in a scene:

1. Create naming convention: `scene01_npc01_warforged.wav`
2. Use consistent presets for character continuity
3. Export all dialogue sequentially
4. Import into video editor
5. Sync with video content

### Save Your Settings

**Method 1: Manual Notes**
- Write down slider values for favorite combinations
- Create your own reference sheet

**Method 2: Create Custom Presets**
- Edit `presets/voice_presets.json`
- Add new preset with your values
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for format

## Troubleshooting

### Common Issues

**No Voice Models Found**
- Download a voice model using "Download Voice Models" button
- Or manually place .onnx files in `models/` folder
- Restart the application

**Audio Sounds Distorted**
- Reduce Distortion slider
- Lower Mechanical Frequency
- Decrease Volume slider
- Reduce extreme pitch shifts

**Voice Sounds Too Robotic**
- Decrease Mechanical Frequency
- Reduce Distortion
- Increase natural variation in text

**Not Enough Effect**
- Increase Echo Level
- Add Chorus effect
- Increase Delay Time
- Adjust pitch shift more dramatically

**Slow Generation**
- Normal: 2-10 seconds per generation
- Longer text = longer processing
- This ensures quality output

**Discord Integration Not Working**
- Check VB-CABLE is installed and system restarted
- Verify Discord input is set to "Default"
- Use **🔧 Reset Audio Device** if mic stuck
- See [vb-cable-setup.html](vb-cable-setup.html)

**Window Too Small / UI Cutoff**
- Window size: 1280x1280 (square)
- All UI elements should be visible
- If not, try maximizing window

## Integration with Tools

### Video Editing

Exported WAV files work with all major editors:
- **DaVinci Resolve**
- **Adobe Premiere Pro**
- **Final Cut Pro**
- **Shotcut**
- **HitFilm Express**

### Audio Editing

Further process exports with:
- **Audacity** (free)
- **Adobe Audition**
- **Reaper**
- **FL Studio**

### Streaming/Recording

Use exports with:
- **OBS Studio**
- **Streamlabs**
- **XSplit**

### Discord (Live Sessions)

Use **Send to Discord** feature for:
- Live TTRPG sessions
- NPC voice acting in real-time
- Immersive storytelling

## Best Practices

1. **Test First**: Always preview before exporting
2. **Start Simple**: Use presets as starting points
3. **Save Favorites**: Note combinations that work
4. **Batch Similar**: Use same preset for related NPCs
5. **Name Clearly**: Use descriptive filenames
6. **Read TEXT_CONTROL_GUIDE.md**: Understand what works with text input
7. **Explore Languages**: Try different voice models
8. **Combine Effects**: Layer multiple sliders for unique voices

## Keyboard Shortcuts

Currently, all controls are mouse-based. Keyboard shortcuts may be added in future versions.

## File Locations

- **Presets**: `presets/voice_presets.json`
- **Voice Models**: `models/` (next to executable)
- **Exports**: `exports/` (default save location)
- **Documentation**: `docs/`
- **Source Code**: `source/` (bundled for GPL compliance)
- **Temporary Files**: Automatically cleaned up

## Technical Details

### Audio Processing Pipeline

1. **TTS Generation** - Piper generates base speech
2. **Speech Rate** - Applied via Piper's length_scale
3. **Sentence Pause** - Applied via Piper's --sentence-silence
4. **Pitch Shift** - Applied first for tonal changes
5. **Ring Modulation** - Creates mechanical effects
6. **Distortion** - Adds grit and aggression
7. **High-pass Filter** - Removes low frequencies
8. **Low-pass Filter** - Removes high frequencies
9. **Chorus** - Creates ethereal, layered sound
10. **Delay** - Adds distinct echo
11. **Reverb** - Final spatial processing
12. **Volume Boost** - Final amplification

### System Requirements

**Minimum:**
- Windows 10 or Linux
- 4GB RAM
- 500MB disk space (+ voice models)

**Recommended:**
- Windows 10/11 or Ubuntu 20.04+
- 8GB RAM
- 2GB disk space (with multiple models)

## Getting Help

**Documentation:**
- [Setup Guide](SETUP.md) - Installation and troubleshooting
- [Text Control Guide](TEXT_CONTROL_GUIDE.md) - Text input tips
- [Multi-Language Guide](MULTILANGUAGE_GUIDE.md) - Language support
- [Quick Reference](QUICK_REFERENCE.md) - Preset creation
- [Discord Setup](vb-cable-setup.html) - VB-CABLE installation

**Community:**
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Share presets and tips

**License:**
- The Artificer is licensed under GNU GPL v3
- You can use it commercially, modify it, and redistribute it
- See About/License dialog in the app for details

---

**Happy voice generation! May your NPCs sound legendary!**
