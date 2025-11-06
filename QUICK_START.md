# 🚀 Quick Start Guide

## Installation

1. **Ensure Python is installed** (3.10 or later)
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Windows
Simply double-click `run.bat` or open command prompt:
```cmd
run.bat
```

### Linux/Mac
Make executable and run:
```bash
chmod +x run.sh
./run.sh
```

### Alternative Methods
```bash
# Using the Python launcher
python run.py

# Using module import
python -m app.main

# Direct execution (now fixed!)
cd app
python main.py
```

## First Time Setup

1. **Launch the application** using any method above

2. **Configure Paths**:
   - Click "📂 Browse" next to "CurseForge Instances"
   - Navigate to your CurseForge instances folder
   - Click "📂 Browse" next to "Custom Launcher Game"
   - Navigate to your game directory
   - Click "💾 Save Paths"

3. **You're ready!** The app will now display your modpacks

## Basic Usage

### Syncing a Modpack

1. **Select** a modpack from the left panel
2. **Preview** changes by clicking "🔍 Preview Changes"
3. **Review** the color-coded list:
   - ➕ Green = Files to add
   - 🔄 Orange = Files to update
   - 🗑️ Red = Files to remove
4. **(Optional)** Check "💾 Create backup before syncing"
5. **Sync** by clicking "✨ Sync Now"
6. **Confirm** when prompted

### Tips

- 🔄 Use "Refresh Modpacks" if you add new modpacks
- 🚫 Select a file and click "Exclude Selected" to skip it in future syncs
- 📋 Check the log panel for detailed operation information
- 🗑️ Click "Clear Log" to reset the log view

## Troubleshooting

### Import Error
✅ **Fixed!** The application now handles imports correctly from any location.

### Python Not Found
- **Windows**: Install from [python.org](https://python.org)
- **Linux**: `sudo apt install python3` (or your package manager)
- **Mac**: `brew install python3`

### PyQt6 Not Found
```bash
pip install PyQt6
# or
pip install -r requirements.txt
```

### Path Doesn't Exist
- Verify the path is correct
- Check you have read permissions
- Use the Browse button to select the directory

## What's New in Version 2.0

✨ **Complete GUI overhaul** with modern, professional design
🐛 **Fixed import error** - now works from anywhere
🎨 **Material Design** color scheme and styling
📊 **Enhanced validation** and error handling
📚 **Comprehensive documentation**

## Support

- Check `MODERNIZATION_SUMMARY.md` for full details
- Review `CHANGELOG.md` for all changes
- See `BEFORE_AFTER.md` for visual comparisons
- Read `README.md` for complete documentation

## File Structure

```
workspace/
├── run.py              ← Run this
├── run.bat             ← Or this (Windows)
├── run.sh              ← Or this (Linux/Mac)
├── README.md           ← Full documentation
├── QUICK_START.md      ← This file
├── CHANGELOG.md        ← All changes
├── MODERNIZATION_SUMMARY.md ← Detailed summary
├── BEFORE_AFTER.md     ← Visual comparison
├── requirements.txt    ← Dependencies
└── app/                ← Application code
    ├── main.py
    ├── core/
    ├── gui/
    └── utils/
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Run the application
3. ✅ Configure your paths
4. ✅ Start syncing modpacks!

**Enjoy your modernized Minecraft Modpack Sync tool!** 🎮✨
