#!/usr/bin/env python3
"""
The Artificer - TTS Voice Generator

A desktop application for generating and processing NPC voices for TTRPG content.

Copyright (C) 2025 Michael (BahneGork)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Source code: https://github.com/BahneGork/the-artificer-tts-generator
"""

import os
import sys
import json
import threading
import tempfile
import webbrowser
import subprocess
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

# Try to import pycaw for Windows audio device control (Discord integration)
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IMMDeviceEnumerator, EDataFlow, ERole

    # Define PKEY_Device_FriendlyName using comtypes (not ctypes)
    from comtypes import GUID
    import comtypes

    # Define PROPERTYKEY structure using comtypes
    class PROPERTYKEY(comtypes.Structure):
        _fields_ = [
            ('fmtid', GUID),
            ('pid', comtypes.c_ulong)
        ]

    PKEY_Device_FriendlyName = PROPERTYKEY(
        GUID('{a45c254e-df1c-4efd-8020-67d146a850e0}'),
        14
    )

    # Define IPolicyConfig interface for setting default audio device
    # This is not exposed by pycaw, so we define it ourselves
    from comtypes import COMMETHOD, HRESULT
    from ctypes.wintypes import LPCWSTR, DWORD

    class IPolicyConfig(comtypes.IUnknown):
        _iid_ = GUID('{f8679f50-850a-41cf-9c72-430f290290c8}')
        _methods_ = [
            # We only need SetDefaultEndpoint, but need to define all methods in order
            COMMETHOD([], HRESULT, 'GetMixFormat'),
            COMMETHOD([], HRESULT, 'GetDeviceFormat'),
            COMMETHOD([], HRESULT, 'ResetDeviceFormat'),
            COMMETHOD([], HRESULT, 'SetDeviceFormat'),
            COMMETHOD([], HRESULT, 'GetProcessingPeriod'),
            COMMETHOD([], HRESULT, 'SetProcessingPeriod'),
            COMMETHOD([], HRESULT, 'GetShareMode'),
            COMMETHOD([], HRESULT, 'SetShareMode'),
            COMMETHOD([], HRESULT, 'GetPropertyValue'),
            COMMETHOD([], HRESULT, 'SetPropertyValue'),
            COMMETHOD([], HRESULT, 'SetDefaultEndpoint',
                     (['in'], LPCWSTR, 'wszDeviceId'),
                     (['in'], DWORD, 'role')),
        ]

    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False
    print("Warning: pycaw not available. Discord integration will be disabled.")

# Try to import pygame for audio playback (optional)
try:
    import pygame.mixer
    PYGAME_AVAILABLE = True
    print("SUCCESS: pygame.mixer imported successfully")
except ImportError as e:
    PYGAME_AVAILABLE = False
    print(f"Warning: pygame not available: {e}")
    print("Preview will use pydub playback instead.")
except Exception as e:
    PYGAME_AVAILABLE = False
    print(f"Error importing pygame: {e}")
    import traceback
    traceback.print_exc()

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Voice Model Catalog - Curated list for TTRPG characters
VOICE_CATALOG = [
    {
        "id": "en_US-hfc_male-medium",
        "name": "English (US) - Deep Male",
        "description": "Deep, authoritative voice. Perfect for: Dragons, Giants, Warriors, Villains",
        "language": "en/en_US",
        "voice": "hfc_male",
        "quality": "medium",
        "size_mb": 63,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/hfc_male/medium/speaker_0.mp3"
    },
    {
        "id": "en_US-joe-medium",
        "name": "English (US) - Gruff Male",
        "description": "Rough, masculine voice. Perfect for: Guards, Bandits, Orcs, Dwarves",
        "language": "en/en_US",
        "voice": "joe",
        "quality": "medium",
        "size_mb": 63,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/joe/medium/speaker_0.mp3"
    },
    {
        "id": "en_GB-alan-medium",
        "name": "English (UK) - British Male",
        "description": "Refined British accent. Perfect for: Nobles, Wizards, Scholars, Vampires",
        "language": "en/en_GB",
        "voice": "alan",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_GB/alan/medium/speaker_0.mp3"
    },
    {
        "id": "en_US-amy-medium",
        "name": "English (US) - Female",
        "description": "Clear female voice. Perfect for: Queens, Clerics, Female NPCs, Elves",
        "language": "en/en_US",
        "voice": "amy",
        "quality": "medium",
        "size_mb": 63,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/amy/medium/speaker_0.mp3"
    },
    {
        "id": "en_US-lessac-medium",
        "name": "English (US) - Neutral Female (Default)",
        "description": "Balanced, clear voice. Perfect for: General NPCs, Narration",
        "language": "en/en_US",
        "voice": "lessac",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/lessac/medium/speaker_0.mp3"
    },
    {
        "id": "en_US-ryan-high",
        "name": "English (US) - Young Male",
        "description": "Higher-pitched male. Perfect for: Young NPCs, Halflings, with effects for Goblins",
        "language": "en/en_US",
        "voice": "ryan",
        "quality": "high",
        "size_mb": 112,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/ryan/high/speaker_0.mp3"
    },
    {
        "id": "en_US-libritts-high",
        "name": "English (US) - Multi-Speaker (Best Quality)",
        "description": "Highest quality, natural speech. Perfect for: Important NPCs, Player Characters",
        "language": "en/en_US",
        "voice": "libritts",
        "quality": "high",
        "size_mb": 182,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/libritts/high/speaker_0.mp3"
    },
    {
        "id": "en_US-hfc_female-medium",
        "name": "English (US) - Mature Female",
        "description": "Deeper female voice. Perfect for: Hags, Witches, Matriarchs, Authority Figures",
        "language": "en/en_US",
        "voice": "hfc_female",
        "quality": "medium",
        "size_mb": 63,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/hfc_female/medium/speaker_0.mp3"
    },
    {
        "id": "en_US-ljspeech-medium",
        "name": "English (US) - Soft Female",
        "description": "Gentle, pleasant voice. Perfect for: Healers, Fairies, Kind NPCs",
        "language": "en/en_US",
        "voice": "ljspeech",
        "quality": "medium",
        "size_mb": 63,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_US/ljspeech/medium/speaker_0.mp3"
    },
    {
        "id": "en_GB-northern_english_male-medium",
        "name": "English (UK) - Northern Male",
        "description": "Northern English accent. Perfect for: Commoners, Tavern Keepers, Workers",
        "language": "en/en_GB",
        "voice": "northern_english_male",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/en/en_GB/northern_english_male/medium/speaker_0.mp3"
    },
    # Spanish voices
    {
        "id": "es_ES-mls_9972-low",
        "name": "Spanish (Spain) - Male",
        "description": "Clear Spanish voice. Perfect for: Spanish NPCs, Multilingual campaigns",
        "language": "es/es_ES",
        "voice": "mls_9972",
        "quality": "low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/es/es_ES/mls_9972/low/speaker_0.mp3"
    },
    {
        "id": "es_MX-ald-medium",
        "name": "Spanish (Mexico) - Male",
        "description": "Mexican Spanish voice. Perfect for: Latin-inspired campaigns, Spanish NPCs",
        "language": "es/es_MX",
        "voice": "ald",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/es/es_MX/ald/medium/speaker_0.mp3"
    },
    # French voices
    {
        "id": "fr_FR-siwis-medium",
        "name": "French - Female",
        "description": "Clear French female voice. Perfect for: French NPCs, European campaigns",
        "language": "fr/fr_FR",
        "voice": "siwis",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/fr/fr_FR/siwis/medium/speaker_0.mp3"
    },
    {
        "id": "fr_FR-mls_1840-low",
        "name": "French - Male",
        "description": "Clear French male voice. Perfect for: French NPCs, Nobles, Merchants",
        "language": "fr/fr_FR",
        "voice": "mls_1840",
        "quality": "low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/fr/fr_FR/mls_1840/low/speaker_0.mp3"
    },
    # German voices
    {
        "id": "de_DE-thorsten-medium",
        "name": "German - Male",
        "description": "Clear German male voice. Perfect for: German NPCs, Central European campaigns",
        "language": "de/de_DE",
        "voice": "thorsten",
        "quality": "medium",
        "size_mb": 87,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/de/de_DE/thorsten/medium/speaker_0.mp3"
    },
    {
        "id": "de_DE-eva_k-x_low",
        "name": "German - Female",
        "description": "German female voice. Perfect for: German NPCs, Merchants, Scholars",
        "language": "de/de_DE",
        "voice": "eva_k",
        "quality": "x_low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/de/de_DE/eva_k/x_low/speaker_0.mp3"
    },
    # Japanese voices
    {
        "id": "ja_JP-natsunatsu-medium",
        "name": "Japanese - Female",
        "description": "Japanese female voice. Perfect for: Japanese campaigns, Asian-inspired NPCs",
        "language": "ja/ja_JP",
        "voice": "natsunatsu",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/ja/ja_JP/natsunatsu/medium/speaker_0.mp3"
    },
    # Italian voices
    {
        "id": "it_IT-riccardo-x_low",
        "name": "Italian - Male",
        "description": "Italian male voice. Perfect for: Italian NPCs, Mediterranean campaigns",
        "language": "it/it_IT",
        "voice": "riccardo",
        "quality": "x_low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/it/it_IT/riccardo/x_low/speaker_0.mp3"
    },
    # Portuguese voices
    {
        "id": "pt_BR-faber-medium",
        "name": "Portuguese (Brazil) - Male",
        "description": "Brazilian Portuguese voice. Perfect for: Portuguese NPCs, South American campaigns",
        "language": "pt/pt_BR",
        "voice": "faber",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/pt/pt_BR/faber/medium/speaker_0.mp3"
    },
    # Russian voices
    {
        "id": "ru_RU-dmitri-medium",
        "name": "Russian - Male",
        "description": "Russian male voice. Perfect for: Slavic-inspired campaigns, Eastern NPCs",
        "language": "ru/ru_RU",
        "voice": "dmitri",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/ru/ru_RU/dmitri/medium/speaker_0.mp3"
    },
    # Dutch voices
    {
        "id": "nl_NL-mls_5809-low",
        "name": "Dutch - Male",
        "description": "Dutch male voice. Perfect for: Dutch NPCs, Low Countries campaigns",
        "language": "nl/nl_NL",
        "voice": "mls_5809",
        "quality": "low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/nl/nl_NL/mls_5809/low/speaker_0.mp3"
    },
    # Polish voices
    {
        "id": "pl_PL-mls_6892-low",
        "name": "Polish - Male",
        "description": "Polish male voice. Perfect for: Slavic campaigns, Eastern European NPCs",
        "language": "pl/pl_PL",
        "voice": "mls_6892",
        "quality": "low",
        "size_mb": 18,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/pl/pl_PL/mls_6892/low/speaker_0.mp3"
    },
    # Swedish voices
    {
        "id": "sv_SE-nst-medium",
        "name": "Swedish - Male",
        "description": "Swedish male voice. Perfect for: Nordic campaigns, Scandinavian NPCs",
        "language": "sv/sv_SE",
        "voice": "nst",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/sv/sv_SE/nst/medium/speaker_0.mp3"
    },
    # Danish voices
    {
        "id": "da_DK-talesyntese-medium",
        "name": "Danish - Male",
        "description": "Danish male voice. Perfect for: Nordic campaigns, Scandinavian NPCs, Danish characters",
        "language": "da/da_DK",
        "voice": "talesyntese",
        "quality": "medium",
        "size_mb": 51,
        "sample_url": "https://rhasspy.github.io/piper-samples/samples/da/da_DK/talesyntese/medium/speaker_0.mp3"
    }
]


class AudioDeviceManager:
    """
    Manages Windows audio device switching for Discord integration.
    Handles automatic device switching and restoration for "Send to Discord" feature.
    """

    def __init__(self, app_instance=None):
        self.original_output_device_id = None
        self.original_output_device_name = None
        self.original_input_device_id = None
        self.original_input_device_name = None
        self.is_discord_mode = False
        self.pycaw_available = PYCAW_AVAILABLE
        self.app_instance = app_instance  # Reference to main app for config loading

    def get_all_recording_devices(self):
        """Get list of all recording devices"""
        if not self.pycaw_available:
            return []

        try:
            # Initialize COM for this thread
            from comtypes import CoInitialize, CoUninitialize
            CoInitialize()

            devices = []

            # Use pycaw's GetAllDevices() which provides friendly names
            from pycaw.pycaw import AudioUtilities
            all_devices = AudioUtilities.GetAllDevices()

            for device in all_devices:
                # Filter by device ID prefix:
                # {0.0.0.00000000}.{guid} = render/output device
                # {0.0.1.00000000}.{guid} = capture/input device
                if device.id.startswith('{0.0.1.'):
                    # Check if device is active - state is an enum (AudioDeviceState.Active)
                    # Convert enum to string and check
                    state_str = str(device.state)
                    if 'Active' not in state_str:
                        print(f"DEBUG: Skipping inactive device: {device.FriendlyName} (state={device.state})")
                        continue

                    # Get the endpoint for this device
                    try:
                        device_enumerator = AudioUtilities.GetDeviceEnumerator()
                        endpoint = device_enumerator.GetDevice(device.id)

                        devices.append({
                            'id': device.id,
                            'name': device.FriendlyName,
                            'endpoint': endpoint
                        })
                        print(f"DEBUG: Found ACTIVE capture device: {device.FriendlyName}")
                    except Exception as ex:
                        print(f"DEBUG: Could not get endpoint for {device.id}: {ex}")
                        continue

            return devices
        except Exception as e:
            print(f"Error getting recording devices: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_current_default_device(self):
        """Get the current default recording device"""
        if not self.pycaw_available:
            return None

        try:
            # Initialize COM for this thread
            from comtypes import CoInitialize, CoUninitialize
            CoInitialize()

            device_enumerator = AudioUtilities.GetDeviceEnumerator()
            default_device = device_enumerator.GetDefaultAudioEndpoint(
                EDataFlow.eCapture.value,  # Recording devices
                ERole.eConsole.value       # Default device
            )

            device_id = default_device.GetId()

            # Get friendly name from Windows Registry
            try:
                import winreg
                reg_path = f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\Capture\\{device_id}"
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                try:
                    name, _ = winreg.QueryValueEx(key, "FriendlyName")
                except:
                    name, _ = winreg.QueryValueEx(key, "DeviceDesc")
                winreg.CloseKey(key)
                if ';' in name:
                    name = name.split(';')[-1]
            except:
                name = device_id

            return {
                'id': device_id,
                'name': name,
                'endpoint': default_device
            }
        except Exception as e:
            print(f"Error getting default device: {e}")
            return None

    def set_default_device(self, device_id):
        """Set a device as the default recording device"""
        if not self.pycaw_available:
            return False

        try:
            # Initialize COM for this thread
            from comtypes import CoInitialize, CoUninitialize, CoCreateInstance, GUID
            from ctypes import create_unicode_buffer
            CoInitialize()

            # Use the IPolicyConfig interface we defined at the top of the file
            # to set the default audio device
            # Convert CLSID string to GUID object
            clsid = GUID('{870af99c-171d-4f9e-af0d-e63df40c2bc9}')  # CLSID_CPolicyConfigClient
            policy_config = CoCreateInstance(
                clsid,
                IPolicyConfig,
                CLSCTX_ALL
            )

            # Convert device_id string to a unicode buffer that ctypes can work with
            device_id_buffer = create_unicode_buffer(device_id)

            # Set as default for all roles
            policy_config.SetDefaultEndpoint(device_id_buffer, ERole.eConsole.value)
            policy_config.SetDefaultEndpoint(device_id_buffer, ERole.eMultimedia.value)
            policy_config.SetDefaultEndpoint(device_id_buffer, ERole.eCommunications.value)

            return True
        except Exception as e:
            print(f"Error setting default device: {e}")
            import traceback
            traceback.print_exc()
            return False

    def find_virtual_cable(self):
        """Find VB-CABLE or similar virtual audio device using saved config"""
        devices = self.get_all_recording_devices()

        # Debug: print all detected devices
        print(f"DEBUG: Found {len(devices)} recording devices:")
        for device in devices:
            print(f"  - {device['name']}")

        # First, check if user has configured a specific device
        saved_device_id = None
        if self.app_instance:
            saved_device_id = self.app_instance.load_discord_config()

        if saved_device_id:
            print(f"DEBUG: Using saved virtual cable: {saved_device_id}")
            # Find the saved device in the list
            for device in devices:
                if device['id'] == saved_device_id:
                    print(f"DEBUG: Found saved virtual cable")
                    return device
            print(f"DEBUG: Saved device not found - may have been unplugged")

        # Fallback: try auto-detection (probably won't work without friendly names)
        print("DEBUG: No configured virtual cable - auto-detection not reliable")
        print("DEBUG: Please use '⚙️ Configure Discord' button to select your virtual cable")
        return None

    def get_cable_input_device(self):
        """Find CABLE Input (playback device) - the device we PLAY audio TO"""
        if not self.pycaw_available:
            return None

        try:
            from comtypes import CoInitialize
            CoInitialize()

            # Get all playback devices (render/output devices)
            from pycaw.pycaw import AudioUtilities
            all_devices = AudioUtilities.GetAllDevices()

            for device in all_devices:
                # Filter for OUTPUT devices (playback)
                # {0.0.0.00000000}.{guid} = render/output device
                if device.id.startswith('{0.0.0.'):
                    # Check if active
                    state_str = str(device.state)
                    if 'Active' not in state_str:
                        continue

                    # Look for CABLE Input
                    if 'CABLE Input' in device.FriendlyName:
                        print(f"DEBUG: Found CABLE Input: {device.FriendlyName}")
                        device_enumerator = AudioUtilities.GetDeviceEnumerator()
                        endpoint = device_enumerator.GetDevice(device.id)
                        return {
                            'id': device.id,
                            'name': device.FriendlyName,
                            'endpoint': endpoint
                        }

            print("DEBUG: CABLE Input not found - is VB-CABLE installed?")
            return None

        except Exception as e:
            print(f"Error finding CABLE Input: {e}")
            return None

    def switch_to_virtual_cable(self):
        """Switch default OUTPUT to CABLE Input and INPUT to CABLE Output for Discord"""
        try:
            from comtypes import CoInitialize
            CoInitialize()

            device_enumerator = AudioUtilities.GetDeviceEnumerator()

            # Save current OUTPUT device (speakers)
            output_device = device_enumerator.GetDefaultAudioEndpoint(
                0,  # eRender = 0 (playback/output devices)
                ERole.eConsole.value
            )
            self.original_output_device_id = output_device.GetId()

            # Save current INPUT device (microphone)
            input_device = device_enumerator.GetDefaultAudioEndpoint(
                1,  # eCapture = 1 (recording/input devices)
                ERole.eConsole.value
            )
            self.original_input_device_id = input_device.GetId()

            # Get friendly names
            all_devices = AudioUtilities.GetAllDevices()
            for dev in all_devices:
                if dev.id == self.original_output_device_id:
                    self.original_output_device_name = dev.FriendlyName
                if dev.id == self.original_input_device_id:
                    self.original_input_device_name = dev.FriendlyName

            print(f"DEBUG: Current OUTPUT: {self.original_output_device_name}")
            print(f"DEBUG: Current INPUT: {self.original_input_device_name}")

        except Exception as e:
            print(f"Error getting current devices: {e}")
            return False, "Could not detect current audio devices"

        # Find CABLE Input (OUTPUT/playback device - where we PLAY audio TO)
        cable_input = self.get_cable_input_device()
        if not cable_input:
            return False, "CABLE Input not found. Please install VB-CABLE."

        # Find CABLE Output (INPUT/recording device - where Discord RECORDS FROM)
        cable_output = self.find_virtual_cable()
        if not cable_output:
            return False, "CABLE Output not found. Please configure with ⚙️ button."

        # Switch OUTPUT to CABLE Input (so audio plays through cable)
        print(f"DEBUG: Switching OUTPUT to {cable_input['name']}")
        success1 = self.set_default_device(cable_input['id'])

        # Switch INPUT to CABLE Output (so Discord hears it)
        print(f"DEBUG: Switching INPUT to {cable_output['name']}")
        success2 = self.set_default_device(cable_output['id'])

        if success1 and success2:
            self.is_discord_mode = True
            return True, f"Audio routing through virtual cable"
        else:
            return False, "Failed to switch audio devices"

    def restore_original_device(self):
        """Restore original OUTPUT (speakers) and INPUT (microphone) devices"""
        if not self.original_output_device_id or not self.original_input_device_id:
            return False, "No original devices to restore"

        # Restore OUTPUT device (speakers)
        print(f"DEBUG: Restoring OUTPUT to {self.original_output_device_name}")
        success1 = self.set_default_device(self.original_output_device_id)

        # Restore INPUT device (microphone)
        print(f"DEBUG: Restoring INPUT to {self.original_input_device_name}")
        success2 = self.set_default_device(self.original_input_device_id)

        if success1 and success2:
            output_name = self.original_output_device_name
            input_name = self.original_input_device_name
            self.original_output_device_id = None
            self.original_output_device_name = None
            self.original_input_device_id = None
            self.original_input_device_name = None
            self.is_discord_mode = False
            return True, f"Restored speakers and microphone"
        else:
            return False, "Failed to restore audio devices"

    def emergency_reset(self):
        """Emergency reset - find first real microphone and use it"""
        devices = self.get_all_recording_devices()

        # Filter out virtual cables
        real_mics = [d for d in devices if not any(
            keyword in d['name'].lower()
            for keyword in ['cable', 'voicemeeter', 'virtual', 'vac']
        )]

        if not real_mics:
            return False, "No real microphone found"

        # Use first real mic
        success = self.set_default_device(real_mics[0]['id'])
        if success:
            self.original_device_id = None
            self.original_device_name = None
            self.is_discord_mode = False
            return True, f"Reset to '{real_mics[0]['name']}'"
        else:
            return False, "Emergency reset failed"


class TTRPGVoiceLab(ctk.CTk):
    """Main application class for TTRPG Voice Lab"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("The Artificer - TTS Voice Generator")
        self.geometry("1280x1000")
        self.minsize(1280, 700)  # Set minimum window size

        # Initialize pygame mixer for audio playback (if available)
        if PYGAME_AVAILABLE:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)

        # Application state
        self.current_preset: Optional[Dict[str, Any]] = None
        self.presets: list = []
        self.temp_files: list = []
        self.is_generating = False
        self.is_sending_to_discord = False  # Track Discord playback state

        # Initialize audio device manager for Discord integration
        self.audio_device_manager = AudioDeviceManager(app_instance=self)

        # Paths - handle both development and PyInstaller frozen app
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # For PyInstaller onedir builds, models/presets are next to the EXE
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

        # Force window to render and update layout properly
        self.update()  # Full update instead of just idletasks

        # Force geometry recalculation
        self.geometry("1280x1000")
        self.update_idletasks()

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
        # Configure grid layout - 3 columns: left sidebar, main content, right sidebar
        self.grid_columnconfigure(0, weight=0)  # Left sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # Main content - expands
        self.grid_columnconfigure(2, weight=0)  # Right sidebar - fixed width
        self.grid_rowconfigure(0, weight=1)  # Main content area
        self.grid_rowconfigure(1, weight=0)  # Status bar at bottom

        # Left sidebar for presets
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=1, sticky="nsew")

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

        # Speech controls frame - Row 2
        self.controls_frame_speech = ctk.CTkFrame(self.main_frame)
        self.controls_frame_speech.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.controls_frame_speech.grid_columnconfigure(0, weight=1)

        # Sentence Silence slider
        ctk.CTkLabel(
            self.controls_frame_speech,
            text="Sentence Pause:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, padx=5, pady=(10, 5), sticky="w")

        self.sentence_silence_slider = ctk.CTkSlider(
            self.controls_frame_speech,
            from_=0,
            to=2.0,
            number_of_steps=40,
            command=self.update_sentence_silence_label
        )
        self.sentence_silence_slider.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.sentence_silence_slider.set(0.75)  # Default Piper value

        self.sentence_silence_value_label = ctk.CTkLabel(
            self.controls_frame_speech,
            text="0.75s"
        )
        self.sentence_silence_value_label.grid(row=2, column=0, padx=5, pady=(0, 10))

        # Effect controls frame - Row 3
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
        self.button_frame.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
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

        # Discord integration buttons (row 1)
        self.send_to_discord_button = ctk.CTkButton(
            self.button_frame,
            text="🎙️ Send to Discord",
            command=self.send_to_discord,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#5865F2",  # Discord blurple
            hover_color="#4752C4"
        )
        self.send_to_discord_button.grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")

        # Cancel button (initially hidden)
        self.cancel_discord_button = ctk.CTkButton(
            self.button_frame,
            text="⏹️ Cancel & Restore Mic",
            command=self.cancel_discord_playback,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#ED4245",  # Discord red
            hover_color="#C03537"
        )
        self.cancel_discord_button.grid(row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="ew")
        self.cancel_discord_button.grid_remove()  # Hide initially

        # Discord status indicator
        self.discord_status_label = ctk.CTkLabel(
            self.button_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.discord_status_label.grid(row=2, column=0, columnspan=2, pady=(0, 5))

        # Show/hide Discord buttons based on pycaw availability
        if not PYCAW_AVAILABLE:
            self.send_to_discord_button.configure(state="disabled", text="🎙️ Discord (Not Available)")
            self.discord_status_label.configure(
                text="Install pycaw for Discord integration (Windows only)",
                text_color="orange"
            )

        # Right sidebar for voice models
        self.voice_sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.voice_sidebar.grid(row=0, column=2, rowspan=1, sticky="nsew")

        # Voice sidebar title
        voice_sidebar_title = ctk.CTkLabel(
            self.voice_sidebar,
            text="Voice Models",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        voice_sidebar_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Voice Model label
        ctk.CTkLabel(
            self.voice_sidebar,
            text="Select Voice:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        # Voice selector dropdown
        self.voice_selector = ctk.CTkComboBox(
            self.voice_sidebar,
            values=["No models found"],
            command=self.on_voice_selected,
            state="readonly"
        )
        self.voice_selector.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Download Voices button
        self.download_voices_btn = ctk.CTkButton(
            self.voice_sidebar,
            text="Download Voices",
            command=self.open_voice_downloader,
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self.download_voices_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Currently selected voice label
        ctk.CTkLabel(
            self.voice_sidebar,
            text="Currently Selected:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")

        self.selected_voice_label = ctk.CTkLabel(
            self.voice_sidebar,
            text="No voice selected",
            font=ctk.CTkFont(size=11),
            wraplength=210,
            anchor="w",
            justify="left",
            text_color="gray70"
        )
        self.selected_voice_label.grid(row=5, column=0, padx=20, pady=(0, 5), sticky="w")

        # Voice description label
        ctk.CTkLabel(
            self.voice_sidebar,
            text="About This Voice:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=6, column=0, padx=20, pady=(5, 5), sticky="w")

        # Voice description text (wrapped)
        self.voice_description_label = ctk.CTkLabel(
            self.voice_sidebar,
            text="Select a voice to see description",
            font=ctk.CTkFont(size=11),
            wraplength=210,
            anchor="w",
            justify="left"
        )
        self.voice_description_label.grid(row=7, column=0, padx=20, pady=(0, 10), sticky="nw")

        # Emergency reset audio button (Discord integration)
        self.reset_audio_btn = ctk.CTkButton(
            self.voice_sidebar,
            text="🔧 Reset Audio Device",
            command=self.emergency_reset_audio,
            height=35,
            fg_color="#ED4245",  # Discord red
            hover_color="#C03537"
        )
        self.reset_audio_btn.grid(row=8, column=0, padx=20, pady=(20, 5), sticky="ew")

        # Show/hide reset button based on pycaw availability
        if not PYCAW_AVAILABLE:
            self.reset_audio_btn.grid_remove()

        # Configure Discord button
        self.configure_discord_btn = ctk.CTkButton(
            self.voice_sidebar,
            text="⚙️ Configure Discord",
            command=self.configure_discord_device,
            height=35,
            fg_color="#5865F2",
            hover_color="#4752C4"
        )
        self.configure_discord_btn.grid(row=9, column=0, padx=20, pady=(5, 5), sticky="ew")

        # Show/hide configure button based on pycaw availability
        if not PYCAW_AVAILABLE:
            self.configure_discord_btn.grid_remove()

        # Discord Setup Guide button
        self.discord_guide_btn = ctk.CTkButton(
            self.voice_sidebar,
            text="📖 Discord Setup Guide",
            command=self.open_discord_guide,
            height=35,
            fg_color="#5865F2",
            hover_color="#4752C4"
        )
        self.discord_guide_btn.grid(row=10, column=0, padx=20, pady=(5, 5), sticky="ew")

        # About / License button
        self.about_btn = ctk.CTkButton(
            self.voice_sidebar,
            text="About / License",
            command=self.show_about_dialog,
            height=35,
            fg_color="gray30",
            hover_color="gray20"
        )
        self.about_btn.grid(row=11, column=0, padx=20, pady=(5, 20), sticky="ew")

        # Status bar at bottom of window
        status_bar_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        status_bar_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.status_label = ctk.CTkLabel(
            status_bar_frame,
            text="Ready",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        # Populate voice models (moved to after status_label creation)
        self.voice_models = {}  # Dictionary: display_name -> model_path

        # Load voice models after status_label is created
        self.load_voice_models()

    def update_speech_rate_label(self, value):
        """Update speech rate slider label"""
        self.speech_rate_value_label.configure(text=f"{float(value):.1f}x")

    def update_sentence_silence_label(self, value):
        """Update sentence silence slider label"""
        self.sentence_silence_value_label.configure(text=f"{float(value):.2f}s")

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

            # Update description for first voice
            self.on_voice_selected(voice_names[0])

    def on_voice_selected(self, choice):
        """Handle voice model selection"""
        if choice in self.voice_models:
            # Update selected voice label in sidebar
            self.selected_voice_label.configure(text=choice)
            self.status_label.configure(text="Ready")

            # Update voice description
            model_path = self.voice_models[choice]
            model_filename = Path(model_path).stem  # Get filename without extension

            # Find matching voice in catalog
            description = "No description available"
            for voice in VOICE_CATALOG:
                if voice['id'] == model_filename:
                    description = voice['description']
                    break

            self.voice_description_label.configure(text=description)

    def open_voice_downloader(self):
        """Open the voice downloader dialog"""
        dialog = VoiceDownloaderDialog(self, self.models_dir)
        dialog.wait_window()  # Wait for dialog to close

        # Refresh voice models after dialog closes
        self.load_voice_models()

    def load_discord_config(self):
        """Load Discord virtual cable configuration from config file"""
        try:
            if getattr(sys, 'frozen', False):
                config_path = Path(sys.executable).parent / 'discord_config.json'
            else:
                config_path = Path(__file__).parent.parent / 'discord_config.json'

            if config_path.exists():
                import json
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('virtual_cable_device_id')
        except Exception as e:
            print(f"Error loading Discord config: {e}")
        return None

    def save_discord_config(self, device_id):
        """Save Discord virtual cable configuration to config file"""
        try:
            if getattr(sys, 'frozen', False):
                config_path = Path(sys.executable).parent / 'discord_config.json'
            else:
                config_path = Path(__file__).parent.parent / 'discord_config.json'

            import json
            config = {'virtual_cable_device_id': device_id}
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving Discord config: {e}")
            return False

    def configure_discord_device(self):
        """Show dialog to configure which device is the virtual cable"""
        if not PYCAW_AVAILABLE:
            messagebox.showerror("Error", "Discord integration not available (pycaw not installed)")
            return

        # Get all recording devices
        try:
            devices = self.audio_device_manager.get_all_recording_devices()
            print(f"DEBUG configure_discord_device: Got {len(devices)} devices")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enumerate audio devices:\n{e}")
            return

        if not devices or len(devices) == 0:
            messagebox.showerror("Error", "No recording devices found.\n\nMake sure you have a microphone or virtual cable installed.")
            return

        # Create configuration dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Configure Discord Virtual Cable")
        dialog.geometry("600x400")
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Instructions
        instructions = ctk.CTkLabel(
            dialog,
            text="Select your virtual audio cable device (e.g., VB-CABLE Output):",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=550
        )
        instructions.pack(pady=20, padx=20)

        # List of devices - use scrollable frame
        device_list_frame = ctk.CTkScrollableFrame(dialog, width=560, height=250)
        device_list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        selected_device = ctk.StringVar(value="")

        print(f"DEBUG: Creating radio buttons for {len(devices)} devices")
        for idx, device in enumerate(devices):
            # Show friendly device name
            device_label = device['name']
            print(f"DEBUG: Adding radio button: {device_label}")

            radio = ctk.CTkRadioButton(
                device_list_frame,
                text=device_label,
                variable=selected_device,
                value=device['id']
            )
            radio.pack(pady=5, padx=10, anchor="w", fill="x")

        print(f"DEBUG: Finished adding {len(devices)} radio buttons")

        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=20, padx=20, fill="x")

        def save_selection():
            device_id = selected_device.get()
            if not device_id:
                messagebox.showwarning("No Selection", "Please select a device")
                return

            if self.save_discord_config(device_id):
                messagebox.showinfo("Success", "Virtual cable configured successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save configuration")

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_selection,
            height=40,
            fg_color="#5865F2",
            hover_color="#4752C4"
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            height=40,
            fg_color="gray30",
            hover_color="gray20"
        )
        cancel_btn.pack(side="left", padx=5)

    def open_discord_guide(self):
        """Open the Discord setup guide (VB-CABLE installation help)"""
        try:
            # Use same path logic as base_dir for consistency
            if getattr(sys, 'frozen', False):
                # Running as compiled executable - docs are next to EXE
                base_path = Path(sys.executable).parent
            else:
                # Running as script
                base_path = Path(__file__).parent.parent

            setup_guide_path = base_path / 'docs' / 'vb-cable-setup.html'

            if setup_guide_path.exists():
                # Open local HTML file
                webbrowser.open(f'file://{setup_guide_path.absolute()}')
            else:
                # Fallback to online VB-Audio website if HTML file not found
                webbrowser.open("https://vb-audio.com/Cable/")
        except Exception as e:
            # Fallback to online VB-Audio website
            webbrowser.open("https://vb-audio.com/Cable/")

    def show_about_dialog(self):
        """Show About/License dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("About - The Artificer")
        dialog.geometry("600x500")
        dialog.resizable(False, False)

        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()

        # Configure grid
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        # Header frame
        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # App title
        title = ctk.CTkLabel(
            header_frame,
            text="The Artificer - TTS Voice Generator",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(0, 5))

        # Version
        version = ctk.CTkLabel(
            header_frame,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=12)
        )
        version.pack(pady=(0, 10))

        # Copyright
        copyright_text = ctk.CTkLabel(
            header_frame,
            text="Copyright © 2025 Michael (BahneGork)",
            font=ctk.CTkFont(size=11)
        )
        copyright_text.pack()

        # License info frame with scrollable text
        info_frame = ctk.CTkFrame(dialog)
        info_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_rowconfigure(0, weight=1)

        # Create scrollable text widget
        license_text = ctk.CTkTextbox(info_frame, wrap="word", font=ctk.CTkFont(size=11))
        license_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # License content
        content = """LICENSE

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program in the LICENSE file. If not, see <https://www.gnu.org/licenses/>.

SOURCE CODE

The complete source code is available at:
https://github.com/BahneGork/the-artificer-tts-generator

THIRD-PARTY COMPONENTS

This application uses the following open-source libraries:

• Pedalboard (Spotify AB) - GPL v3
• Piper TTS (Rhasspy) - MIT (with GPL espeak-ng)
• CustomTkinter (Tom Schimansky) - MIT
• Pydub - MIT
• NumPy - BSD 3-Clause
• PyInstaller - GPL v2 with exceptions
• audioop-lts - PSF License

Due to GPL v3 components, this entire application is licensed under GPL v3.

See THIRD_PARTY_LICENSES.txt for complete attribution and license details.

VOICE MODELS

Voice models are downloaded separately from HuggingFace (rhasspy/piper-voices). Each voice model has its own license. Users should review individual voice model licenses before commercial use.

Voice models are NOT distributed with this application.
"""

        license_text.insert("1.0", content)
        license_text.configure(state="disabled")  # Make read-only

        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=100,
            height=32
        )
        close_btn.grid(row=2, column=0, pady=(0, 20))

        # Center dialog on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Bring to front
        dialog.lift()
        dialog.focus_force()

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

            # Get sentence silence from slider
            sentence_silence = self.sentence_silence_slider.get()

            cmd = [
                str(piper_exe),
                '--model', model_path,
                '--output_file', str(temp_filename),
                '--length_scale', str(length_scale),
                '--sentence-silence', str(sentence_silence)
            ]

            # Run piper with text input
            # Hide console window on Windows
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                startupinfo=startupinfo
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

    def send_to_discord_thread(self):
        """Thread function for sending audio to Discord"""
        try:
            self.status_label.configure(text="Generating TTS for Discord...")
            self.is_sending_to_discord = True

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

            # Create temporary WAV file for playback
            temp_discord_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_discord_path = temp_discord_file.name
            temp_discord_file.close()
            self.temp_files.append(temp_discord_path)

            # Export processed audio
            processed_audio.export(temp_discord_path, format='wav')

            # Switch to virtual cable
            self.status_label.configure(text="Switching to virtual cable...")
            success, message = self.audio_device_manager.switch_to_virtual_cable()

            if not success:
                messagebox.showerror("Discord Error", f"{message}\n\nSetup instructions:\n1. Install VB-CABLE from vb-audio.com\n2. Set Discord input to 'Default'\n3. Restart this app")
                self.status_label.configure(text="Ready")
                return

            self.discord_status_label.configure(text=f"🎙️ {message}", text_color="#43B581")  # Discord green

            # Wait for Discord to detect device change
            import time
            time.sleep(0.5)

            # Play audio to virtual cable (this goes to Discord)
            self.status_label.configure(text="Playing to Discord...")

            # Give audio system time to stabilize after device switch
            time.sleep(1.0)

            # Use winsound for reliable Windows playback (built-in, no dependencies)
            import winsound

            # Play audio using Windows API (this is synchronous)
            # We'll use SND_ASYNC flag to play async so we can check for cancellation
            import threading
            playback_complete = threading.Event()

            def play_audio():
                try:
                    winsound.PlaySound(temp_discord_path, winsound.SND_FILENAME)
                except Exception as e:
                    print(f"Winsound playback error: {e}")
                finally:
                    playback_complete.set()

            # Start playback in separate thread
            playback_thread = threading.Thread(target=play_audio, daemon=True)
            playback_thread.start()

            # Wait for playback to finish or cancellation
            while not playback_complete.is_set():
                if not self.is_sending_to_discord:
                    # Cancelled - stop playback
                    winsound.PlaySound(None, winsound.SND_PURGE)
                    break
                time.sleep(0.1)

            # Restore original audio devices
            time.sleep(0.3)  # Brief pause before switching back
            self.status_label.configure(text="Restoring audio devices...")
            success, message = self.audio_device_manager.restore_original_device()

            if success:
                self.discord_status_label.configure(text=f"✓ {message}", text_color="#43B581")
                self.status_label.configure(text="Discord playback complete - Ready")
            else:
                self.discord_status_label.configure(text=f"⚠️ {message}", text_color="orange")
                self.status_label.configure(text="Warning: Could not restore audio - Ready")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Discord error: {error_details}")

            # Try to restore microphone on error
            try:
                self.audio_device_manager.restore_original_device()
            except:
                pass

            messagebox.showerror("Error", f"Discord playback failed: {str(e)}")
            self.discord_status_label.configure(text="❌ Playback failed", text_color="red")
            self.status_label.configure(text="Error - Ready")

        finally:
            self.is_sending_to_discord = False
            self.send_to_discord_button.grid()
            self.cancel_discord_button.grid_remove()
            self.send_to_discord_button.configure(state="normal")

    def send_to_discord(self):
        """Send audio to Discord via virtual cable"""
        if self.is_generating or self.is_sending_to_discord:
            messagebox.showinfo("Info", "Audio generation in progress...")
            return

        if not PYCAW_AVAILABLE:
            messagebox.showerror("Not Available", "Discord integration requires pycaw library.\n\nInstall with: pip install pycaw comtypes")
            return

        # Check for virtual cable
        virtual_cable = self.audio_device_manager.find_virtual_cable()
        if not virtual_cable:
            messagebox.showinfo(
                "Configure Discord Integration",
                "Virtual audio cable not configured.\n\n"
                "Please click '⚙️ Configure Discord' button to select\n"
                "your virtual cable device (e.g., VB-CABLE Output).\n\n"
                "First time setup:\n"
                "1. Install VB-CABLE (see 📖 Discord Setup Guide)\n"
                "2. Click '⚙️ Configure Discord' to select the device\n"
                "3. Click '🎙️ Send to Discord' to use it"
            )
            return

        # Hide send button, show cancel button
        self.send_to_discord_button.grid_remove()
        self.cancel_discord_button.grid()
        self.send_to_discord_button.configure(state="disabled")

        # Start playback thread
        thread = threading.Thread(target=self.send_to_discord_thread, daemon=True)
        thread.start()

    def cancel_discord_playback(self):
        """Cancel Discord playback and restore microphone"""
        self.is_sending_to_discord = False
        self.status_label.configure(text="Cancelling...")

        # Restore microphone
        try:
            success, message = self.audio_device_manager.restore_original_device()
            if success:
                self.discord_status_label.configure(text=f"⏹️ Cancelled - {message}", text_color="orange")
            else:
                self.discord_status_label.configure(text=f"⚠️ {message}", text_color="red")
        except Exception as e:
            self.discord_status_label.configure(text=f"⚠️ Error restoring mic: {str(e)}", text_color="red")

        # Restore UI
        self.send_to_discord_button.grid()
        self.cancel_discord_button.grid_remove()
        self.send_to_discord_button.configure(state="normal")
        self.status_label.configure(text="Cancelled - Ready")

    def emergency_reset_audio(self):
        """Emergency reset - restore microphone if stuck on virtual cable"""
        if not PYCAW_AVAILABLE:
            messagebox.showerror("Not Available", "Audio device management not available on this system.")
            return

        # Get current device info
        current_device = self.audio_device_manager.get_current_default_device()
        if not current_device:
            messagebox.showerror("Error", "Could not detect current audio device.")
            return

        current_name = current_device['name']

        # Check if currently on virtual cable
        is_on_virtual = any(
            keyword in current_name.lower()
            for keyword in ['cable', 'voicemeeter', 'virtual', 'vac']
        )

        if is_on_virtual:
            # Stuck on virtual cable - emergency reset
            response = messagebox.askyesno(
                "Emergency Reset",
                f"Current input device: {current_name}\n\n"
                "This appears to be a virtual cable.\n"
                "Reset to your real microphone?\n\n"
                "Note: This will find and switch to your first real microphone."
            )

            if not response:
                return

            success, message = self.audio_device_manager.emergency_reset()

            if success:
                messagebox.showinfo("Success", f"Audio device reset!\n\n{message}")
                self.discord_status_label.configure(text=f"🔧 {message}", text_color="#43B581")
                self.status_label.configure(text="Audio device reset - Ready")
            else:
                messagebox.showerror("Error", f"Emergency reset failed:\n{message}")
                self.discord_status_label.configure(text="❌ Reset failed", text_color="red")

        else:
            # Not on virtual cable - show info dialog
            all_devices = self.audio_device_manager.get_all_recording_devices()

            device_list = "\n".join([f"• {d['name']}" for d in all_devices])

            messagebox.showinfo(
                "Audio Device Status",
                f"Current input device:\n{current_name}\n\n"
                "This appears to be your real microphone.\n\n"
                f"Available recording devices:\n{device_list}\n\n"
                "No reset needed. Use this button if your mic gets stuck on virtual cable after app crash."
            )

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


class VoiceDownloaderDialog(ctk.CTkToplevel):
    """Dialog for browsing and downloading voice models"""

    def __init__(self, parent, models_dir):
        super().__init__(parent)

        self.models_dir = models_dir
        self.voice_checkboxes = {}
        self.selected_voices = []
        self.is_downloading = False

        # Window configuration
        self.title("Download Voice Models")
        self.geometry("800x600")
        self.resizable(False, False)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        # Build UI
        self.build_ui()

        # Check which voices are already installed
        self.update_installed_voices()

        # Center window on parent and bring to front
        self.center_on_parent(parent)
        self.lift()  # Bring to front
        self.focus_force()  # Force keyboard focus
        self.after(10, lambda: self.lift())  # Ensure it stays on top

    def center_on_parent(self, parent):
        """Center the dialog on the parent window"""
        self.update_idletasks()  # Update window to get accurate dimensions

        # Get parent window position and size
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Get dialog size
        dialog_width = 800
        dialog_height = 600

        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        # Set position
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def build_ui(self):
        """Build the dialog UI"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Download Voice Models",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        # Info label
        info_label = ctk.CTkLabel(
            main_frame,
            text="Select voices to download. Click on voice name to hear a sample.",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(pady=(0, 10))

        # Scrollable frame for voice list
        self.scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            width=740,
            height=400
        )
        self.scroll_frame.pack(pady=(0, 10), fill="both", expand=True)

        # Populate voice list
        for voice in VOICE_CATALOG:
            self.create_voice_item(voice)

        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        # Download button
        self.download_btn = ctk.CTkButton(
            button_frame,
            text="Download Selected",
            command=self.download_selected,
            fg_color="green",
            hover_color="darkgreen",
            width=150
        )
        self.download_btn.pack(side="left", padx=5)

        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.destroy,
            width=150
        )
        close_btn.pack(side="right", padx=5)

        # Progress label
        self.progress_label = ctk.CTkLabel(
            button_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(side="left", padx=20)

    def create_voice_item(self, voice):
        """Create a voice item in the list"""
        # Frame for this voice
        voice_frame = ctk.CTkFrame(self.scroll_frame)
        voice_frame.pack(fill="x", pady=5, padx=5)
        voice_frame.grid_columnconfigure(1, weight=1)

        # Checkbox
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            voice_frame,
            text="",
            variable=var,
            width=30
        )
        checkbox.grid(row=0, column=0, padx=5, pady=5, rowspan=2)
        self.voice_checkboxes[voice['id']] = {'var': var, 'frame': voice_frame, 'voice': voice}

        # Voice name (clickable for sample)
        name_label = ctk.CTkLabel(
            voice_frame,
            text=voice['name'],
            font=ctk.CTkFont(size=14, weight="bold"),
            cursor="hand2",
            text_color="#3b8ed0"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=5)
        name_label.bind("<Button-1>", lambda e, url=voice['sample_url']: self.open_sample(url))

        # Description
        desc_label = ctk.CTkLabel(
            voice_frame,
            text=voice['description'],
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        desc_label.grid(row=1, column=1, sticky="w", padx=5)

        # Size
        size_label = ctk.CTkLabel(
            voice_frame,
            text=f"{voice['size_mb']} MB",
            font=ctk.CTkFont(size=11),
            width=80
        )
        size_label.grid(row=0, column=2, padx=5, pady=5, rowspan=2)

        # Status label (will show "Installed" or download progress)
        status_label = ctk.CTkLabel(
            voice_frame,
            text="",
            font=ctk.CTkFont(size=11),
            width=100
        )
        status_label.grid(row=0, column=3, padx=5, pady=5, rowspan=2)
        self.voice_checkboxes[voice['id']]['status_label'] = status_label

    def update_installed_voices(self):
        """Check and mark which voices are already installed"""
        if not self.models_dir.exists():
            return

        for voice_id, voice_data in self.voice_checkboxes.items():
            model_file = self.models_dir / f"{voice_id}.onnx"
            if model_file.exists():
                voice_data['status_label'].configure(text="✓ Installed", text_color="green")
                voice_data['var'].set(False)  # Uncheck installed voices
                voice_data['frame'].configure(fg_color="#1a4d2e")  # Darker green tint

    def open_sample(self, url):
        """Open voice sample in browser"""
        import webbrowser
        webbrowser.open(url)

    def download_selected(self):
        """Download selected voices"""
        if self.is_downloading:
            return

        # Get selected voices
        selected = [
            voice_data['voice']
            for voice_id, voice_data in self.voice_checkboxes.items()
            if voice_data['var'].get()
        ]

        if not selected:
            messagebox.showinfo("No Selection", "Please select at least one voice to download.")
            return

        # Calculate total size
        total_mb = sum(v['size_mb'] for v in selected)
        result = messagebox.askyesno(
            "Confirm Download",
            f"Download {len(selected)} voice model(s)?\n\nTotal size: {total_mb} MB"
        )

        if not result:
            return

        # Disable download button
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="Downloading...")

        # Start download in background thread
        download_thread = threading.Thread(
            target=self.download_voices_thread,
            args=(selected,),
            daemon=True
        )
        download_thread.start()

    def download_voices_thread(self, voices):
        """Download voices in background thread"""
        import urllib.request

        self.models_dir.mkdir(exist_ok=True)

        for idx, voice in enumerate(voices, 1):
            try:
                # Update progress label
                self.after(0, lambda: self.progress_label.configure(
                    text=f"Downloading {idx}/{len(voices)}: {voice['name']}"
                ))

                # Update voice status
                voice_id = voice['id']
                self.after(0, lambda vid=voice_id: self.voice_checkboxes[vid]['status_label'].configure(
                    text="Downloading...", text_color="orange"
                ))

                # Build download URLs
                base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{voice['language']}/{voice['voice']}/{voice['quality']}"

                # Download .onnx file
                onnx_url = f"{base_url}/{voice['id']}.onnx"
                onnx_path = self.models_dir / f"{voice['id']}.onnx"
                urllib.request.urlretrieve(onnx_url, onnx_path)

                # Download .onnx.json file
                json_url = f"{base_url}/{voice['id']}.onnx.json"
                json_path = self.models_dir / f"{voice['id']}.onnx.json"
                urllib.request.urlretrieve(json_url, json_path)

                # Mark as complete
                self.after(0, lambda vid=voice_id: self.voice_checkboxes[vid]['status_label'].configure(
                    text="✓ Installed", text_color="green"
                ))
                self.after(0, lambda vid=voice_id: self.voice_checkboxes[vid]['frame'].configure(
                    fg_color="#1a4d2e"
                ))
                self.after(0, lambda vid=voice_id: self.voice_checkboxes[vid]['var'].set(False))

            except Exception as e:
                # Mark as failed
                self.after(0, lambda vid=voice_id, err=str(e): self.voice_checkboxes[vid]['status_label'].configure(
                    text="Failed", text_color="red"
                ))
                self.after(0, lambda err=str(e): messagebox.showerror(
                    "Download Error",
                    f"Failed to download {voice['name']}:\n{err}"
                ))

        # Re-enable download button
        self.after(0, lambda: self.progress_label.configure(text="Download complete!"))
        self.after(0, lambda: self.download_btn.configure(state="normal", text="Download Selected"))
        self.is_downloading = False


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
