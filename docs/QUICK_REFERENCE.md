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

1. **Select Preset** → Click preset in sidebar
2. **Enter Text** → Type NPC dialogue
3. **Adjust Effects** → Move sliders
4. **Preview** → Click 🔊 Preview button
5. **Export** → Click 💾 Export WAV button

## Effect Sliders Cheat Sheet

### Pitch Shift
- **-12 to -6**: Deep demon/dragon voices
- **-4 to -2**: Slightly deeper, more authoritative
- **0**: Natural voice
- **+2 to +4**: Slightly higher, youthful
- **+6 to +12**: High-pitched creatures (goblins, pixies)

### Mechanical Frequency
- **0 Hz**: No mechanical effect
- **20-40 Hz**: Subtle robotic quality
- **50-80 Hz**: Clear mechanical voice (Warforged)
- **100-150 Hz**: Heavy robot/radio effect
- **150-200 Hz**: Extreme mechanical distortion

### Echo Level
- **0-20%**: Intimate, close-up voice
- **30-50%**: Natural room reverb
- **60-80%**: Large hall or cavern
- **90-100%**: Otherworldly, ethereal, ghostly

## Voice Recipe Book

### Undead/Lich
- Pitch: -3
- Mechanical: 0 Hz
- Echo: 85%

### Robot/AI
- Pitch: -1
- Mechanical: 60 Hz
- Echo: 15%

### Elemental (Air)
- Pitch: +3
- Mechanical: 25 Hz
- Echo: 75%

### Elemental (Earth)
- Pitch: -6
- Mechanical: 0 Hz
- Echo: 90%

### Tiny Creature (Fairy/Sprite)
- Pitch: +8
- Mechanical: 0 Hz
- Echo: 40%

### Cosmic Entity
- Pitch: -8
- Mechanical: 15 Hz
- Echo: 95%

### Swarm Intelligence
- Pitch: +2
- Mechanical: 45 Hz
- Echo: 60%

### Ancient Construct
- Pitch: -2
- Mechanical: 70 Hz
- Echo: 50%

## Keyboard Shortcuts

Currently none - use mouse/trackpad

## File Locations

- **Presets**: `presets/voice_presets.json`
- **Voice Models**: `models/*.onnx`
- **Exports**: `exports/` (default)
- **Temp Files**: Auto-cleaned

## Troubleshooting One-Liners

```bash
# No model found
./download_models.sh

# Piper not found
pip install piper-tts

# Audio not playing
pip install pygame

# Build EXE (Windows)
pyinstaller ttrpg_voice_lab.spec
```

## Export Best Practices

1. Use descriptive filenames: `npc_warforged_greeting.wav`
2. Test with preview first
3. Keep pitch shift between -8 and +8 for natural results
4. Use less than 70% echo unless going for extreme effects
5. Export at highest quality - file size doesn't matter for video editing

## Common Mistakes

❌ **Don't**: Export without previewing
✅ **Do**: Always preview first

❌ **Don't**: Use extreme mechanical frequency (>150 Hz) unless intentional
✅ **Do**: Start with preset defaults and adjust gradually

❌ **Don't**: Forget to adjust sliders after changing presets
✅ **Do**: Sliders update with preset, but verify before export

❌ **Don't**: Use full 100% echo on everything
✅ **Do**: Use echo sparingly for normal NPCs

## Performance Tips

- **Longer text = longer generation time** (2-10 seconds)
- **UI stays responsive** during generation
- **Preview before export** to save time
- **Batch similar NPCs** with same preset

## Integration with Video Editors

### DaVinci Resolve
1. Import WAV to Media Pool
2. Drag to timeline
3. Sync with video

### Adobe Premiere Pro
1. File → Import
2. Select WAV files
3. Place on audio track

### Audacity (for further processing)
1. File → Open
2. Apply additional effects if needed
3. Export as desired format

## Quick Tips

- **Warforged Variations**: Adjust mechanical freq between 40-80 Hz for different construct types
- **Dragon Age**: Lower pitch for ancient dragons, moderate for young dragons
- **Ghost Types**: Poltergeists use less echo (60%), wraiths use more (90%)
- **Demon Hierarchy**: Imps +4 pitch, Demons -2, Demon Lords -6
- **NPC Consistency**: Write down settings for recurring characters

---

**Pro Tip**: Save your favorite slider combinations by screenshotting or writing them down. Custom preset saving coming in future version!
