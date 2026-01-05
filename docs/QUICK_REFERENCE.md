# Quick Reference Card

## Installation (30 seconds)

```bash
git clone <repo-url>
cd the-artificer-tts-generator
pip install -r requirements.txt
./download_models.sh  # Select option 1
./run.sh
```

## Basic Usage (5 steps)

1. **Select Voice** → Choose language/model in right sidebar
2. **Choose Preset** → Click preset in left sidebar (optional)
3. **Enter Text** → Type NPC dialogue
4. **Adjust Effects** → Move sliders
5. **Preview** → Click 🔊 Preview button
6. **Export** → Click 💾 Export WAV button

## Effect Sliders Cheat Sheet

### Row 1 - Speech Controls

**Speech Rate (0.5x to 2.0x)**
- **0.5x**: Very slow, dramatic, menacing
- **0.8x**: Slower, deliberate
- **1.0x**: Normal speed (default)
- **1.5x**: Fast, excited
- **2.0x**: Very fast, frantic

**Pitch Shift (-12 to +12)**
- **-12 to -6**: Deep demon/dragon voices
- **-4 to -2**: Slightly deeper, authoritative
- **0**: Natural voice
- **+2 to +4**: Slightly higher, youthful
- **+6 to +12**: High-pitched creatures (goblins, pixies)

**Distortion (0 to 20 dB)**
- **0 dB**: Clean, no distortion
- **5 dB**: Subtle grit
- **10 dB**: Moderate aggression/growl
- **15-20 dB**: Heavy distortion, demonic

**Mechanical Frequency (0 to 200 Hz)**
- **0 Hz**: No mechanical effect
- **30-50 Hz**: Subtle robotic quality (Clockwork)
- **60-100 Hz**: Clear mechanical voice
- **100-150 Hz**: Heavy robot/radio effect
- **150-200 Hz**: Extreme mechanical distortion

**Volume (0 to +12 dB)**
- **0 dB**: Quiet
- **+3 dB**: Normal (default)
- **+6 dB**: Moderate boost
- **+12 dB**: Very loud

### Row 2 - Speech Timing

**Sentence Pause (0s to 2.0s)**
- **0s**: No pause, rapid speech
- **0.5s**: Quick pacing
- **0.75s**: Natural (default)
- **1.5s**: Dramatic, slow pacing
- **2.0s**: Very slow, deliberate

### Row 3 - Audio Effects

**Echo Level (0% to 100%)**
- **0-20%**: Intimate, close-up voice
- **30-50%**: Natural room reverb
- **60-80%**: Large hall or cavern
- **90-100%**: Otherworldly, ethereal, ghostly

**Chorus Depth (0% to 100%)**
- **0%**: Off
- **30-50%**: Subtle shimmer, ethereal
- **60-80%**: Moderate otherworldly effect
- **90-100%**: Heavy layered voices

**Delay Time (0 to 500ms)**
- **0ms**: Off
- **100-200ms**: Short echo
- **300-400ms**: Moderate echo tail
- **500ms**: Long distinct echo

**Low-pass Filter (1000 to 8000 Hz)**
- **1000-3000 Hz**: Very muffled, underwater
- **4000-6000 Hz**: Distant, spectral
- **7000-8000 Hz**: Off/minimal (default)

**High-pass Filter (50 to 500 Hz)**
- **50-100 Hz**: Off/minimal (default)
- **150-250 Hz**: Tinny, radio effect
- **300-500 Hz**: Extreme tinny, telephone

## Voice Recipe Book

### Undead/Lich
- Speech Rate: 0.8x
- Pitch: -2
- Sentence Pause: 1.2s
- Echo: 85%
- Chorus: 60%
- Low-pass: 4000 Hz

### Robot/AI
- Speech Rate: 1.0x
- Pitch: -1
- Mechanical: 60 Hz
- Echo: 15%
- High-pass: 150 Hz

### Ancient Dragon
- Speech Rate: 0.6x
- Pitch: -6
- Sentence Pause: 1.5s
- Echo: 80%
- Delay: 300ms

### Goblin/Small Creature
- Speech Rate: 1.6x
- Pitch: +8
- Sentence Pause: 0.2s
- Mechanical: 80 Hz
- Distortion: 3 dB

### Ghostly Spirit
- Speech Rate: 0.9x
- Sentence Pause: 1.0s
- Echo: 90%
- Chorus: 70%
- Low-pass: 4000 Hz

### Demon Lord
- Speech Rate: 0.7x
- Pitch: -6
- Distortion: 15 dB
- Echo: 60%
- Delay: 200ms

### Elemental (Fire)
- Speech Rate: 1.2x
- Distortion: 12 dB
- Mechanical: 30 Hz
- Echo: 40%

### Fey Creature
- Speech Rate: 1.1x
- Pitch: +3
- Chorus: 60%
- Echo: 50%

### Giant
- Speech Rate: 0.5x
- Pitch: -8
- Sentence Pause: 1.8s
- Low-pass: 3000 Hz
- Echo: 70%

### Vampire
- Speech Rate: 0.9x
- Pitch: -3
- Echo: 30%
- Chorus: 20%

### Clockwork Construct
- Pitch: -2
- Mechanical: 50 Hz
- Distortion: 5 dB
- Echo: 20%
- High-pass: 100 Hz

## Discord Integration

**Setup:**
1. Install VB-CABLE (free virtual audio cable)
2. Set Discord input to "Default"
3. Click 📖 Discord Setup Guide in app

**Usage:**
1. Type NPC dialogue
2. Click 🎙️ Send to Discord
3. Audio plays in Discord voice chat
4. Mic automatically restores

**Emergency:** Click 🔧 Reset Audio Device if mic gets stuck

## Multi-Language Support

**Download Voices:**
1. Click "Download Voice Models" button
2. Browse 400+ voices in 30+ languages
3. Select and download
4. Use voice dropdown to select

**Languages:** English, Spanish, French, German, Japanese, Italian, Portuguese, Russian, and 20+ more!

## Text Input Tips

✅ **Do:**
- Write naturally: "Stop. Listen carefully."
- Use Sentence Pause slider for timing
- Keep text conversational

❌ **Don't:**
- Try ellipsis for pauses: "Stop... ... listen" (doesn't work)
- Use phonetic spelling: "ay-thee-nuh" (sounds worse)
- Expect SSML tags to work (Piper doesn't support them)

**See TEXT_CONTROL_GUIDE.md for details**

## File Locations

- **Presets**: `presets/voice_presets.json`
- **Voice Models**: `models/*.onnx`
- **Exports**: `exports/` (default)
- **Documentation**: `docs/`
- **Source Code**: `source/` (GPL compliance)
- **Temp Files**: Auto-cleaned

## Troubleshooting One-Liners

```bash
# No model found
Click "Download Voice Models" in app

# Discord not working
Click "Discord Setup Guide" in app

# Audio not playing
pip install pygame

# Build EXE (Windows)
build-installer-nsis.bat

# Or with Inno Setup
build-installer.bat
```

## Export Best Practices

1. **Preview first** - Always test before exporting
2. **Descriptive names** - `scene01_npc_lich_dialogue.wav`
3. **Natural ranges** - Keep pitch between -8 and +8
4. **Moderate echo** - Less than 70% for most NPCs
5. **Save favorites** - Write down slider values

## Common Mistakes

❌ **Don't**: Export without previewing
✅ **Do**: Always preview first

❌ **Don't**: Use extreme settings without testing
✅ **Do**: Start with presets, adjust gradually

❌ **Don't**: Ignore Sentence Pause slider
✅ **Do**: Use it instead of punctuation tricks

❌ **Don't**: Try to add pauses with "..."
✅ **Do**: Use Sentence Pause slider (verified feature)

## Performance Tips

- **Text length**: 2-10 seconds generation time
- **UI responsive**: Never blocks during generation
- **Preview fast**: Test before committing to export
- **Batch workflow**: Use same preset for related NPCs

## Integration with Editors

### DaVinci Resolve
1. Media Pool → Import
2. Drag WAV to timeline
3. Sync with video

### Adobe Premiere Pro
1. File → Import
2. Select WAV files
3. Place on audio track

### OBS Studio
1. Add Media Source
2. Browse to WAV file
3. Configure playback

### Discord Live
1. Click 🎙️ Send to Discord
2. Audio plays in voice chat
3. Mic auto-restores

## Quick Tips

- **Construct variations**: Adjust Mechanical 40-80 Hz for different types
- **Dragon age**: Lower pitch for ancient (-8), moderate for young (-4)
- **Ghost types**: Poltergeists 60% echo, wraiths 90% echo
- **Demon hierarchy**: Imps +4 pitch, Demons -2, Lords -6
- **Sentence pacing**: Use Sentence Pause for dramatic timing
- **Multiple languages**: Download voices for different NPC cultures
- **Discord sessions**: Perfect for live TTRPG voice acting

## Keyboard Shortcuts

Currently none - all mouse/trackpad based

Future version may add keyboard controls

---

**Pro Tip**: Check TEXT_CONTROL_GUIDE.md to understand what actually works with Piper TTS (no SSML, no text tricks - use sliders instead!)
