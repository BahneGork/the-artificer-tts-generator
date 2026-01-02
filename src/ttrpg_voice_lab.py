#!/usr/bin/env python3
"""
The Artificer - TTS Generator
A desktop application for generating and processing NPC voices for TTRPG content.
"""

import os
import sys
import json
import threading
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any

import customtkinter as ctk
from tkinter import filedialog, messagebox
import numpy as np
from pydub import AudioSegment
from pedalboard import (
    Pedalboard,
    Reverb,
    Distortion,
    Chorus,
    LowpassFilter,
    HighpassFilter,
    Delay,
    PitchShift
)

# Try to import pygame for audio playback (optional)
try:
    import pygame.mixer
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Preview will use pydub playback instead.")

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TTRPGVoiceLab(ctk.CTk):
    """Main application class for TTRPG Voice Lab"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("The Artificer - TTS Voice Generator")
        self.geometry("1000x700")

        # Initialize pygame mixer for audio playback (if available)
        if PYGAME_AVAILABLE:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)

        # Application state
        self.current_preset: Optional[Dict[str, Any]] = None
        self.presets: list = []
        self.temp_files: list = []
        self.is_generating = False

        # Paths - handle both development and PyInstaller frozen app
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            if hasattr(sys, '_MEIPASS'):
                self.base_dir = Path(sys._MEIPASS)
            else:
                self.base_dir = Path(sys.executable).parent
        else:
            # Running as script
            self.base_dir = Path(__file__).parent.parent

        self.models_dir = self.base_dir / "models"
        self.presets_dir = self.base_dir / "presets"

        # Exports directory should be in a writable location
        if getattr(sys, 'frozen', False):
            # When frozen, use Documents folder or executable directory
            self.exports_dir = Path(sys.executable).parent / "exports"
        else:
            self.exports_dir = self.base_dir / "exports"

        # Create exports directory if it doesn't exist
        self.exports_dir.mkdir(exist_ok=True)

        # Debug: Show where exports dir is
        print(f"DEBUG: Exports directory: {self.exports_dir}")
        print(f"DEBUG: Frozen: {getattr(sys, 'frozen', False)}")
        print(f"DEBUG: Executable: {sys.executable if hasattr(sys, 'executable') else 'N/A'}")

        # Load presets
        self.load_presets()

        # Build UI
        self.build_ui()

        # Check for Piper model
        self.check_piper_model()

    def load_presets(self):
        """Load voice presets from JSON file"""
        preset_file = self.presets_dir / "voice_presets.json"
        try:
            with open(preset_file, 'r') as f:
                data = json.load(f)
                self.presets = data.get('presets', [])
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                f"Preset file not found: {preset_file}\nPlease ensure voice_presets.json exists."
            )
            self.presets = []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse preset file.")
            self.presets = []

    def build_ui(self):
        """Build the main user interface"""
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left sidebar for presets
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Sidebar title
        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Voice Presets",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.sidebar_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Preset buttons
        self.preset_buttons = []
        for idx, preset in enumerate(self.presets):
            btn = ctk.CTkButton(
                self.sidebar,
                text=preset['name'],
                command=lambda p=preset: self.load_preset(p),
                height=40
            )
            btn.grid(row=idx+1, column=0, padx=20, pady=5, sticky="ew")
            self.preset_buttons.append(btn)

        # Main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="NPC Voice Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Current preset label
        self.preset_label = ctk.CTkLabel(
            self.main_frame,
            text="No preset selected",
            font=ctk.CTkFont(size=14)
        )
        self.preset_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Voice/Language selector frame
        self.voice_frame = ctk.CTkFrame(self.main_frame)
        self.voice_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.voice_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.voice_frame,
            text="Voice Model:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.voice_selector = ctk.CTkComboBox(
            self.voice_frame,
            values=["No models found"],
            command=self.on_voice_selected,
            state="readonly"
        )
        self.voice_selector.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Populate voice models (moved to after status_label creation)
        self.voice_models = {}  # Dictionary: display_name -> model_path

        # Text input area
        self.text_frame = ctk.CTkFrame(self.main_frame)
        self.text_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.text_frame,
            text="Dialogue Text:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.text_input = ctk.CTkTextbox(
            self.text_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.text_input.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.text_input.insert("1.0", "Greetings, adventurer. What brings you to these lands?")

        # Effect controls frame - Row 1
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.controls_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Speech Rate slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Speech Rate:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, padx=5, pady=(10, 5), sticky="w")

        self.speech_rate_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=30,
            command=self.update_speech_rate_label
        )
        self.speech_rate_slider.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.speech_rate_slider.set(1.0)

        self.speech_rate_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="1.0x"
        )
        self.speech_rate_value_label.grid(row=2, column=0, padx=5, pady=(0, 10))

        # Pitch shift slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Pitch Shift:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=1, padx=5, pady=(10, 5), sticky="w")

        self.pitch_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=-12,
            to=12,
            number_of_steps=24,
            command=self.update_pitch_label
        )
        self.pitch_slider.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.pitch_slider.set(0)

        self.pitch_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="0"
        )
        self.pitch_value_label.grid(row=2, column=1, padx=5, pady=(0, 10))

        # Distortion slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Distortion:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=2, padx=5, pady=(10, 5), sticky="w")

        self.distortion_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0,
            to=20,
            number_of_steps=40,
            command=self.update_distortion_label
        )
        self.distortion_slider.grid(row=1, column=2, padx=5, pady=(0, 10), sticky="ew")
        self.distortion_slider.set(0)

        self.distortion_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="0 dB"
        )
        self.distortion_value_label.grid(row=2, column=2, padx=5, pady=(0, 10))

        # Mechanical frequency slider (Ring Modulator)
        ctk.CTkLabel(
            self.controls_frame,
            text="Mechanical:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=3, padx=5, pady=(10, 5), sticky="w")

        self.mech_freq_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0,
            to=200,
            number_of_steps=40,
            command=self.update_mech_label
        )
        self.mech_freq_slider.grid(row=1, column=3, padx=5, pady=(0, 10), sticky="ew")
        self.mech_freq_slider.set(0)

        self.mech_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="0 Hz"
        )
        self.mech_value_label.grid(row=2, column=3, padx=5, pady=(0, 10))

        # Volume boost slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Volume:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=4, padx=5, pady=(10, 5), sticky="w")

        self.volume_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0,
            to=12,
            number_of_steps=24,
            command=self.update_volume_label
        )
        self.volume_slider.grid(row=1, column=4, padx=5, pady=(0, 10), sticky="ew")
        self.volume_slider.set(3)

        self.volume_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="+3 dB"
        )
        self.volume_value_label.grid(row=2, column=4, padx=5, pady=(0, 10))

        # Effect controls frame - Row 2
        self.controls_frame2 = ctk.CTkFrame(self.main_frame)
        self.controls_frame2.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.controls_frame2.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Echo/Reverb level slider
        ctk.CTkLabel(
            self.controls_frame2,
            text="Echo Level:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, padx=5, pady=(10, 5), sticky="w")

        self.echo_slider = ctk.CTkSlider(
            self.controls_frame2,
            from_=0,
            to=1,
            number_of_steps=20,
            command=self.update_echo_label
        )
        self.echo_slider.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.echo_slider.set(0.3)

        self.echo_value_label = ctk.CTkLabel(
            self.controls_frame2,
            text="30%"
        )
        self.echo_value_label.grid(row=2, column=0, padx=5, pady=(0, 10))

        # Chorus Depth slider
        ctk.CTkLabel(
            self.controls_frame2,
            text="Chorus Depth:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=1, padx=5, pady=(10, 5), sticky="w")

        self.chorus_slider = ctk.CTkSlider(
            self.controls_frame2,
            from_=0,
            to=1,
            number_of_steps=20,
            command=self.update_chorus_label
        )
        self.chorus_slider.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        self.chorus_slider.set(0)

        self.chorus_value_label = ctk.CTkLabel(
            self.controls_frame2,
            text="Off"
        )
        self.chorus_value_label.grid(row=2, column=1, padx=5, pady=(0, 10))

        # Delay Time slider
        ctk.CTkLabel(
            self.controls_frame2,
            text="Delay Time:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=2, padx=5, pady=(10, 5), sticky="w")

        self.delay_slider = ctk.CTkSlider(
            self.controls_frame2,
            from_=0,
            to=500,
            number_of_steps=50,
            command=self.update_delay_label
        )
        self.delay_slider.grid(row=1, column=2, padx=5, pady=(0, 10), sticky="ew")
        self.delay_slider.set(0)

        self.delay_value_label = ctk.CTkLabel(
            self.controls_frame2,
            text="Off"
        )
        self.delay_value_label.grid(row=2, column=2, padx=5, pady=(0, 10))

        # Low-pass Filter slider
        ctk.CTkLabel(
            self.controls_frame2,
            text="Low-pass:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=3, padx=5, pady=(10, 5), sticky="w")

        self.lowpass_slider = ctk.CTkSlider(
            self.controls_frame2,
            from_=1000,
            to=8000,
            number_of_steps=70,
            command=self.update_lowpass_label
        )
        self.lowpass_slider.grid(row=1, column=3, padx=5, pady=(0, 10), sticky="ew")
        self.lowpass_slider.set(8000)

        self.lowpass_value_label = ctk.CTkLabel(
            self.controls_frame2,
            text="Off"
        )
        self.lowpass_value_label.grid(row=2, column=3, padx=5, pady=(0, 10))

        # High-pass Filter slider
        ctk.CTkLabel(
            self.controls_frame2,
            text="High-pass:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=4, padx=5, pady=(10, 5), sticky="w")

        self.highpass_slider = ctk.CTkSlider(
            self.controls_frame2,
            from_=50,
            to=500,
            number_of_steps=45,
            command=self.update_highpass_label
        )
        self.highpass_slider.grid(row=1, column=4, padx=5, pady=(0, 10), sticky="ew")
        self.highpass_slider.set(50)

        self.highpass_value_label = ctk.CTkLabel(
            self.controls_frame2,
            text="Off"
        )
        self.highpass_value_label.grid(row=2, column=4, padx=5, pady=(0, 10))

        # Action buttons
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.preview_button = ctk.CTkButton(
            self.button_frame,
            text="🔊 Preview",
            command=self.preview_audio,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.preview_button.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.export_button = ctk.CTkButton(
            self.button_frame,
            text="💾 Export WAV",
            command=self.export_audio,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.export_button.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="ew")

        # Status bar
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=7, column=0, padx=20, pady=(0, 10))

        # Load voice models after status_label is created
        self.load_voice_models()

    def update_speech_rate_label(self, value):
        """Update speech rate slider label"""
        self.speech_rate_value_label.configure(text=f"{float(value):.1f}x")

    def update_pitch_label(self, value):
        """Update pitch slider label"""
        self.pitch_value_label.configure(text=f"{int(float(value))}")

    def update_distortion_label(self, value):
        """Update distortion slider label"""
        val = int(float(value))
        self.distortion_value_label.configure(text=f"{val} dB" if val > 0 else "Off")

    def update_mech_label(self, value):
        """Update mechanical frequency slider label"""
        val = int(float(value))
        self.mech_value_label.configure(text=f"{val} Hz" if val > 0 else "Off")

    def update_volume_label(self, value):
        """Update volume slider label"""
        self.volume_value_label.configure(text=f"+{int(float(value))} dB")

    def update_echo_label(self, value):
        """Update echo slider label"""
        self.echo_value_label.configure(text=f"{int(float(value) * 100)}%")

    def update_chorus_label(self, value):
        """Update chorus slider label"""
        val = float(value)
        self.chorus_value_label.configure(text=f"{int(val * 100)}%" if val > 0.05 else "Off")

    def update_delay_label(self, value):
        """Update delay slider label"""
        val = int(float(value))
        self.delay_value_label.configure(text=f"{val}ms" if val > 0 else "Off")

    def update_lowpass_label(self, value):
        """Update low-pass slider label"""
        val = int(float(value))
        self.lowpass_value_label.configure(text=f"{val}Hz" if val < 7900 else "Off")

    def update_highpass_label(self, value):
        """Update high-pass slider label"""
        val = int(float(value))
        self.highpass_value_label.configure(text=f"{val}Hz" if val > 60 else "Off")

    def load_voice_models(self):
        """Scan models directory and populate voice selector"""
        if not self.models_dir.exists():
            return

        onnx_files = list(self.models_dir.glob("*.onnx"))
        if not onnx_files:
            return

        self.voice_models = {}
        for onnx_file in onnx_files:
            json_file = onnx_file.with_suffix('.onnx.json')

            # Try to parse the JSON file for voice info
            display_name = onnx_file.stem
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        voice_info = json.load(f)
                        # Extract language and voice name
                        language = voice_info.get('language', {}).get('name_english', 'Unknown')
                        voice_name = voice_info.get('name', onnx_file.stem)
                        quality = voice_info.get('quality', '')

                        # Format: "English (US) - lessac (medium)"
                        if quality:
                            display_name = f"{language} - {voice_name} ({quality})"
                        else:
                            display_name = f"{language} - {voice_name}"
                except:
                    # If JSON parsing fails, use filename
                    display_name = onnx_file.stem

            self.voice_models[display_name] = str(onnx_file)

        # Update dropdown
        if self.voice_models:
            voice_names = list(self.voice_models.keys())
            self.voice_selector.configure(values=voice_names)
            self.voice_selector.set(voice_names[0])  # Select first voice
            self.status_label.configure(text=f"Loaded {len(voice_names)} voice model(s)")

    def on_voice_selected(self, choice):
        """Handle voice model selection"""
        if choice in self.voice_models:
            self.status_label.configure(text=f"Selected: {choice}")

    def load_preset(self, preset: Dict[str, Any]):
        """Load a voice preset and update UI"""
        self.current_preset = preset
        self.preset_label.configure(text=f"Preset: {preset['name']} - {preset['description']}")

        # Update sliders based on preset
        effects = preset['effects']

        # Row 1 controls
        self.speech_rate_slider.set(effects.get('speech_rate', 1.0))
        self.pitch_slider.set(effects.get('pitch_shift', 0))
        self.distortion_slider.set(effects.get('distortion_drive', 0))
        self.mech_freq_slider.set(effects.get('ring_modulator_freq', 0))
        self.volume_slider.set(effects.get('volume_boost', 3))

        # Row 2 controls
        self.echo_slider.set(effects.get('reverb_wetness', 0.3))
        self.chorus_slider.set(effects.get('chorus_depth', 0.0))
        self.delay_slider.set(effects.get('delay_time_ms', 0))
        self.lowpass_slider.set(effects.get('lowpass_cutoff', 8000))
        self.highpass_slider.set(effects.get('highpass_cutoff', 50))

        # Update labels
        self.update_speech_rate_label(effects.get('speech_rate', 1.0))
        self.update_pitch_label(effects.get('pitch_shift', 0))
        self.update_distortion_label(effects.get('distortion_drive', 0))
        self.update_mech_label(effects.get('ring_modulator_freq', 0))
        self.update_volume_label(effects.get('volume_boost', 3))
        self.update_echo_label(effects.get('reverb_wetness', 0.3))
        self.update_chorus_label(effects.get('chorus_depth', 0.0))
        self.update_delay_label(effects.get('delay_time_ms', 0))
        self.update_lowpass_label(effects.get('lowpass_cutoff', 8000))
        self.update_highpass_label(effects.get('highpass_cutoff', 50))

        self.status_label.configure(text=f"Loaded preset: {preset['name']}")

    def check_piper_model(self):
        """Check if Piper voice model exists"""
        if not self.models_dir.exists():
            self.models_dir.mkdir(exist_ok=True)

        # Look for any .onnx files
        onnx_files = list(self.models_dir.glob("*.onnx"))
        if not onnx_files:
            messagebox.showwarning(
                "No Voice Model Found",
                f"No Piper voice models found in {self.models_dir}\n\n"
                "Please download a voice model from:\n"
                "https://github.com/rhasspy/piper/releases\n\n"
                "Download both the .onnx and .onnx.json files and place them in the 'models' folder."
            )

    def generate_tts(self, text: str) -> Optional[str]:
        """
        Generate TTS audio using Piper.
        Returns path to generated audio file or None on failure.
        """
        try:
            # Get selected voice model from dropdown
            selected_voice = self.voice_selector.get()
            if selected_voice not in self.voice_models:
                messagebox.showerror("Error", "No voice model selected.")
                return None

            model_path = self.voice_models[selected_voice]

            # Create temporary output file in a writable location
            # Use the exports directory which we know is writable
            temp_dir = self.exports_dir / 'temp'
            temp_dir.mkdir(exist_ok=True)

            import uuid
            temp_filename = temp_dir / f"tts_{uuid.uuid4().hex}.wav"
            self.temp_files.append(str(temp_filename))

            # Use piper-tts command line
            import subprocess

            # Find piper executable and set espeak data path
            if getattr(sys, 'frozen', False):
                # Running as frozen executable - piper.exe is in _internal folder
                if hasattr(sys, '_MEIPASS'):
                    piper_exe = Path(sys._MEIPASS) / 'piper.exe'
                    espeak_data = Path(sys._MEIPASS) / 'espeak-ng-data'
                else:
                    piper_exe = Path(sys.executable).parent / '_internal' / 'piper.exe'
                    espeak_data = Path(sys.executable).parent / '_internal' / 'espeak-ng-data'
            else:
                # Running as script - try to find piper in PATH or project root
                piper_exe = 'piper'
                project_piper = Path(__file__).parent.parent / 'piper.exe'
                if project_piper.exists():
                    piper_exe = str(project_piper)
                espeak_data = Path(__file__).parent.parent / 'espeak-ng-data'

            # Set environment variable for espeak-ng data
            env = os.environ.copy()
            if espeak_data.exists():
                env['ESPEAK_DATA_PATH'] = str(espeak_data)

            # Get speech rate from slider
            speech_rate = self.speech_rate_slider.get()
            # Piper uses length_scale which is inverse of speed
            length_scale = 1.0 / speech_rate

            cmd = [
                str(piper_exe),
                '--model', model_path,
                '--output_file', str(temp_filename),
                '--length_scale', str(length_scale)
            ]

            # Run piper with text input
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

            stdout, stderr = process.communicate(input=text)

            if process.returncode != 0:
                raise Exception(f"Piper failed: {stderr}")

            return str(temp_filename)

        except Exception as e:
            messagebox.showerror("TTS Error", f"Failed to generate TTS: {str(e)}")
            return None

    def apply_effects(self, audio_path: str) -> Optional[AudioSegment]:
        """
        Apply audio effects using Pedalboard.
        Returns processed AudioSegment or None on failure.
        """
        try:
            # Load audio
            audio = AudioSegment.from_wav(audio_path)

            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples()).astype(np.float32)
            samples = samples / (2**15)  # Normalize to -1.0 to 1.0

            # Get all effect parameters from sliders
            pitch_shift = self.pitch_slider.get()
            distortion_drive = self.distortion_slider.get()
            mech_freq = self.mech_freq_slider.get()
            volume_boost = self.volume_slider.get()
            reverb_wetness = self.echo_slider.get()
            chorus_depth = self.chorus_slider.get()
            delay_time = self.delay_slider.get()
            lowpass_cutoff = self.lowpass_slider.get()
            highpass_cutoff = self.highpass_slider.get()

            # Build effects chain
            board = Pedalboard()

            # 1. Pitch shift (first in chain for best quality)
            if abs(pitch_shift) > 0.1:
                board.append(PitchShift(semitones=pitch_shift))

            # 2. Ring modulator for mechanical effect (applied directly to samples)
            if mech_freq > 1:
                sample_rate = audio.frame_rate
                t = np.arange(len(samples)) / sample_rate
                modulator = np.sin(2 * np.pi * mech_freq * t)
                samples = samples * modulator

            # 3. Distortion (adds grit and aggression)
            if distortion_drive > 0.1:
                board.append(Distortion(drive_db=distortion_drive))

            # 4. High-pass filter (remove low frequencies for tinny/radio effect)
            if highpass_cutoff > 60:
                board.append(HighpassFilter(cutoff_frequency_hz=highpass_cutoff))

            # 5. Low-pass filter (muffled/distant sound)
            if lowpass_cutoff < 7900:
                board.append(LowpassFilter(cutoff_frequency_hz=lowpass_cutoff))

            # 6. Chorus (ethereal/haunting effect)
            if chorus_depth > 0.05:
                # Pedalboard Chorus doesn't expose depth directly, but we can use it when active
                board.append(Chorus(
                    rate_hz=1.0,
                    depth=chorus_depth,
                    centre_delay_ms=7.0,
                    feedback=0.0,
                    mix=chorus_depth
                ))

            # 7. Delay (echo effect)
            if delay_time > 5:
                # Delay time in seconds
                delay_seconds = delay_time / 1000.0
                board.append(Delay(
                    delay_seconds=delay_seconds,
                    feedback=0.3,
                    mix=0.5
                ))

            # 8. Reverb (spatial/room effect - applied last for natural sound)
            room_size = 0.5
            if self.current_preset:
                room_size = self.current_preset['effects'].get('reverb_room_size', 0.5)

            if reverb_wetness > 0.05:
                board.append(
                    Reverb(
                        room_size=room_size,
                        wet_level=reverb_wetness,
                        dry_level=1.0 - reverb_wetness
                    )
                )

            # Process audio through effects chain
            processed = board(samples, audio.frame_rate)

            # 9. Apply volume boost (final stage)
            if volume_boost > 0:
                # Convert dB to linear gain
                gain = 10 ** (volume_boost / 20)
                processed = processed * gain

            # Convert back to AudioSegment
            processed = np.clip(processed * (2**15), -32768, 32767).astype(np.int16)
            processed_audio = AudioSegment(
                processed.tobytes(),
                frame_rate=audio.frame_rate,
                sample_width=2,
                channels=1
            )

            return processed_audio

        except Exception as e:
            messagebox.showerror("Effects Error", f"Failed to apply effects: {str(e)}")
            return None

    def preview_audio_thread(self):
        """Thread function for preview generation"""
        try:
            self.status_label.configure(text="Generating TTS...")
            self.is_generating = True

            # Get text
            text = self.text_input.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter some text to speak.")
                return

            # Generate TTS
            tts_file = self.generate_tts(text)
            if not tts_file:
                return

            self.status_label.configure(text="Applying effects...")

            # Apply effects
            processed_audio = self.apply_effects(tts_file)
            if not processed_audio:
                return

            # Save to temporary file for playback
            import uuid
            temp_dir = self.exports_dir / 'temp'
            temp_dir.mkdir(exist_ok=True)
            temp_preview_path = temp_dir / f"preview_{uuid.uuid4().hex}.wav"
            self.temp_files.append(str(temp_preview_path))

            processed_audio.export(str(temp_preview_path), format='wav')

            self.status_label.configure(text="Playing preview...")

            # Play audio using pygame or system default player
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(str(temp_preview_path))
                pygame.mixer.music.play()
            else:
                # Use system default WAV player (avoids pydub temp file issues)
                import platform
                if platform.system() == 'Windows':
                    os.startfile(str(temp_preview_path))
                else:
                    # Linux/Mac - try xdg-open or open
                    import subprocess
                    subprocess.run(['xdg-open', str(temp_preview_path)], check=False)

            self.status_label.configure(text="Preview complete - Ready")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()

            # Write error to log file
            log_file = Path(sys.executable).parent / "error_log.txt"
            with open(log_file, 'w') as f:
                f.write(f"Error: {str(e)}\n\n")
                f.write(f"Exports dir: {self.exports_dir}\n\n")
                f.write(f"Traceback:\n{error_details}")

            messagebox.showerror("Error", f"Preview failed: {str(e)}\n\nError log saved to: {log_file}")
            self.status_label.configure(text="Error - Ready")
        finally:
            self.is_generating = False
            self.preview_button.configure(state="normal")

    def preview_audio(self):
        """Preview the generated audio"""
        if self.is_generating:
            messagebox.showinfo("Info", "Audio generation in progress...")
            return

        self.preview_button.configure(state="disabled")
        thread = threading.Thread(target=self.preview_audio_thread, daemon=True)
        thread.start()

    def export_audio_thread(self, output_path: str):
        """Thread function for export generation"""
        try:
            self.status_label.configure(text="Generating TTS for export...")
            self.is_generating = True

            # Get text
            text = self.text_input.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter some text to speak.")
                return

            # Generate TTS
            tts_file = self.generate_tts(text)
            if not tts_file:
                return

            self.status_label.configure(text="Applying effects for export...")

            # Apply effects
            processed_audio = self.apply_effects(tts_file)
            if not processed_audio:
                return

            self.status_label.configure(text="Exporting WAV file...")

            # Export to final location
            processed_audio.export(output_path, format='wav')

            self.status_label.configure(text=f"Exported successfully to {Path(output_path).name}")
            messagebox.showinfo("Success", f"Audio exported to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
            self.status_label.configure(text="Export failed - Ready")
        finally:
            self.is_generating = False
            self.export_button.configure(state="normal")

    def export_audio(self):
        """Export the generated audio to a WAV file"""
        if self.is_generating:
            messagebox.showinfo("Info", "Audio generation in progress...")
            return

        # Get save location
        filename = filedialog.asksaveasfilename(
            initialdir=str(self.exports_dir),
            title="Export Audio",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )

        if not filename:
            return

        self.export_button.configure(state="disabled")
        thread = threading.Thread(target=self.export_audio_thread, args=(filename,), daemon=True)
        thread.start()

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self.temp_files.clear()

    def on_closing(self):
        """Handle application close"""
        if PYGAME_AVAILABLE:
            pygame.mixer.quit()
        self.cleanup_temp_files()
        self.destroy()


def main():
    """Main entry point"""
    try:
        app = TTRPGVoiceLab()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()

        # Write error to log file in a writable location
        try:
            if getattr(sys, 'frozen', False):
                log_file = Path(sys.executable).parent / "startup_error.log"
            else:
                log_file = Path(__file__).parent.parent / "startup_error.log"

            with open(log_file, 'w') as f:
                f.write("=== The Artificer - Startup Error ===\n\n")
                f.write(f"Error: {str(e)}\n\n")
                f.write(f"Python version: {sys.version}\n")
                f.write(f"Frozen: {getattr(sys, 'frozen', False)}\n")
                f.write(f"Executable: {sys.executable}\n\n")
                f.write(f"Traceback:\n{error_details}")

            # Show messagebox with log location
            try:
                from tkinter import Tk, messagebox
                root = Tk()
                root.withdraw()
                messagebox.showerror(
                    "Startup Error",
                    f"The application failed to start.\n\n"
                    f"Error: {str(e)}\n\n"
                    f"Full error log saved to:\n{log_file}"
                )
                root.destroy()
            except:
                pass  # If even messagebox fails, just write to console
        except:
            pass  # If file writing fails, fall through to console output

        # Always print to console (will show if console=True in spec)
        print("\n" + "="*50)
        print("STARTUP ERROR")
        print("="*50)
        print(error_details)
        print("="*50)
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
