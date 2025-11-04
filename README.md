# Ride Save Game Editor - Complete Package

Welcome! This package contains everything you need to edit your Ride (RideGamejam) save files.

## 📦 What's Included

### 📄 Documentation (Start Here!)
- **SUMMARY.md** - Overview of everything
- **SAVE_EDITING_GUIDE.md** - Comprehensive tutorial
- **QUICK_REFERENCE.txt** - Fast lookup table
- **MEMORY_MAP.txt** - Visual file structure

### 🛠️ Tools
- **save_editor.py** - Analyze your save files
- **interactive_editor.py** - Edit with guided options

### 🎮 Example Files
- **TimNPeans_GodMode.sav** - Pre-modified save (max resources, no damage)

## 🚀 Quick Start

### Want to cheat? (Easiest)
Replace your save file with `TimNPeans_GodMode.sav` for:
- 9999 EpicPens (currency)
- 9999 VehicleParts
- Perfect vehicle condition (0 damage)

### Want to customize? (Python)
```bash
python3 interactive_editor.py
```
Choose from 5 modification options:
1. Max Currency
2. Max Parts
3. Repair Vehicle
4. Reset Progress
5. God Mode (all of the above)

### Want full control? (Hex Editor)
Use any hex editor (HxD, 010 Editor, etc.) and:
1. Open your save file
2. Check **QUICK_REFERENCE.txt** for offsets
3. Edit the values you want
4. Save

## 🎯 Most Common Edits

### Give Yourself Money
- **Offset:** 0x0C8E
- **New Value:** `0F 27 00 00` (9999 in hex)

### Get More Parts
- **Offset:** 0x0CBC
- **New Value:** `0F 27 00 00` (9999 in hex)

### Repair Your Vehicle
Set all these offsets to `00 00 00 00`:
- 0x085B (Frame)
- 0x0925 (Engine)
- 0x09F0, 0x0ABB, 0x0B86, 0x0C51 (All Tires)

## ⚠️ Before You Start

1. **Backup your save file!** Cannot stress this enough.
2. **Close the game** before editing
3. **Test small changes first** to be safe

## 📊 Discovered Values

| What               | Where   | Current | Range    |
|--------------------|---------|---------|----------|
| Checkpoint         | 0x0735  | 9       | 0-?      |
| EpicPens           | 0x0C8E  | 16      | 0-9999   |
| VehicleParts       | 0x0CBC  | 20      | 0-9999   |
| Frame Damage       | 0x085B  | 0       | 0-100    |
| Engine Damage      | 0x0925  | 0       | 0-100    |
| Tire Damage (x4)   | various | 0       | 0-100    |

## 📚 Need More Help?

1. **New to hex editing?** → Read SAVE_EDITING_GUIDE.md
2. **Want quick reference?** → See QUICK_REFERENCE.txt
3. **Want to see structure?** → Check MEMORY_MAP.txt
4. **Having problems?** → Troubleshooting section in SAVE_EDITING_GUIDE.md

## 💾 Save File Location

**Windows:**
```
%LOCALAPPDATA%\RideGamejam\Saved\SaveGames\
```

**Linux (Steam/Proton):**
```
~/.steam/steam/steamapps/compatdata/[APPID]/pfx/drive_c/users/steamuser/AppData/Local/RideGamejam/Saved/SaveGames/
```

## ✅ Verified & Tested

All values and offsets have been verified on:
- File: TimNPeans.sav (24,822 bytes)
- Game: Ride (RideGamejam)
- Format: Unreal Engine GVAS v3

## ⚙️ Requirements

**For Python scripts:**
- Python 3.6 or higher
- No external dependencies needed (uses built-in modules)

**For manual editing:**
- Any hex editor (HxD, 010 Editor, Hex Fiend, etc.)

## 🎓 Learning Resources

Included in this package:
- Complete file format documentation
- Hex editing tutorial
- Understanding little-endian values
- Finding new values (advanced)

## 🔒 Safety & Legal

- ✅ Backup before editing (seriously!)
- ✅ Single-player game modifications
- ✅ Educational purposes
- ⚠️ Use at your own risk
- ⚠️ May affect achievements
- ⚠️ Disable Steam Cloud before editing

## 🤝 Support

If something doesn't work:
1. Check your backup exists
2. Verify file size is still 24,822 bytes
3. Make sure values are in little-endian format
4. Try the pre-made God Mode save to test
5. Consult the troubleshooting section

## 📦 Package Contents Summary

```
📁 Save Game Editor Package
│
├── 📄 README.md (you are here)
├── 📄 SUMMARY.md
├── 📄 SAVE_EDITING_GUIDE.md
├── 📄 QUICK_REFERENCE.txt
├── 📄 MEMORY_MAP.txt
│
├── 🐍 save_editor.py
├── 🐍 interactive_editor.py
│
└── 💾 TimNPeans_GodMode.sav
```

## 🎉 Ready to Start!

1. Backup your save (seriously!)
2. Choose your editing method
3. Follow the guides
4. Enjoy the game your way!

---

**Package Version:** 1.0
**Last Updated:** November 2024
**Game:** Ride (RideGamejam)

Happy editing! 🎮✨
