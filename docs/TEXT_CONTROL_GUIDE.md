# Text Control Guide - The Artificer TTS

This guide explains what text controls are available when generating voices with Piper TTS.

## ⚠️ Important: What Piper TTS Does NOT Support

**Piper TTS is a simple, fast neural text-to-speech engine.** It does NOT support:

- ❌ SSML (Speech Synthesis Markup Language) tags
- ❌ Special markup like `<break>`, `<emphasis>`, `<prosody>`
- ❌ Phonetic spelling tricks (e.g., "ay-thee-nuh" sounds worse than "Athena")
- ❌ Ellipsis for pauses (e.g., "..." does NOT create pauses)
- ❌ ALL CAPS for emphasis (may work slightly, but inconsistent)

**Bottom line:** Most text tricks from commercial TTS engines (Amazon Polly, Google Wavenet, etc.) **will not work** with Piper.

## ✅ What Actually Works

### 1. **App Control Sliders** (Recommended)

The app provides direct controls that actually work:

**Speech Controls:**
- **Speech Rate** - Controls speaking speed (0.5x to 2.0x)
- **Sentence Pause** - Controls pause length between sentences (0s to 2.0s)

**Audio Effects:**
- **Pitch Shift** - Change voice pitch (-12 to +12 semitones)
- **Distortion** - Add grit and aggression
- **Mechanical** - Ring modulator for robotic effects
- **Volume** - Boost or reduce volume
- **Echo/Reverb** - Add spatial depth
- **Chorus** - Ethereal/haunting effect
- **Delay** - Echo delay
- **Low-pass/High-pass filters** - Muffled or tinny sounds

### 2. **Natural Punctuation**

Basic punctuation works as expected:

```
"Stop." - Full stop, natural pause
"Wait, listen." - Comma creates slight pause
"Really? Are you sure?" - Question mark affects intonation
"No! Don't do that!" - Exclamation adds emphasis
```

**That's it.** Don't try to add extra punctuation for effect - it doesn't work.

### 3. **Phoneme Injection** (Advanced)

For precise pronunciation control, you can inject raw espeak-ng phonemes using `[[ ]]` blocks:

```
"The dragon's name is [[ dɹæɡənˈθoʊn ]]"
```

**Requirements:**
- You must know IPA (International Phonetic Alphabet)
- You must know espeak-ng phoneme syntax
- This is complex and generally not worth it for most users

**IPA Reference:** https://en.wikipedia.org/wiki/International_Phonetic_Alphabet

## 🎯 Best Practices

### Write Naturally

The neural TTS models are trained on natural text. Just write dialogue as you would speak it:

**Good:**
```
"Greetings, adventurer. What brings you to these dark lands?"
```

**Don't Do This:**
```
"Greetings... ... adventurer. What... brings you to these DARK lands?"
```

The second version doesn't add pauses or emphasis - it just confuses the model.

### Use the Sentence Pause Slider

Instead of trying to add pauses with punctuation, use the **Sentence Pause** slider:

- **0s** - No pause between sentences (fast narration)
- **0.75s** - Default, natural pause
- **1.5s** - Dramatic, slower pacing
- **2.0s** - Very slow, deliberate pacing

This actually works, unlike `...` or other punctuation tricks.

### Combine Controls for Effect

Use multiple sliders together:

**Ominous Villain:**
- Speech Rate: 0.8x (slower)
- Sentence Pause: 1.5s (dramatic pauses)
- Pitch: -3 (deeper voice)
- Echo: 40% (menacing presence)

**Frantic Goblin:**
- Speech Rate: 1.5x (faster)
- Sentence Pause: 0.2s (no pauses)
- Pitch: +6 (high pitch)
- Mechanical: 80Hz (nasally quality)

**Ghostly Spirit:**
- Speech Rate: 0.9x
- Sentence Pause: 1.2s
- Echo: 60%
- Chorus: 0.8 (ethereal)
- High-pass: 200Hz (distant)

## 🔧 Technical Details

### Why Doesn't SSML Work?

Piper TTS uses neural voice models trained on plain text. The models don't understand markup tags - they only understand phonemes (sound units). SSML support would require:

1. Parsing markup tags
2. Converting tags to model-specific parameters
3. Training data that includes markup variations

As of 2025, Piper development has moved to https://github.com/OHF-Voice/piper1-gpl, and SSML support remains unimplemented. Some features (breaks, substitutions) were planned but never completed.

### Available Piper Parameters

The Artificer exposes these Piper command-line parameters:

- `--length-scale` - Speech rate (controlled by Speech Rate slider)
- `--sentence-silence` - Pause between sentences (controlled by Sentence Pause slider)
- `--model` - Voice model selection (controlled by Voice dropdown)

All other effects (pitch, distortion, echo, etc.) are applied **after** TTS generation using Pedalboard audio processing.

## 📚 Additional Resources

**Official Piper Documentation:**
- GitHub Repository: https://github.com/OHF-Voice/piper1-gpl
- Voice Samples: https://rhasspy.github.io/piper-samples/

**IPA Resources (for phoneme injection):**
- IPA Chart: https://www.ipachart.com/
- espeak-ng Phoneme Documentation: https://github.com/espeak-ng/espeak-ng/blob/master/docs/phonemes.md

**The Artificer Documentation:**
- See `USER_GUIDE.md` for general app usage
- See `QUICK_REFERENCE.md` for preset creation
- See `vb-cable-setup.html` for Discord integration

---

**Remember:** Piper TTS is designed for simplicity and speed. If you need advanced text markup, consider commercial TTS engines. For most TTRPG voice generation, the app's sliders and presets provide everything you need.
