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
from pydub.playback import play
from pedalboard import (
    Pedalboard,
    Reverb,
    Distortion,
    Chorus,
    LowpassFilter,
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
            self.base_dir = Path(sys.executable).parent
        else:
            # Running as script
            self.base_dir = Path(__file__).parent.parent

        self.models_dir = self.base_dir / "models"
        self.presets_dir = self.base_dir / "presets"
        self.exports_dir = self.base_dir / "exports"

        # Create exports directory if it doesn't exist
        self.exports_dir.mkdir(exist_ok=True)

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

        # Text input area
        self.text_frame = ctk.CTkFrame(self.main_frame)
        self.text_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
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

        # Effect controls frame
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Pitch shift slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Pitch Shift (semitones):",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.pitch_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=-12,
            to=12,
            number_of_steps=24,
            command=self.update_pitch_label
        )
        self.pitch_slider.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.pitch_slider.set(0)

        self.pitch_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="0"
        )
        self.pitch_value_label.grid(row=2, column=0, padx=10, pady=(0, 10))

        # Mechanical frequency slider (Ring Modulator)
        ctk.CTkLabel(
            self.controls_frame,
            text="Mechanical Freq (Hz):",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")

        self.mech_freq_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0,
            to=200,
            number_of_steps=40,
            command=self.update_mech_label
        )
        self.mech_freq_slider.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.mech_freq_slider.set(0)

        self.mech_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="0 Hz"
        )
        self.mech_value_label.grid(row=2, column=1, padx=10, pady=(0, 10))

        # Echo/Reverb level slider
        ctk.CTkLabel(
            self.controls_frame,
            text="Echo Level:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=2, padx=10, pady=(10, 5), sticky="w")

        self.echo_slider = ctk.CTkSlider(
            self.controls_frame,
            from_=0,
            to=1,
            number_of_steps=20,
            command=self.update_echo_label
        )
        self.echo_slider.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="ew")
        self.echo_slider.set(0.3)

        self.echo_value_label = ctk.CTkLabel(
            self.controls_frame,
            text="30%"
        )
        self.echo_value_label.grid(row=2, column=2, padx=10, pady=(0, 10))

        # Action buttons
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
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
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 10))

    def update_pitch_label(self, value):
        """Update pitch slider label"""
        self.pitch_value_label.configure(text=f"{int(float(value))}")

    def update_mech_label(self, value):
        """Update mechanical frequency slider label"""
        self.mech_value_label.configure(text=f"{int(float(value))} Hz")

    def update_echo_label(self, value):
        """Update echo slider label"""
        self.echo_value_label.configure(text=f"{int(float(value) * 100)}%")

    def load_preset(self, preset: Dict[str, Any]):
        """Load a voice preset and update UI"""
        self.current_preset = preset
        self.preset_label.configure(text=f"Preset: {preset['name']} - {preset['description']}")

        # Update sliders based on preset
        effects = preset['effects']
        self.pitch_slider.set(effects.get('pitch_shift', 0))
        self.mech_freq_slider.set(effects.get('ring_modulator_freq', 0))
        self.echo_slider.set(effects.get('reverb_wetness', 0.3))

        # Update labels
        self.update_pitch_label(effects.get('pitch_shift', 0))
        self.update_mech_label(effects.get('ring_modulator_freq', 0))
        self.update_echo_label(effects.get('reverb_wetness', 0.3))

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
            # Find Piper model
            onnx_files = list(self.models_dir.glob("*.onnx"))
            if not onnx_files:
                messagebox.showerror("Error", "No Piper voice model found in models folder.")
                return None

            model_path = str(onnx_files[0])

            # Create temporary output file
            temp_output = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_output.close()
            self.temp_files.append(temp_output.name)

            # Use piper-tts command line
            import subprocess

            cmd = [
                'piper',
                '--model', model_path,
                '--output_file', temp_output.name
            ]

            # Run piper with text input
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate(input=text)

            if process.returncode != 0:
                raise Exception(f"Piper failed: {stderr}")

            return temp_output.name

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

            # Get effect parameters from sliders
            pitch_shift = self.pitch_slider.get()
            mech_freq = self.mech_freq_slider.get()
            reverb_wetness = self.echo_slider.get()

            # Build effects chain
            board = Pedalboard()

            # Pitch shift
            if abs(pitch_shift) > 0.1:
                board.append(PitchShift(semitones=pitch_shift))

            # Ring modulator for mechanical effect
            if mech_freq > 0:
                # Simulate ring modulator with amplitude modulation
                sample_rate = audio.frame_rate
                t = np.arange(len(samples)) / sample_rate
                modulator = np.sin(2 * np.pi * mech_freq * t)
                samples = samples * modulator

            # Distortion (if preset includes it)
            if self.current_preset:
                distortion_drive = self.current_preset['effects'].get('distortion_drive', 0)
                if distortion_drive > 0:
                    board.append(Distortion(drive_db=distortion_drive))

            # Chorus (if preset includes it)
            if self.current_preset and self.current_preset['effects'].get('chorus_enabled', False):
                board.append(Chorus())

            # Low-pass filter (if preset includes it)
            if self.current_preset and 'lowpass_cutoff' in self.current_preset['effects']:
                cutoff = self.current_preset['effects']['lowpass_cutoff']
                board.append(LowpassFilter(cutoff_frequency_hz=cutoff))

            # Reverb
            room_size = 0.5
            if self.current_preset:
                room_size = self.current_preset['effects'].get('reverb_room_size', 0.5)

            board.append(
                Reverb(
                    room_size=room_size,
                    wet_level=reverb_wetness,
                    dry_level=1.0 - reverb_wetness
                )
            )

            # Process audio
            processed = board(samples, audio.frame_rate)

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
            temp_preview = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_preview.close()
            self.temp_files.append(temp_preview.name)

            processed_audio.export(temp_preview.name, format='wav')

            self.status_label.configure(text="Playing preview...")

            # Play audio using pygame or pydub
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(temp_preview.name)
                pygame.mixer.music.play()
            else:
                # Use pydub playback as fallback
                preview_audio = AudioSegment.from_wav(temp_preview.name)
                play(preview_audio)

            self.status_label.configure(text="Preview complete - Ready")

        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")
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
    app = TTRPGVoiceLab()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
