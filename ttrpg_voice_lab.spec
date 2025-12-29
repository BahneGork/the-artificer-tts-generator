# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for The Artificer - TTS Voice Generator
Build with: pyinstaller ttrpg_voice_lab.spec
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect necessary data files
datas = [
    ('presets', 'presets'),
    ('models', 'models'),
]

# Collect hidden imports for audio libraries
hiddenimports = [
    'piper',
    'pedalboard',
    'pydub',
    'pygame',
    'numpy',
    'customtkinter',
]

# Add pedalboard data files
datas += collect_data_files('pedalboard')

a = Analysis(
    ['src/ttrpg_voice_lab.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TTRPGVoiceLab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TTRPGVoiceLab',
)
