# INDEX.md - Digimon Time Stranger ToolKit

## Repository Root

| File/Dir | Purpose |
|----------|---------|
| `digimon_editor.py` | Main Digimon editor GUI (PyQt6). Edit stats, skills, traits, evolutions, model, and battle data. |
| `MBE_Editor.py` | Direct binary MBE file/CSV editor (PyQt6). Multi-sheet viewer/editor with search. |
| `lua_decompiler_gui.py` | Lua decompiler GUI (PyQt6). Batch decompile `.lua` via `unluac_2023_12_24.jar`. |
| `mvgl_tools_gui.py` | MVGL/CPK/MBE/AFS2 tool GUI (Tkinter). Frontend for `MVGLToolsCLI.exe`. |
| `data_loader.py` | Data loading library. `MBELoader` parses `.mbe` CSV dirs into `DigimonData`. |
| `csv_exporter.py` | Export library. `CSVExporter` writes `DigimonData` back to 9 required CSV files. |
| `dts_launcher.py` | Unified launcher dashboard for all 4 apps and batch launchers. Single entry point. |
| `digimon_editor.spec` | PyInstaller spec for bundling the main editor. |
| `UTILITIES.md` | Full reference for all tools, launchers, executables, and dependency graph. |
| `WINDEX.md` | Global workflow guidelines for the project. |
| `AGENTS.md` | Project roles and coordination patterns using supported plan/task tools. |
| `decompile_lua.bat` | Launcher for Lua decompilation. |
| `Lua_Decompiler.bat` | Alternative Lua decompiler launcher. |
| `Launch_MVGL_GUI.bat` | Launcher for MVGL Tools GUI. |
| `DSCSToolsCLI.exe` | External CLI: MBE ↔ CSV conversion. |
| `CPKBrowser.exe` | External CLI: CPK archive browser. |
| `Base/` | Read-only original game data. |
| `DLC/` | Mod output (`addcont_17` structure). |
| `dsts-loader/` | Mod-loader format patches (`AP.CSV`). |
| `LUA/` | Decompiled Lua scripts. |
| `backup/` | Critical text file backups. |
| `_internal/` | Embedded Python runtime for packaged builds. |
