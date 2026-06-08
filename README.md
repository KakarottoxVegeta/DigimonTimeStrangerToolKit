# Digimon Time Stranger ToolKit

A comprehensive modding toolkit for **Digimon Story Time Stranger**, featuring a PyQt6-based Digimon Editor, MBE file tools, Lua decompilation, and Reloaded-II mod loader integration.

## 🎯 Project Overview

This toolkit enables creation and modification of Digimon data for Digimon Story Time Stranger, supporting:
- **Full Digimon Editor** with 10-tab interface (Basic, Stats, Skills, Traits, Model, Evolution, Battle, etc.)
- **MBE File Parsing** - Binary game format ↔ CSV conversion
- **dsts-loader Integration** - Mod loader compatible patch format
- **Lua Script Tools** - Decompilation and patching
- **DLC Export** - Addcont_17 structure for in-game mods
- **Reloaded-II Support** - Modern mod loader framework

## 📁 Project Structure

```
DigimonTimeStrangerToolKit/
├── WINDEX.md              # Workflow guidelines
├── Agents.md              # Agent role definitions
├── README.md              # This file
├── .gitignore             # Version control exclusions
│
├── digimon_editor.py      # Main PyQt6 editor (9160 lines)
├── data_loader.py         # MBE/CSV parsing (3795 lines)
├── csv_exporter.py        # Export logic (1094 lines)
├── lua_decompiler_gui.py  # Lua decompiler GUI (495 lines)
├── MBE_Editor.py          # Binary MBE editor (1351 lines)
├── mvgl_tools_gui.py      # MVGL tools GUI (455 lines)
├── digimon_editor.spec    # PyInstaller build config
│
├── DSCSToolsCLI.exe       # MBE ↔ CSV converter
├── unluac_2023_12_24.jar  # Lua decompiler
│
├── _internal/             # Embedded Python 3.8 runtime
├── Base/                  # Original game data (read-only)
├── DLC/                   # Mod output (addcont_17 structure)
├── dsts-loader/           # Mod loader patch format
├── LUA/                   # Decompiled Lua scripts
│   ├── alua/              # Original Lua scripts
│   └── patchlua/          # Patched Lua scripts
├── backup/                # Critical text file backups
└── Reloaded-II/           # Mod loader runtime
```

## 🚀 Quick Start

### Running the Editor
```bash
python digimon_editor.py
```

### Building Executable
```bash
pyinstaller digimon_editor.spec
```

### Decompiling Lua Scripts
```bash
python lua_decompiler_gui.py
# or
Lua_Decompiler.bat
```

## 📋 Workflow Guidelines

See [WINDEX.md](WINDEX.md) for complete workflow standards including:
- Data flow architecture
- File format handling
- ID management
- Evolution system rules
- Quality gates
- Development workflows

## 🤖 Agent Roles

See [Agents.md](Agents.md) for agent definitions:
- **COMMANDER** - Orchestration & project management
- **ARCHITECT** - System design & data models
- **CODE** - Implementation & bug fixes
- **RESEARCH** - Reverse engineering & analysis
- **DEBUG** - Troubleshooting & root cause analysis
- **TESTER** - QA & in-game validation
- **PACKAGER** - Build & release engineering
- **DOCS** - Documentation & guides

## 🔧 Key Features

### Digimon Editor Tabs
1. **Basic Info** - ID, names, classification, profile
2. **Stats** - Base stats, growth pattern, resistances
3. **Skills** - Signature (12) & Generic (4) skills
4. **Advanced Skills** - Full battle_skill.mbe parameters
5. **Traits** - 41 boolean trait flags
6. **Model & Animation** - Model settings, LOD, references
7. **Evolution** - Paths, pre-evolutions, requirements
8. **Battle** - Enemy parameters, formations, encounters
9. **Files** - 9-file completeness tracker

### Export Modes
| Mode | Use Case | Output |
|------|----------|--------|
| Base Game Edit | Direct modification | MBE files (repack needed) |
| DLC Export | In-game without base mod | addcont_17 structure |
| dsts-loader | Mod loader distribution | AP.CSV patch files |
| Merge | Update single Digimon | Preserves other entries |

## 📦 Required Files for Complete Digimon

A complete Digimon requires data in all 9 files:
1. `digimon_status.mbe/000_digimon_status_data.csv`
2. `char_info.mbe/000_char_info.csv`
3. `text/char_name.mbe/000_Sheet1.csv`
4. `model_setting.mbe/000_model_setting.csv`
5. `model_locator.mbe/000_model_locator.csv`
6. `model_locator.mbe/001_model_locator_motion.csv`
7. `lod_chara.mbe/000_lod.csv`
8. `lod_chara.mbe/001_lod_model.csv`
9. `field_anime.mbe/000_field_move_animation.csv`

## ⚙️ Configuration

### Resistance Values (0-4)
| Value | Meaning | Multiplier |
|-------|---------|------------|
| 0 | Normal | 1.0x |
| 1 | Weak | 1.5x |
| 2 | Very Weak | 2.0x |
| 3 | Resist | 0.5x |
| 4 | Immune | 0.0x |

### Evolution Limits
- **Max 6 evolutions per source Digimon** (hard game limit)
- Evolution ID formula: `(source_id * 100) + counter`
- Pre-evolutions create reverse entries

## 🛠️ Development

### Adding New Features
Follow spawn pattern [SP-001]:
```
COMMANDER → ARCHITECT (design) → RESEARCH (analyze) → CODE (implement) → TESTER (validate) → DOCS (document)
```

### Bug Fixes
Follow spawn pattern [SP-002]:
```
COMMANDER → DEBUG (analyze) → CODE (fix) → TESTER (regress) → DOCS (changelog)
```

### Release Process
Follow spawn pattern [SP-004]:
```
COMMANDER → CODE (polish) → TESTER (full suite) → PACKAGER (build) → DOCS (release notes)
```

## 📚 Documentation

- **WINDEX.md** - Complete workflow guidelines
- **Agents.md** - Agent role definitions
- **Digimon Time Stealer Lua Scripts - Complete Reference Guide.html** - Lua API reference

## 🔗 External Tools

- **DSCSToolsCLI.exe** - MBE binary ↔ CSV conversion
- **unluac_2023_12_24.jar** - Lua bytecode decompilation
- **Reloaded-II** - Modern mod loader framework

## 📄 License

This project is for educational and modding purposes. Respect the original game's IP.

---

*Last Updated: 2026-06-08*
*Project: Digimon Time Stranger ToolKit*