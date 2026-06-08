# -*- mode: python ; coding: utf-8 -*-
# Digimon Time Stranger ToolKit - PyInstaller Spec
# Guidelines: [TS-002], [TS-003], [RC-001], [RC-002], [VC-001]

import os
from pathlib import Path

# Collect embedded Python runtime
internal_path = Path('_internal')
internal_datas = []
if internal_path.exists():
    for file_path in internal_path.rglob('*'):
        if file_path.is_file():
            rel_path = file_path.relative_to(internal_path)
            internal_datas.append((str(file_path), f'_internal/{rel_path}'))

# Collect DSCSToolsCLI.exe
dscs_binaries = []
if Path('DSCSToolsCLI.exe').exists():
    dscs_binaries.append(('DSCSToolsCLI.exe', '.'))

# Collect unluac jar
unluac_datas = []
if Path('unluac_2023_12_24.jar').exists():
    unluac_datas.append(('unluac_2023_12_24.jar', '.'))

# Collect Lua scripts
lua_datas = []
lua_path = Path('LUA')
if lua_path.exists():
    for file_path in lua_path.rglob('*.lua'):
        rel_path = file_path.relative_to(lua_path)
        lua_datas.append((str(file_path), f'LUA/{rel_path}'))

# Collect batch launchers
bat_datas = []
for bat_file in ['decompile_lua.bat', 'Lua_Decompiler.bat', 'Launch_MVGL_GUI.bat']:
    if Path(bat_file).exists():
        bat_datas.append((bat_file, '.'))

# Combine all datas
all_datas = internal_datas + unluac_datas + lua_datas + bat_datas

a = Analysis(
    ['digimon_editor.py'],
    pathex=[],
    binaries=dscs_binaries,
    datas=all_datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'csv',
        'json',
        'pathlib',
        'dataclasses',
        'typing',
        'shutil',
        're',
        'os',
        'sys',
        'copy',
        'textwrap',
        'tempfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'unittest',
        'doctest',
    ],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='digimon_editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
