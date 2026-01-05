# The Artificer - TTS Voice Generator Roadmap

This document outlines planned features and improvements for The Artificer.

## Version 1.2.0 (Planned)

### High Priority
- [ ] **Save/Load Custom Presets** - Allow users to save their own slider configurations as custom presets
  - Save preset button in UI
  - Load custom presets from user presets folder
  - Export/import preset files
  - Preset management (rename, delete custom presets)

### Medium Priority
- [ ] **Batch Processing** - Process multiple text files at once
  - Select multiple text files
  - Auto-generate filenames from text content
  - Progress bar for batch operations

- [ ] **Keyboard Shortcuts** - Add keyboard shortcuts for common operations
  - Ctrl+P: Preview
  - Ctrl+E: Export
  - Ctrl+D: Send to Discord
  - Ctrl+S: Save custom preset

- [ ] **Recent Files List** - Quick access to recently exported files
  - Show last 10 exports
  - Quick re-export with same settings

- [ ] **Volume Normalization** - Auto-normalize output volume
  - Option to normalize all exports to consistent volume
  - Peak limiter to prevent clipping

### Low Priority
- [ ] **Real-time Preview** - Update preview as sliders are adjusted
  - Toggle option (may impact performance)
  - Debounced updates to avoid too many generations

- [ ] **MIDI Controller Support** - Control sliders with MIDI hardware
  - Map MIDI controls to sliders
  - Save MIDI mappings

- [ ] **Effect Preset Library** - Share effect combinations
  - Community preset repository
  - Import/export preset packs

- [ ] **Waveform Visualization** - Show audio waveform
  - Visual representation of generated audio
  - Helps identify clipping or issues

## Version 2.0.0 (Future)

### Major Features
- [ ] **Multi-Voice Scenes** - Create scenes with multiple characters
  - Assign different voices to different speakers
  - Timeline-based editing
  - Export complete scenes

- [ ] **Voice Training** - Train custom voice models (if feasible)
  - Record voice samples
  - Fine-tune Piper models
  - Share custom models

- [ ] **Plugin System** - Extend functionality with plugins
  - Custom effects
  - Custom export formats
  - Integration with other tools

## Completed Features

### Version 1.1.0 (2025-01-05)
- ✅ Discord Integration (Send to Discord)
- ✅ Multi-Language Support (30+ languages, 400+ voices)
- ✅ Enhanced Audio Controls (11 sliders)
- ✅ 7 New Voice Presets
- ✅ GPL v3 Compliance
- ✅ NSIS Installer Support
- ✅ Comprehensive Documentation

### Version 1.0.0 (2024-12-29)
- ✅ Initial release
- ✅ 5 voice presets
- ✅ Basic audio effects
- ✅ Piper TTS integration
- ✅ Preview and export functionality

## Community Requests

Have a feature request? Create an issue on [GitHub](https://github.com/BahneGork/the-artificer-tts-generator/issues) with the `enhancement` label.

## Notes

- Features are listed in approximate priority order within each section
- Priorities may change based on community feedback and technical feasibility
- Some features may be moved between versions as development progresses
