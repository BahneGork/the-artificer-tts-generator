# Multi-Language Voice Models Guide

The Artificer supports **all languages** available in Piper TTS, including Danish!

## Quick Start: Adding Danish Voices

### Step 1: Download Danish Voice Models

Visit the Piper voices repository:
**https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/da/da_DK**

Available Danish voices:
- **talesyntese/medium** - Best quality, recommended

### Step 2: Download Required Files

For each voice, download **both files**:
1. The `.onnx` file (the voice model)
2. The `.onnx.json` file (voice metadata)

Example for Danish medium quality:
- `da_DK-talesyntese-medium.onnx`
- `da_DK-talesyntese-medium.onnx.json`

### Step 3: Place Files in Models Folder

Copy both files to your `models` folder:
- **Development**: `the-artificer-tts-generator/models/`
- **Built EXE**: `TTRPGVoiceLab/models/`

### Step 4: Restart the Application

The voice selector dropdown will automatically detect and display:
```
Danish - talesyntese (medium)
```

## Other Supported Languages

Piper supports **many languages**. Browse all available voices here:
**https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0**

### Popular Languages:

| Language | Code | Example Voices |
|----------|------|----------------|
| **Danish** | da_DK | talesyntese |
| **German** | de_DE | thorsten, eva_k, pavoque |
| **Spanish** | es_ES | carlfm, mls |
| **French** | fr_FR | siwis, mls |
| **Italian** | it_IT | riccardo |
| **Dutch** | nl_NL | mls |
| **Norwegian** | no_NO | talesyntese |
| **Swedish** | sv_SE | nst |
| **Polish** | pl_PL | mls |
| **Russian** | ru_RU | ruslan, dmitri |
| **Japanese** | ja_JP | kokoro |
| **Chinese** | zh_CN | huayan |

## Voice Quality Levels

Piper offers different quality levels:

- **x-low** - Fastest, smallest file size
- **low** - Fast, good for testing
- **medium** - **Recommended** - Best balance of quality and speed
- **high** - Highest quality, slower generation

## Using Multiple Languages

1. Download voice models for multiple languages
2. Place all `.onnx` and `.onnx.json` files in the `models` folder
3. The dropdown will show all available voices
4. Switch between languages by selecting from the dropdown
5. All voice effects work with any language!

## Example: Danish NPC Setup

1. Download Danish voice model (see Step 1)
2. Select "Danish - talesyntese (medium)" from dropdown
3. Choose a preset (e.g., "Goblin" for a Danish goblin)
4. Enter Danish text: "Hej, eventyrere! Hvad bringer jer til disse lande?"
5. Click Preview or Export

The voice effects apply to any language - a Danish Ancient Dragon sounds just as deep and booming as an English one!

## Troubleshooting

**Voice doesn't appear in dropdown:**
- Ensure both `.onnx` and `.onnx.json` files are in the models folder
- Restart the application after adding new models

**Generation fails:**
- Verify the `.onnx` file isn't corrupted
- Check that the model is compatible with your Piper version
- Try downloading the files again

**Wrong pronunciation:**
- Make sure you selected the correct language voice
- Some models may not handle all special characters

## Technical Details

The app automatically:
- Scans the `models` folder for `.onnx` files
- Reads `.onnx.json` metadata for language and voice info
- Displays voices in format: `Language - VoiceName (quality)`
- Uses the selected model for all TTS generation

All voice effects (pitch, distortion, filters, etc.) work identically across all languages.
