# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for The Artificer - TTS Voice Generator
Build with: pyinstaller ttrpg_voice_lab.spec
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Include piper.exe and its DLL dependencies as binaries
binaries = []
piper_files = ['piper.exe', 'espeak-ng.dll', 'piper_phonemize.dll']
for piper_file in piper_files:
    if os.path.exists(piper_file):
        binaries.append((piper_file, '.'))

# Also include any other DLL files that might be in the project root
import glob
for dll in glob.glob('*.dll'):
    dll_name = os.path.basename(dll)
    if dll_name not in [b[0] for b in binaries]:  # Avoid duplicates
        binaries.append((dll, '.'))

# Collect necessary data files
datas = [
    ('presets', 'presets'),
]

# Include models folder if it exists (optional - users can add their own)
if os.path.exists('models'):
    datas.append(('models', 'models'))

# Include docs folder (VB-CABLE setup guide, etc.)
if os.path.exists('docs'):
    datas.append(('docs', 'docs'))

# Include espeak-ng-data if it exists
if os.path.exists('espeak-ng-data'):
    datas.append(('espeak-ng-data', 'espeak-ng-data'))

# Collect hidden imports for audio libraries
hiddenimports = [
    'piper',
    'pedalboard',
    'pydub',
    'pydub.playback',
    'pygame',
    'numpy',
    'customtkinter',
    'audioop_lts',  # Required for Python 3.13+
    'pycaw',  # Windows audio control for Discord integration
    'pycaw.pycaw',
    'comtypes',  # Required by pycaw
    'comtypes.client',
    'ctypes.wintypes',
]

# Add pedalboard data files
datas += collect_data_files('pedalboard')

# Add pycaw data files
try:
    datas += collect_data_files('pycaw')
except:
    pass  # pycaw might not have data files

a = Analysis(
    ['src/ttrpg_voice_lab.py'],
    pathex=[],
    binaries=binaries,
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
    console=False,  # No console window for GUI app
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
