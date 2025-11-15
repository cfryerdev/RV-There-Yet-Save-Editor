# RV There Yet Save Game Editor - Sample Project

Welcome! This package contains everything you need to edit your Ride save files. Note: This is just a tech demo of having Claude attempt at looking at a save file for a game it does not know, do an analysis, and build a save editor. Its also rather amusing that it thinks EpicPens are currency/money or something lol

## 📦 What's Included

### 📄 Documentation
- [QUICK_REFERENCE.txt](/docs/QUICK_REFERENCE.txt) - Fast lookup table
- [MEMORY_MAP.txt](/docs/MEMORY_MAP.txt) - Visual file structure

### 🛠️ Tools
- **interactive_editor.py** - Edit with guided options

## 🚀 Quick Start

Put your save file into the /saves directory, then:

```bash
python3 interactive_editor.py
```
Choose from 6 modification options:
1. Max HealthPacks
2. Max Parts
3. Repair Vehicle
4. Reset Progress
5. God Mode (all of the above)
6. Set Progress Checkpoint (custom value 1-17)

### Want full control? (Hex Editor)
Use any hex editor (HxD, 010 Editor, etc.) and:
1. Open your save file
2. Check **QUICK_REFERENCE.txt** for offsets
3. Edit the values you want
4. Save


## ⚠️ Before You Start

1. **Backup your save file!** Cannot stress this enough.
2. **Close the game** before editing
3. **Test small changes first** to be safe

## 💾 Save File Location

**Windows:**
```
%LOCALAPPDATA%\RideGamejam\Saved\SaveGames\
```

**Linux (Steam/Proton):**
```
~/.steam/steam/steamapps/compatdata/[APPID]/pfx/drive_c/users/steamuser/AppData/Local/RideGamejam/Saved/SaveGames/
```

## ⚙️ Requirements

**For Python scripts:**
- Python 3.6 or higher
- No external dependencies needed (uses built-in modules)

**Package Version:** 1.0
**Last Updated:** November 2024
**Game:** Ride (RideGamejam)

Happy editing! 🎮✨
