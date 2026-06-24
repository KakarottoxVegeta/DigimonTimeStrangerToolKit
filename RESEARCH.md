# RESEARCH.md — Digimon Time Stranger Knowledge Base

> **Centralized research backlog** for all DTS modding unknowns.
> Extracted from `SuperSimp666DigimonTimestranger/ROADMAP.md` + Remix Toolkit findings.
> Source of truth for open questions, reverse-engineering tasks, and feasibility studies.

## Legend

| Symbol | Meaning |
|--------|---------|
| `⚠️` | Open — needs research |
| `🔬` | In progress |
| `✅` | Resolved / documented |
| `❌` | Blocked / infeasible |
| `📦` | Resolved by Remix Toolkit |

---

## Digimon Data

### Stage / Rank Values
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:** `digimon_status.mbe` col 4 = stageId. Known values: 3=Rookie, 4=Champion, 5=Ultimate, 6=Mega. Full range 0–14 exists.
- **Source:** `Time Stranger Data File Headers.txt` — `"stageId": 4`

### Digimon Status Full Schema
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:** 136 columns documented in `Time Stranger Data File Headers.txt`
  - Col 0: id, Col 2: strKey, Col 4: stageId, Col 6: typeId
  - Cols 7–17: 12 elemental resistances (Null, Fire, Water, Ice, Grass, Wind, Elec, Ground, Steel, Light, Dark)
  - Cols 19–59: 41 boolean trait flags
  - Col 61: basePersonality
  - Cols 64–70: baseHP, baseSP, baseATK, baseDEF, baseINT, baseSPI, baseSPD
  - Col 71: growthPatternId (1–18)
  - Cols 72–107: 12 signature skills (ID + slot pairs)
  - Cols 108–119: 4 generic skills (ID + level pairs)
  - Col 131: fieldGuideId, Col 132: scriptId

### Type / Attribute Column
- **Status:** 📦 Resolved
- **Finding:** Col 6 = typeId. Text names in `digimon_type.mbe`. Element names in `element.mbe`.

### Growth Curve Structure
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:** 18 growth pattern files in `digimon_growth.mbe`. Per-level HP/SP/ATK/DEF/INT/SPI/SPD values. Pattern ID referenced by `digimon_status.mbe` col 71.

### Evolution System
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:**
  - `evolution.mbe/01_evolution_to.csv`: idx, idFrom (col 1), idTo (col 3)
  - `evolution.mbe/00_evolution_condition.csv`: dbId, tamerLevel (col 2), HP/SP/ATK/DEF/INT/SPI/SPD thresholds (cols 4–10), skillCountValor/Philanthropy/Amicable/Wisdom (cols 13–16), needsItem (col 22), jogress partner IDs (cols 24, 27)

### Evolution Line Grouping
- **Status:** ⚠️ Needs research
- **Notes:** Parse `00_evolution_condition.csv` + `01_evolution_to.csv` to group by line. Need to build adjacency graph.

### Evolution Line Depth
- **Status:** ⚠️ Needs research
- **Notes:** Max stages per line (Rookie→Champion→Ultimate→Mega = 4; some have 5+ with Burst/Ultra). Need to enumerate all lines.

### Special Evolution Types
- **Status:** ⚠️ Needs research
- **Notes:** Identify Armor, X-Antibody, Jogress, Burst Mode Digimon in `digimon_status.mbe` — need trait/flag columns (cols 19–59).

### New Digimon ID Allocation
- **Status:** ⚠️ Needs research
- **Notes:** Max Digimon ID in `digimon_status.mbe`; gaps for new entries; ID conflicts with enemy/battle tables.

### Custom Digimon Detection
- **Status:** ⚠️ Needs research
- **Notes:** How to distinguish mod-added Digimon from vanilla — ID range? mod_manifest? extra CSV column?

### Custom Digimon Rank Inference
- **Status:** ⚠️ Needs research
- **Notes:** If modder doesn't set col 4 (stage/rank), auto-detect from stat totals — need vanilla rank stat ranges per stage.

### Custom Digimon Evolution Line Parsing
- **Status:** ⚠️ Needs research
- **Notes:** How modders add evolution lines — same `evolution.mbe` format? separate file? Need to merge and re-index.

### Mod Manifest Format
- **Status:** ⚠️ Needs research
- **Notes:** Standardize or detect mod metadata format (JSON? CSV header? folder convention?) for Digimon attribution.

---

## Battle System

### Battle Skill Schema
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:** `battle_skill.mbe/00_battle_skill_list.csv` — 68 columns:
  - Col 0: skillId, Col 4: nameId, Col 5: skillFixedDescId
  - Col 16: effectId, Col 22: dmgType (0:none/self, 1:physical, 2:magic, 4:fixed, 5:fixed%, 6:buff, 11:major)
  - Col 23: power, Col 28: element, Col 33: targetType
  - Cols 34–35: minHits/maxHits, Col 36: SPCost
  - Col 39: alwaysHits, Col 40: accuracy, Col 42: critRate
  - Cols 43–45: HPDrain/SPDrain/recoil
  - Col 46: skillConditionalType (13 = if target KO'd)
  - Cols 52–60: 5 buffSet references into `02_buff_set.csv`
  - Cols 26–27: additionalProperty_1 (13 types: HP/SP scaling, KO count, usage count, round count, buff count)
  - Col 27: additionalProperty (stat inversion, nullify compatibility, etc.)

### Buff System
- **Status:** 📦 Resolved by Remix Toolkit
- **Finding:** `battle_skill.mbe/02_buff_set.csv` — 134 buff types: Poison, Confusion, Paralysis, Sleep, Panic, Bug, Pixelation, stat ±% modifiers, elemental resist ±%, counters, barriers.

### Enemy ID → Digimon Mapping
- **Status:** 📦 Partially resolved
- **Finding:** `battle_enemy.mbe/000_enemy_parameter.csv` col 2 = base Digimon ID. Enemy stat overrides at cols for level, HP, SP, ATK, DEF, INT, SPI, SPD.

### Battle Speed Multiplier
- **Status:** ⚠️ Needs research
- **Notes:** `battle_field_level.mbe` Col 7. Need to verify.

### EXP Reward Formula
- **Status:** ⚠️ Needs research
- **Notes:** `battle_calculate.mbe/000_battle_formula.csv`. Likely engine-level; may need memory scan.

### EXP Formula Location
- **Status:** ⚠️ Needs research
- **Notes:** `battle_calculate.mbe` has damage formulas but not EXP award — may need memory scan.

### Stat Cap Locations
- **Status:** ⚠️ Needs research
- **Notes:** `battle_calculate.mbe/01_battle_define.csv` IDs 43,44,52,54 (9999, 99999, 999999, 99999); `digimon_editor.py` UI caps (HP/SP 99999, others 9999); engine runtime caps unknown.

### Stat Uncap Feasibility
- **Status:** ⚠️ Needs research
- **Notes:** May need memory patching / code injection if engine enforces hard caps; test by setting CSV caps to 9999999.

### Boss/Story Encounter Detection
- **Status:** ⚠️ Needs research
- **Notes:** `encount_group.csv` col 75 = battle script name; cross-ref with Lua scripts for story-critical flags.

### Randomizer Stat Scaling
- **Status:** ⚠️ Needs research
- **Notes:** When swapping ranks, scale HP/ATK/DEF/INT/SPI/SPD to target rank's average to maintain balance.

### Surge Stat Inheritance
- **Status:** ⚠️ Needs research
- **Notes:** When Agumon surges to Greymon, does it keep Agumon's personality/traits? Or use Greymon's base?

### Surge EXP/Reward Scaling
- **Status:** ⚠️ Needs research
- **Notes:** Outlier Digimon should give appropriate EXP/bits/items for their actual rank, not base rank.

### Per-Area Surge Config
- **Status:** ⚠️ Needs research
- **Notes:** Map surge rates to `field_map.mbe` areas (early game 1%, late game 15%, post-game 30%).

---

## Difficulty System

### Difficulty ID Limits
- **Status:** ⚠️ Needs research
- **Notes:** Engine may hardcode max difficulty ID (5); new IDs (6+) may need Lua patches for `is_high_difficulty` checks.

### Difficulty UI Text Keys
- **Status:** ⚠️ Needs research
- **Notes:** `ui_difficulty_name_01` format — need to add new string entries for custom difficulties.

---

## Map System

### Field Mob Digimon IDs
- **Status:** 📦 Partially resolved
- **Finding:** `field_mob_*.mbe/01_field_mob.csv` col 3 = Digimon ID (e.g., `chr708`). Need to resolve to stage.

### Map Collision / Navmesh Format
- **Status:** ⚠️ Needs research
- **Notes:** `field_map.mbe/08_field_map_collision_element.csv`, `09_field_map_special_collision.csv`.

### Rail Move Path Data
- **Status:** ⚠️ Needs research
- **Notes:** Referenced by string name in mob/NPC CSVs — need to find rail move definitions.

### Rail-Move Path Compatibility
- **Status:** ⚠️ Needs research
- **Notes:** Can new mobs inherit existing rail-move paths? Need matching path name format in `field_mob` CSV.

### Minimap Icon Format
- **Status:** ⚠️ Needs research
- **Notes:** `field_map.mbe/03_field_minimap.csv`.

### Map Difficulty Inference
- **Status:** ⚠️ Needs research
- **Notes:** Scan existing `field_mob` Digimon ranks per map to infer area difficulty tier (early/mid/late/post-game).

### Biome/Theme Detection Per Map
- **Status:** ⚠️ Needs research
- **Notes:** How to determine map theme (forest/volcano/coastal) — map name? `field_map.mbe` environment column? Lua var?

### Navmesh-Aware Spawn Placement
- **Status:** ⚠️ Needs research
- **Notes:** How to place new mobs at valid positions — copy coords from existing mobs? Read navmesh? Random ground trace?

### Spawn Density Limits Per Map
- **Status:** ⚠️ Needs research
- **Notes:** Max mobs per map before performance degrades — engine limit? Test by incrementally adding mobs.

---

## Model System

### Digimon Model Format
- **Status:** ⚠️ Needs research
- **Notes:** Identify game model format (FBX? custom?); locate model files in game data; determine bone rig standard.

### Model Reference Columns
- **Status:** 📦 Partially resolved
- **Finding:** `model_setting.mbe` — NPC collision, distances, battle/field/menu scale, rideable flag. `lod_chara.mbe` — LOD distances. `model_locator.mbe` — locator + motion. `char_info.mbe` — char_key, chr_id, model_ref, motion_ref.

### Texture Format
- **Status:** ⚠️ Needs research
- **Notes:** Game texture format (DDS/BC7?); max resolution; mipmap requirements.

### Animation System
- **Status:** ⚠️ Needs research
- **Notes:** How animations are stored/referenced; shared rig across Digimon?; animation set IDs mapping.

### Animation Speed Control
- **Status:** ⚠️ Needs research
- **Notes:** May be engine-level.

### Triangle/Bone Budgets
- **Status:** ⚠️ Needs research
- **Notes:** Max tris per Digimon model; max bones per mesh; performance limits.

### LOD System
- **Status:** 📦 Partially resolved
- **Finding:** `lod_chara.mbe` exists with LOD distances and model references. Need to document levels and thresholds.

---

## Time / Weather System

### Time-of-Day MBE Location
- **Status:** ⚠️ Needs research
- **Notes:** Find time system MBE (`field_time.mbe`? `world_time.mbe`? Lua-only?); identify per-map time enable flags.

### Weather MBE Location
- **Status:** ⚠️ Needs research
- **Notes:** Find weather system MBE (`field_weather.mbe`? `world_weather.mbe`?); identify weather type IDs and params.

### Time Period Definitions
- **Status:** ⚠️ Needs research
- **Notes:** How many time periods (dawn/day/dusk/night/midnight?); lighting params per period; skybox swap mechanism.

### Lua Time/Weather Functions
- **Status:** ⚠️ Needs research
- **Notes:** `get_time()`, `is_night()`, `get_weather()`, `set_weather()` — find all Lua time/weather API calls.

### Map-Specific Time Support
- **Status:** ⚠️ Needs research
- **Notes:** Which maps support day/night cycles vs. static lighting; `field_map.mbe` time/weather flag columns.

### Time-Locked Spawn Conditions
- **Status:** ⚠️ Needs research
- **Notes:** `field_mob.mbe` time condition columns (night-only spawns?); event/NPC schedule system.

### Weather Particle/Sound Assets
- **Status:** ⚠️ Needs research
- **Notes:** Rain/snow/fog particle systems; weather sound effect file references; wind params.

### Time-Based Evolution Hooks
- **Status:** ⚠️ Needs research
- **Notes:** `evolution.mbe` time condition column?; add new evolution type "evolve at night only".

### Ambient Sound Crossfade
- **Status:** ⚠️ Needs research
- **Notes:** Day/night ambient sound file references per map; crossfade duration and curve.

### Clock UI Integration
- **Status:** ⚠️ Needs research
- **Notes:** Does game have a clock HUD element?; can we add/toggle one via UI MBE or Lua.

### Weather ↔ Battle Interactions
- **Status:** ⚠️ Needs research
- **Notes:** Do battles check weather? (e.g., rain boosts Water-type); storm = random interrupt?

---

## Day/Night Module (daynight)

### MBE Integration
- **Status:** ⚠️ Needs research
- **Notes:** How to inject time/weather data into game — patch existing MBEs or add new ones? Lua hooks?

### Clock Persistence
- **Status:** ⚠️ Needs research
- **Notes:** How game save data is structured; where to inject day counter + mob age state without breaking saves.

### Map Mob Entity Storage
- **Status:** ⚠️ Needs research
- **Notes:** `field_mob_*.mbe` runtime — can per-mob data (age, current Digimon ID) persist or use Lua table?

### Model Swap on Evolution
- **Status:** ⚠️ Needs research
- **Notes:** When a map Digimon evolves, how to swap its 3D model in-place? Same rig? LOD?

### Battle Scaling on Evolved Mobs
- **Status:** ⚠️ Needs research
- **Notes:** Does `enemy_parameter.csv` resolve at encounter load or spawn? Evolved stats need live resolution.

### Map Mob Evolution Save Format
- **Status:** ⚠️ Needs research
- **Notes:** Custom save section vs. piggyback on existing save — how to store Digimon age + current form per mob.

### Boss/Story Mob Evolution Lock
- **Status:** ⚠️ Needs research
- **Notes:** How to flag mobs as "story-locked" so they never evolve; `field_mob` flag column or separate exclusion list.

---

## Custom Digimon Area Placer

### Custom Digimon Type/Attribute Column
- **Status:** 📦 Resolved
- **Finding:** Col 6 = typeId in `digimon_status.mbe`. Text names in `digimon_type.mbe`.

---

*Last Updated: 2026-06-08*
*Source: Extracted from `SuperSimp666DigimonTimestranger/ROADMAP.md` Research Backlog + Remix Toolkit (zeak6464) findings*
