# Ride (RideGamejam) - Save Game Editor Documentation

## Overview
This document provides a complete guide to editing save files for the Ride game (RideGamejam). The save files use Unreal Engine's GVAS format.

---

## Save File Information

**File Format:** Unreal Engine GVAS (Version 3)
**Game:** Ride (RideGamejam)
**Save Files:**
- `TimNPeans.sav` - Main save file (24,822 bytes)
- `TimNPeans_meta.sav` - Metadata file (2,470 bytes)

---

## Discovered Editable Values

### Primary Values

| Property Name      | Offset   | Type  | Current Value | Description                    |
|--------------------|----------|-------|---------------|--------------------------------|
| CurrentCheckpoint  | 0x0735   | Int32 | 9             | Progress checkpoint (0-?)      |
| EpicPens           | 0x0C8E   | Int32 | 16            | Currency/collectible count     |
| VehicleParts       | 0x0CBC   | Int32 | 20            | Available vehicle parts        |

### Vehicle Damage Values

| Damage Type        | Offset   | Type  | Current Value | Description                    |
|--------------------|----------|-------|---------------|--------------------------------|
| Frame              | 0x085B   | Int32 | 0             | Frame damage (0-100?)          |
| Engine             | 0x0925   | Int32 | 0             | Engine damage (0-100?)         |
| Tire.RL            | 0x09F0   | Int32 | 0             | Rear Left tire damage          |
| Tire.FR            | 0x0ABB   | Int32 | 0             | Front Right tire damage        |
| Tire.RR            | 0x0B86   | Int32 | 0             | Rear Right tire damage         |
| Tire.FL            | 0x0C51   | Int32 | 0             | Front Left tire damage         |

---

## Editing Methods

### Method 1: Using Python Script

The easiest way to edit the save file is using the provided Python scripts:

```bash
# Run the interactive editor
python3 interactive_editor.py

# Or directly specify a modification type (1-5)
python3 interactive_editor.py 5  # God Mode
```

**Available Modifications:**
1. Max Currency (9999 EpicPens)
2. Max Vehicle Parts (9999)
3. Repair Vehicle (all damage = 0)
4. Reset Progress (checkpoint 0)
5. God Mode (max everything + full repair)

### Method 2: Using a Hex Editor

You can manually edit the save file using any hex editor (HxD, 010 Editor, etc.):

#### Example: Increase EpicPens to 9999
1. Open `TimNPeans.sav` in your hex editor
2. Go to offset `0x0C8E` (3214 in decimal)
3. You'll see 4 bytes representing the current value (little-endian)
4. Replace with: `0F 27 00 00` (9999 in little-endian hex)
5. Save the file

#### Example: Fully Repair Vehicle
Set all vehicle damage values to 0:
- Go to offset `0x085B` → Set to `00 00 00 00`
- Go to offset `0x0925` → Set to `00 00 00 00`
- Go to offset `0x09F0` → Set to `00 00 00 00`
- Go to offset `0x0ABB` → Set to `00 00 00 00`
- Go to offset `0x0B86` → Set to `00 00 00 00`
- Go to offset `0x0C51` → Set to `00 00 00 00`

---

## Understanding Values

### Int32 (32-bit Integer) Format
All editable values are stored as 32-bit integers in **little-endian** format:
- 1 byte = 2 hex digits
- 4 bytes = 8 hex digits total
- Example: `0F 27 00 00` = 9999 in decimal

### Decimal to Hex Conversion
| Decimal | Hex (Little-Endian) |
|---------|---------------------|
| 0       | 00 00 00 00        |
| 10      | 0A 00 00 00        |
| 100     | 64 00 00 00        |
| 1000    | E8 03 00 00        |
| 9999    | 0F 27 00 00        |
| 65535   | FF FF 00 00        |

---

## Common Modifications

### God Mode Setup
```
EpicPens: 9999
VehicleParts: 9999
All Vehicle Damage: 0
```

### Fresh Start (Keep Progress)
```
CurrentCheckpoint: 0
EpicPens: 0
VehicleParts: 0
All Vehicle Damage: 0
```

### Unlimited Resources
```
EpicPens: 99999
VehicleParts: 99999
Keep everything else as-is
```

---

## Backup Instructions

**ALWAYS** backup your save file before editing:

```bash
# On Windows
copy TimNPeans.sav TimNPeans.sav.backup

# On Linux/Mac
cp TimNPeans.sav TimNPeans.sav.backup
```

---

## Troubleshooting

### Save File Won't Load
- Ensure you edited the correct offsets
- Check that values are in little-endian format
- Restore from backup and try again
- Make sure file size hasn't changed

### Values Reset After Loading
- Some values may have maximum limits in the game code
- Try using more conservative values (e.g., 999 instead of 9999)
- The game may validate certain values on load

### Game Crashes on Load
- Restore your backup immediately
- You may have corrupted the file structure
- Only edit the specific offsets listed in this guide

---

## Advanced Editing

### Finding New Offsets
If you want to find other editable values:
1. Use the `save_editor.py` script to analyze the file
2. Search for property names in hex (they're stored as ASCII)
3. The value typically appears 25-35 bytes after the property name
4. Values are stored as little-endian 32-bit integers

### Property Name Format
Properties in GVAS files follow this pattern:
```
[PropertyName + \0] + [PropertyType + \0] + [metadata] + [value]
```

Example property names to search for:
- `CurrentCheckpoint\0`
- `EpicPens\0`
- `VehicleParts\0`
- `DamageType.Frame\0`

---

## Save File Locations

### Windows
```
%LOCALAPPDATA%\RideGamejam\Saved\SaveGames\
```

### Linux (Proton/Steam)
```
~/.steam/steam/steamapps/compatdata/[APPID]/pfx/drive_c/users/steamuser/AppData/Local/RideGamejam/Saved/SaveGames/
```

### Steam Cloud
The game may use Steam Cloud saves. Disable cloud saves before editing to prevent sync issues.

---

## Safety Tips

1. ✓ **Always backup before editing**
2. ✓ Test with small value changes first
3. ✓ Close the game before editing
4. ✓ Use reasonable values (avoid extremes)
5. ✗ Don't edit while game is running
6. ✗ Don't modify file size or structure
7. ✗ Don't edit unknown offsets without testing

---

## Example Python Snippet

Quick script to modify a value:

```python
import struct

# Read file
with open('TimNPeans.sav', 'rb') as f:
    data = bytearray(f.read())

# Modify EpicPens to 9999
struct.pack_into('<I', data, 0x0C8E, 9999)

# Save file
with open('TimNPeans_modified.sav', 'wb') as f:
    f.write(data)
```

---

## Credits & Notes

- File format: Unreal Engine GVAS
- Analysis tools: Python + struct module
- All offsets verified on the provided save file
- Offsets may vary if game is updated
- Educational purposes only - use at your own risk

---

## Version History

- v1.0 (2024): Initial analysis and documentation
  - Identified primary values (CurrentCheckpoint, EpicPens, VehicleParts)
  - Identified vehicle damage values (Frame, Engine, Tires)
  - Created editing scripts and examples
