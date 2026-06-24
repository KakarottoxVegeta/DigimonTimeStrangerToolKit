# ROADMAP.md - Digimon Time Stranger ToolKit

## Overview

This document tracks planned features, utilities, and improvements for the Digimon Time Stranger ToolKit. Items are organized by priority and category.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[-]` | In Progress |
| `[x]` | Completed |
| `⚠️` | Blocked / Needs Research |
| `🆕` | Newly Added |

---

## Phase 1: Core Tooling (Completed)

- [x] `digimon_editor.py` — Main PyQt6 Digimon editor GUI
- [x] `MBE_Editor.py` — Direct binary MBE/CSV editor
- [x] `lua_decompiler_gui.py` — Lua batch decompiler frontend
- [x] `mvgl_tools_gui.py` — MVGL/CPK/MBE/AFS2 tool frontend
- [x] `data_loader.py` — MBELoader library
- [x] `csv_exporter.py` — CSVExporter + repack helpers
- [x] `DSCSToolsCLI.exe` — MBE ↔ CSV converter
- [x] `CPKBrowser.exe` — CPK archive browser
- [x] `WINDEX.md` — Global workflow guidelines
- [x] `Agents.md` — Agent role definitions
- [x] `UTILITIES.md` — Tool reference documentation
- [x] `INDEX.md` — Repository index

---

## Phase 2: Data Mapping & Discovery Utilities

### 🆕 Table Mapper Utility
**File:** `table_mapper.py` (new)
**Purpose:** Map MBE tables by function — given a game mechanic (e.g., "battle speed", "evolution", "skill damage"), find all related MBE files, CSV sheets, column indices, and Lua hooks.

**Features:**
- [ ] Parse `Time Stranger Data File Headers.txt` into structured lookup
- [ ] Index all `Base/data/*.mbe/` directories and their CSV sheets
- [ ] Map game functions → MBE files → columns → Lua constants
- [ ] CLI interface: `python table_mapper.py --function "battle speed"`
- [ ] Output: table of related files, columns, and cross-references
- [ ] Support fuzzy search (e.g., "fast forward" → battle speed tiers)
- [ ] Export results as JSON for other tools to consume

**Data Sources:**
- `Time Stranger Data File Headers.txt` — known column mappings
- `Base/data/` — 100+ MBE directories
- `Digimon Time Stealer Lua Scripts - Complete Reference Guide.html` — Lua function constants
- `LUA/patchlua/` — battle scripts referencing table IDs

**Example Usage:**
```bash
# Find all tables related to battle speed
python table_mapper.py --function "battle speed"

# Find evolution-related tables
python table_mapper.py --function "evolution"

# Find skill damage formula tables
python table_mapper.py --function "skill damage"

# Output as JSON
python table_mapper.py --function "battle speed" --format json
```

**Expected Output:**
```
Function: battle speed
─────────────────────────────────────────
MBE Files:
  battle_field_level.mbe/000_battle_field_level.csv
    Col 6: battle tier (2-6)
    Col 7: speed tier (7, 15, 25, 30, 35, 40, 50)
    Col 8: battle config ID (204, 206, 207, 801)

  battle_calculate.mbe/002_battle_define_float.csv
    Idx 16: 3.0 (global speed multiplier?)
    Idx 17: 0.1 (turn/animation factor?)

Lua Hooks:
  Battle_Round_Start(info) — LUA/patchlua/battle_*.lua
  Battle_Turn_Start(info)  — LUA/patchlua/battle_*.lua

Constants (from reference guide):
  STATUS_TYPE_SPEED = 9
  PLAYER_DIGIMON = 0
  ENEMY_DIGIMON = 1
```

---

### 🆕 MBE Schema Extractor
**File:** `mbe_schema_extractor.py` (new)
**Purpose:** Auto-extract column types and headers from all MBE CSV files to build a searchable schema database.

**Features:**
- [ ] Scan all `Base/data/*.mbe/` directories
- [ ] Parse CSV header rows (type + name format: `int32 0,empty 1,string2 3`)
- [ ] Build searchable index: column name → file → type
- [ ] Detect relationships between tables (shared IDs, foreign keys)
- [ ] Export schema as JSON

---

### 🆕 Lua Constant Extractor
**File:** `lua_constant_extractor.py` (new)
**Purpose:** Parse the HTML reference guide and Lua scripts to extract all game constants, enums, and function signatures.

**Features:**
- [ ] Parse `Digimon Time Stealer Lua Scripts - Complete Reference Guide.html`
- [ ] Extract all constant tables (STATUS_TYPE_*, MOTION_TYPE_*, etc.)
- [ ] Extract all function signatures with parameters
- [ ] Cross-reference constants with MBE column values
- [ ] Export as JSON for table_mapper.py integration

---

### 🆕 Stat-Based EXP Rebalance Tool
**File:** `exp_rebalance.py` (new)
**Purpose:** Replace the flat enemy EXP rewards with a formula based on enemy stats (HP, SP, ATK, DEF, INT, SPI, SPD, Level), plus configurable multipliers for story/boss encounters.

**Features:**
- [ ] Load `battle_enemy.mbe/00_enemy_parameter.csv` (enemy stats + current EXP in col 33)
- [ ] Load `digimon_status.mbe/01_experience_table.csv` (level-up thresholds for scaling reference)
- [ ] Load `digimon_growth.mbe/*` (growth curves for stat-to-level mapping)
- [ ] Configurable formula: `EXP = base_k * (HP^a * ATK^b * DEF^c * INT^d * SPI^e * SPD^f) * Level^g`
- [ ] **Story/Boss Multiplier System:**
  - [ ] Tag enemies via `encount_group.csv` (col 75 = battle script name) or `battle_type` (col 11)
  - [ ] Configurable multiplier per tag: `story=1.5`, `boss=2.0`, `superboss=3.0`, `normal=1.0`
  - [ ] Optional: multiplier by enemy ID range or specific ID list
- [ ] Preview mode: show before/after EXP for all enemies, sorted by change magnitude
- [ ] Output patched `00_enemy_parameter.csv` with recalculated col 33 (base EXP)
- [ ] Optional: also rebalance bit rewards (col 35), item drops (col 38), drop rates (col 40)
- [ ] Integration with `csv_exporter.py` / `MBE_Editor.py` for one-click MBE repack
- [ ] CLI: `python exp_rebalance.py --formula "..." --multipliers story=1.5,boss=2.0 --preview`
- [ ] Export rebalance report as JSON/CSV for documentation

**Data Sources:**
- `backup/data/battle_enemy.mbe/00_enemy_parameter.csv` — enemy stats (cols 17-23), base EXP (col 33), bits (col 35), item (col 38), drop rate (col 40), battle type (col 11)
- `backup/data/battle_enemy.mbe/01_encount_group.csv` — encounter groups, battle script names (col 75)
- `backup/data/battle_calculate.mbe/06_battle_cp_increase.csv` — battle type CP bonuses
- `backup/data/digimon_status.mbe/01_experience_table.csv` — level-up EXP thresholds (4 patterns)
- `backup/data/digimon_growth.mbe/*` — stat growth per level (18 patterns)

**Example Usage:**
```bash
# Preview with default formula
python exp_rebalance.py --preview

# Custom formula + story/boss multipliers
python exp_rebalance.py --formula "k=0.01,a=0.5,b=0.3,c=0.2,d=0.2,e=0.2,f=0.1,g=1.2" --multipliers "story=1.5,boss=2.0,superboss=3.0" --preview

# Apply and repack MBE
python exp_rebalance.py --formula "..." --multipliers "..." --apply --repack
```

---

## Phase 3: Editor Enhancements

### digimon_editor.py
- [ ] Add "Table Map" panel — show related MBE files for current Digimon
- [ ] Add "Lua Preview" — show which Lua scripts reference current Digimon ID
- [ ] Add "Cross-Reference" view — trace ID through all tables
- [ ] Improve evolution slot limit handling
- [ ] Add batch edit mode for multiple Digimon

### MBE_Editor.py
- [ ] Add column type validation on save
- [ ] Add "Go to Reference" — jump to linked table by ID
- [ ] Add schema-aware column headers (from mbe_schema_extractor)
- [ ] Add diff view between Base and DLC versions

---

## Phase 4: Workflow & Automation

- [ ] `apply_mod.bat` — one-click apply DLC to game directory
- [ ] `validate_mod.bat` — check mod integrity before packaging
- [ ] `diff_tables.bat` — compare Base vs DLC MBE files
- [ ] Auto-backup before any write operation
- [ ] Git hooks for pre-commit validation

---

## Phase 5: Documentation

- [ ] `DATA_MAP.md` — full cross-reference of all MBE tables
- [ ] `LUA_API.md` — extracted Lua API reference
- [ ] `MODDING_TUTORIAL.md` — step-by-step modding guide
- [ ] `FAQ.md` — common issues and solutions

---

## Phase 6: Advanced Features

- [ ] DLC builder — create new Digimon from scratch
- [ ] Evolution chain visualizer — graph view of evolution trees
- [ ] Skill simulator — preview damage calculations
- [ ] Battle simulator — test party compositions
- [ ] Model preview — view Digimon models in-editor

---

## Research Backlog

| Topic | Status | Notes |
|-------|--------|-------|
| Battle speed multiplier location | ⚠️ | Likely `battle_field_level.mbe` Col 7 or `battle_calculate.mbe` Idx 16 |
| Animation speed control | ⚠️ | May be engine-level, not in CSV |
| Field battle spawn rates | ⚠️ | `field_battle_*.mbe` files need analysis |
| DLC quest integration | ⚠️ | `dlc_info.mbe` structure unknown |
| Lua `BattleCommon_SetAnimationSpeed` | ⚠️ | Not in reference guide — may not exist |
| Cross-table ID relationships | ⚠️ | Needs schema extractor to map |

---

## File Inventory

### Existing Tools
| File | Purpose |
|------|---------|
| `digimon_editor.py` | Main editor GUI |
| `MBE_Editor.py` | MBE/CSV editor |
| `lua_decompiler_gui.py` | Lua decompiler |
| `mvgl_tools_gui.py` | Archive tools |
| `data_loader.py` | Data loading library |
| `csv_exporter.py` | Export/repack library |

### New Utilities (Planned)
| File | Purpose |
|------|---------|
| `table_mapper.py` | Map tables by game function |
| `mbe_schema_extractor.py` | Auto-extract MBE schemas |
| `lua_constant_extractor.py` | Extract Lua constants |

### Reference Documents
| File | Purpose |
|------|---------|
| `Time Stranger Data File Headers.txt` | Known column mappings |
| `Digimon Time Stealer Lua Scripts - Complete Reference Guide.html` | Lua API reference |
| `WINDEX.md` | Workflow guidelines |
| `Agents.md` | Agent definitions |
| `UTILITIES.md` | Tool reference |
| `INDEX.md` | Repository index |
| `ROADMAP.md` | This file |

---

*Last Updated: 2026-06-08*
*Project: Digimon Time Stranger ToolKit*
