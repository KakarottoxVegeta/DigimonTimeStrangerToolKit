# WINDEX.md - Project Workflow Guidelines

## Project Overview
**Digimon Time Stranger ToolKit** - A comprehensive modding toolkit for Digimon Story Time Stranger, featuring:
- PyQt6-based Digimon Editor with full data management
- MBE file parsing and CSV export/import
- dsts-loader integration for mod distribution
- Lua script decompilation tools
- Reloaded-II mod loader support

---

## Core Workflow Guidelines

### [WF-001] Modular Architecture
- **Separation of Concerns**: Data loading (`data_loader.py`), UI (`digimon_editor.py`), export (`csv_exporter.py`) are separate modules
- **Single Responsibility**: Each class handles one domain (DigimonData, MBELoader, CSVExporter, SkillEditor)
- **Plugin-Ready**: New editors (MBE_Editor, lua_decompiler_gui) follow same pattern

### [WF-002] Data Flow Standards
```
Base/ (read-only game data)
    ↓ MBELoader
DigimonData objects (in-memory)
    ↓ Editor UI
Modified DigimonData
    ↓ CSVExporter / DLCExporter
DLC/ or dsts-loader/ (mod output)
```

### [WF-003] File Format Handling
- **MBE Files**: Binary game format → CSV via DSCSToolsCLI.exe
- **CSV Files**: Human-editable intermediate format
- **AP.CSV**: dsts-loader patch format (append-only, preserves base game)
- **Lua Scripts**: Decompiled with unluac_2023_12_24.jar

### [WF-004] ID Management
- **Digimon ID**: Numeric (0-99999), unique across base + DLC
- **Chr ID**: String format `chr{id}` (e.g., `chr805`, `chr1000`)
- **Char Key**: String format `char_{NAME}` (e.g., `char_AGUMON`)
- **Animation Reference**: Separate from Chr ID - points to animation source

### [WF-005] Evolution System Rules
- **Max 6 evolutions per source Digimon** (hard game limit)
- **Evolution ID Formula**: `(source_id * 100) + counter`
- **Pre-evolutions**: Create reverse entries in evolution_to.csv
- **Conditions**: Stored in evolution_condition.csv per target Digimon

### [WF-006] Resistance Values (0-4)
| Value | Meaning | Damage Multiplier |
|-------|---------|-------------------|
| 0 | Normal | 1.0x |
| 1 | Weak | 1.5x |
| 2 | Very Weak | 2.0x |
| 3 | Resist | 0.5x |
| 4 | Immune | 0.0x |

### [WF-007] Trait System (41 boolean flags)
Traits 0-15: Elemental specialists (Fire, Water, Plant, etc.)
Traits 16-40: Gameplay modifiers (Searcher, Fighter, Brainy, etc.)

### [WF-008] Skill System
- **Signature Skills**: Up to 12, each with slot (1-12)
- **Generic Skills**: Up to 4, each with level (1-100)
- **Advanced Skills**: Full battle_skill.mbe parameter editing

### [WF-009] Model & Animation
- **Model ID**: References model files
- **Motion ID**: Audio/animation reference
- **Animation Reference**: Which Digimon's animations to use (separate from own Chr ID)
- **LOD Distances**: 3 levels (default: 20, 65, 500)

### [WF-010] Export Modes
1. **Base Game Edit**: Direct MBE modification (requires repack)
2. **DLC Export**: Addcont_17 structure (in-game without base modification)
3. **dsts-loader**: AP.CSV patch format (mod loader compatible)
4. **Merge Mode**: Update single Digimon in existing dsts-loader

---

## Quality Gates

### [QG-001] Pre-Save Validation
- [ ] ID uniqueness check (base + DLC)
- [ ] Chr ID uniqueness check
- [ ] Char Key format validation
- [ ] Evolution slot limits (≤6 per source)
- [ ] Required fields populated

### [QG-002] Export Validation
- [ ] All 9 required files generated for dsts-loader
- [ ] CSV headers match expected format
- [ ] No duplicate rows in evolution files
- [ ] Text files use proper CSV quoting

### [QG-003] Import Validation
- [ ] AP.CSV files parse without errors
- [ ] Referenced Chr IDs exist or are creatable
- [ ] Evolution references valid
- [ ] Profile text properly escaped

---

## Tooling Standards

### [TS-001] Python Environment
- Python 3.8+ (embedded in `_internal/`)
- PyQt6 for GUI
- Standard library only (csv, pathlib, json, etc.)

### [TS-002] External Tools
- **DSCSToolsCLI.exe**: MBE ↔ CSV conversion
- **unluac_2023_12_24.jar**: Lua decompilation
- **Reloaded-II**: Mod loader runtime

### [TS-003] File Organization
```
Project Root/
├── Base/                    # Original game data (read-only)
├── DLC/                     # Mod output (addcont_17 structure)
├── dsts-loader/             # Mod loader format
├── LUA/                     # Decompiled Lua scripts
├── backup/                  # Critical text files backup
├── _internal/               # Embedded Python runtime
├── digimon_editor.py        # Main editor
├── data_loader.py           # MBE/CSV parsing
├── csv_exporter.py          # Export logic
└── *.bat / *.exe            # Launchers and tools
```

---

## Development Workflow

### [DW-001] Adding New Digimon
1. Launch `digimon_editor.py` → "Create New"
2. Select template Digimon
3. Customize all tabs (Basic, Stats, Skills, Traits, Model, Evolution, Battle)
4. Export to DLC or dsts-loader
5. Test in-game via Reloaded-II

### [DW-002] Editing Existing Digimon
1. Load from Base Game or DLC source
2. Modify desired fields
3. Save (updates source files)
4. Repack MBE if editing base game
5. Export to DLC for distribution

### Unification
- **Unified Entry Point**: `dts_launcher.py` launches all other tools and batch files. This is the primary entry point for the toolkit.
- Run `python dts_launcher.py` first, then use it to launch `digimon_editor.py`, `MBE_Editor.py`, `lua_decompiler_gui.py`, `mvgl_tools_gui.py`, or batch launchers from one dashboard.
1. Decompile with `Lua_Decompiler.bat` or `lua_decompiler_gui.py`
2. Edit scripts in `LUA/patchlua/` or `LUA/alua/`
3. Test via Reloaded-II mod loader

### [DW-004] Creating Mod Packs
1. Export multiple Digimon to dsts-loader
2. Include Lua patches in `LUA/patchlua/`
3. Package as Reloaded-II mod
4. Distribute via GameBanana/GitHub

---

## Error Handling Standards

### [EH-001] User-Facing Errors
- Show QMessageBox with clear action guidance
- Log full traceback to console
- Never crash silently

### [EH-002] Data Corruption Prevention
- Backup original files before write
- Validate CSV structure before parse
- Use temp files for atomic writes

### [EH-003] Missing Data Graceful Degradation
- Default values for optional fields
- Placeholder names for missing lookups
- Continue loading partial data

---

## Performance Guidelines

### [PG-001] Large List Handling
- Virtual scrolling for 1000+ Digimon
- Async loading with progress updates
- Caching of name/ID lookups

### [PG-002] File Operations
- Batch CSV reads/writes
- Minimize DSCSToolsCLI calls
- Stream large file processing

---

## Version Control

### [VC-001] Tracked Files
- Source code (`*.py`)
- Configuration (`*.json`, `*.bat`)
- Documentation (`*.md`)
- Lua patches (`LUA/patchlua/*.lua`)

### [VC-002] Ignored Files
- `_internal/` (embedded runtime)
- `Reloaded-II/` (mod loader binaries)
- `Base/` (original game data)
- `DLC/` (generated output)
- `dsts-loader/` (generated output)
- `*.exe` (compiled tools)
- `__pycache__/`

---

## Release Checklist

### [RC-001] Pre-Release
- [ ] All QG gates pass
- [ ] Test with clean game install
- [ ] Verify DLC loads in Reloaded-II
- [ ] Test dsts-loader import/export roundtrip
- [ ] Update version in `digimon_editor.spec`

### [RC-002] Packaging
- [ ] PyInstaller build (`digimon_editor.spec`)
- [ ] Include `_internal/` runtime
- [ ] Bundle DSCSToolsCLI.exe
- [ ] Bundle unluac jar
- [ ] Create release archive

---

*Last Updated: 2026-06-08*
*Project: Digimon Time Stranger ToolKit*