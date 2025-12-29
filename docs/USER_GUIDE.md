# The Artificer - TTS Voice Generator User Guide

## Overview

The Artificer is a desktop application designed for TTRPG content creators to generate high-quality NPC voices for pre-recorded sessions, actual plays, and video content.

## Key Features

### Voice Presets

The application includes several pre-configured voice profiles:

1. **Warforged**: Mechanical construct with metallic resonance
   - Ring modulation at 50Hz
   - Distortion for mechanical quality
   - Perfect for construct NPCs

2. **Ancient Dragon**: Deep, resonant voice with cavernous reverb
   - Pitch shifted down 4 semitones
   - Heavy reverb for otherworldly presence
   - Ideal for dragons, ancient beings, deities

3. **Ghostly Apparition**: Ethereal, otherworldly voice
   - Chorus effect for multiple voices
   - Full wet reverb
   - Low-pass filter for spectral quality
   - Great for ghosts, spirits, undead

4. **Demon Lord**: Dark, distorted voice
   - Heavy distortion and pitch shift
   - Moderate reverb
   - Perfect for demons, devils, villains

5. **Goblin**: High-pitched, nasally creature voice
   - Pitch shifted up
   - Light processing
   - Ideal for small creatures, goblins, kobolds

## Using the Application

### Step 1: Select a Preset

Click on any preset in the left sidebar to load its default settings. The preset name and description will appear at the top of the main area.

### Step 2: Enter Dialogue

Type or paste your NPC's dialogue in the text box. The application works best with:
- Single sentences or short paragraphs
- Natural punctuation for pacing
- Text without special characters

**Tips:**
- Use commas for brief pauses
- Use periods for longer pauses
- Avoid unusual formatting

### Step 3: Customize Effects

Use the three sliders to fine-tune the voice:

#### Pitch Shift
- Range: -12 to +12 semitones
- **Lower values** (-4 to -12): Deeper, more menacing voices
- **Higher values** (+4 to +12): Higher-pitched, creature-like voices
- **0**: Natural voice pitch

#### Mechanical Frequency
- Range: 0 to 200 Hz
- **0 Hz**: No mechanical effect
- **30-60 Hz**: Subtle robotic quality
- **100+ Hz**: Heavy mechanical/radio effect
- Creates a "ring modulator" effect for constructs and mechanical beings

#### Echo Level
- Range: 0% to 100%
- **0-20%**: Minimal reverb, intimate setting
- **30-50%**: Moderate echo, natural room
- **60-100%**: Heavy reverb, cavernous or otherworldly

### Step 4: Preview

Click the **🔊 Preview** button to:
1. Generate the TTS audio (may take 2-5 seconds)
2. Apply all effects
3. Play the audio through your speakers

**Note:** The preview button will be disabled during generation to prevent multiple simultaneous processes.

### Step 5: Export

Click the **💾 Export WAV** button to:
1. Choose a save location
2. Generate the final high-quality audio
3. Save as a .WAV file

**Important:** The exported file is a digital render, not a recording. This means:
- No background noise
- Crystal-clear quality
- Consistent output regardless of system performance
- Perfect for video editing

## Advanced Tips

### Creating Custom Voice Profiles

1. Load a preset that's close to what you want
2. Adjust the sliders to taste
3. Make note of your settings for future use

### Batch Production Workflow

For multiple NPCs in a scene:
1. Create a naming convention (e.g., `scene01_npc_warforged.wav`)
2. Use the same preset for consistency
3. Export all dialogue
4. Import into your video editor

### Effect Combinations

**Undead/Spectral:**
- Pitch: -2 to +2
- Mechanical: 0 Hz
- Echo: 80-100%

**Robot/AI:**
- Pitch: 0 to -2
- Mechanical: 40-80 Hz
- Echo: 10-20%

**Monster/Creature:**
- Pitch: -6 to +6 (depending on size)
- Mechanical: 0 Hz
- Echo: 20-40%

**Deity/Cosmic Entity:**
- Pitch: -4 to -8
- Mechanical: 0 Hz
- Echo: 90-100%

**Elemental:**
- Pitch: -3 to +3
- Mechanical: 15-30 Hz (for crackling effect)
- Echo: 60-80%

## Technical Details

### Audio Quality

- **Sample Rate**: 22050 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Format**: WAV (uncompressed)

### Processing Pipeline

1. **TTS Generation**: Piper generates base speech
2. **Pitch Shift**: Applied first for tonal changes
3. **Ring Modulation**: Creates mechanical effects
4. **Distortion**: Adds grit and aggression
5. **Chorus**: Creates ethereal, layered sound
6. **Low-Pass Filter**: Removes high frequencies for spectral quality
7. **Reverb**: Final spatial processing

### File Locations

- **Presets**: `presets/voice_presets.json`
- **Voice Models**: `models/`
- **Exports**: `exports/` (default save location)
- **Temporary Files**: Automatically cleaned up after use

## Troubleshooting

### Audio Sounds Distorted
- Reduce the Mechanical Frequency
- Lower the pitch shift amount
- Decrease distortion drive in preset

### Voice Sounds Too Robotic
- Decrease Mechanical Frequency
- Add slight pitch variation in your text delivery
- Reduce distortion

### Not Enough Effect
- Increase Echo Level
- Adjust pitch shift more dramatically
- Try a different base preset

### Slow Generation
- Normal generation takes 2-10 seconds depending on text length
- Longer text = longer processing time
- This is expected and ensures quality

## Best Practices

1. **Test First**: Always preview before exporting
2. **Save Settings**: Note your favorite combinations
3. **Batch Similar Content**: Use same preset for related NPCs
4. **Name Files Clearly**: Use descriptive filenames
5. **Keep Originals**: Save unprocessed audio if you might want to re-process

## Integration with Video Editing

The exported WAV files work with all major video editors:
- **DaVinci Resolve**
- **Adobe Premiere Pro**
- **Final Cut Pro**
- **OBS Studio**
- **Audacity** (for further processing)

Simply import the WAV files into your timeline and sync with your video content.

## Future Enhancements

Potential features for future versions:
- Custom preset saving
- Batch text processing
- Additional voice models
- Real-time preview
- Effect presets library
- MIDI controller support

---

**Happy voice generation! May your NPCs sound legendary!**
