# Utilities Reference

## Overview

This repository contains **4 application-level tools** and **3 supporting infrastructure components** for modding *Digimon Story Time Stranger*.

---

## Application-Level Tools

| # | Tool | Framework | Purpose |
|---|------|-----------|---------|
| 1 | `digimon_editor.py` | PyQt6 | Full Digimon editor with tabs for stats, skills, traits, model, evolution, and battle data. Supports Base/DLC/dsts-loader workflows. |
| 2 | `MBE_Editor.py` | PyQt6 | Direct binary MBE file editor. Open/save `.mbe` directories or CSV, multi-sheet tabbed view, search/replace, and column-type-aware parsing (`int`, `short`, `byte`, `float`, `string`, `bool`). |
| 3 | `lua_decompiler_gui.py` | PyQt6 | Frontend for `unluac_2023_12_24.jar`. Batch-decompile `.lua` files from input directory to output directory with progress tracking and timeout safety. |
| 4 | `mvgl_tools_gui.py` | Tkinter | Frontend for `MVGLToolsCLI.exe`. Supports unpack/pack of MVGL, MBE, AFS2 archives, and file/save encryption/decryption across *Cyber Sleuth*, *Time Stranger*, and *The Hundred Line*. |

---

## Infrastructure / Backend Components

| # | Component | Type | Purpose |
|---|-----------|------|---------|
| 5 | `data_loader.py` | Python library | `MBELoader` parses `.mbe` CSV directories into `DigimonData` dataclasses. Handles digimon status, char info, skills, traits, evolutions, battles, growth curves, and text lookups. |
| 6 | `csv_exporter.py` | Python library | `CSVExporter` writes `DigimonData` back to the 9 required CSV files plus extended evolution/battle data. Also provides `repack_mbe_files` and `repack_dlc_mbe_files` helpers. |
| 7 | `DSCSToolsCLI.exe` | Bundled external CLI | Game-specific converter between raw MBE binary and CSV. Used under the hood for format conversion when needed. |
| 8 | `CPKBrowser.exe` | Bundled external CLI | CPK archive inspector/browser for game data extraction. |
| 9 | `external/MVGLTools` | Git submodule | Upstream repo for `MVGLToolsCLI.exe` — MVGL/MBE/AFS2 pack, unpack, encrypt, decrypt for DSTS and related Media.Vision games. |
| 10 | `external/DSTS-Mod-Tool` | Git submodule | All-in-one GUI tool for DSTS modding — MVGL model extraction, CPK, MBE, IMG, TEXT processing, and mod loader integration. |

---

## Launcher Batches

| File | Target |
|------|--------|
| `decompile_lua.bat` | Lua decompilation entry point |
| `Lua_Decompiler.bat` | Alternative Lua decompiler launcher |
| `Launch_MVGL_GUI.bat` | MVGL Tools GUI launcher |

---

## Tool Dependency Graph

```
digimon_editor.py
  ├── data_loader.py  (MBELoader, DigimonData, DLCExporter)
  └── csv_exporter.py (CSVExporter, repack helpers)

MBE_Editor.py
  └── (standalone direct MBE/CSV parser)

lua_decompiler_gui.py
  └── unluac_2023_12_24.jar

mvgl_tools_gui.py
  └── MVGLToolsCLI.exe
```

---

## File-Type Summary

- **Python sources (6):** `digimon_editor.py`, `data_loader.py`, `csv_exporter.py`, `MBE_Editor.py`, `lua_decompiler_gui.py`, `mvgl_tools_gui.py`
- **Executables (6):** `digimon_editor.exe`, `MBE_Editor.exe`, `lua_decompiler_gui.exe`, `mvgl_tools_gui.exe`, `DSCSToolsCLI.exe`, `CPKBrowser.exe`
- **Batches (3):** `decompile_lua.bat`, `Lua_Decompiler.bat`, `Launch_MVGL_GUI.bat`

---

*Generated: 2026-06-08*
*Project: Digimon Time Stranger ToolKit*
