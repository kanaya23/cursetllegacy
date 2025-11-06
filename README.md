# 🎮 Minecraft Modpack Sync Tool

A modern, professional desktop application for synchronising Minecraft modpacks installed via CurseForge with a custom launcher directory.

## ✨ Features

This tool offers:

- 📦 **Automatic modpack detection** within the CurseForge instances directory
- 🔍 **Clear preview** of files that will be added, updated, or removed before committing changes
- ✅ **File-level confirmations** for updates and removals
- 📊 **Persistent history** to track which files were synced previously
- 🚫 **Optional exclusions** to keep specific files from being synced again
- ⚙️ **Configurable paths**, optional backups, progress reporting, and a detailed log view
- 🎨 **Modern, professional UI** with intuitive design and visual feedback
- 🔒 **Safe operations** with backup support and confirmation dialogs

The application is built with Python and PyQt6, providing a modern, professional, and intuitive GUI with:
- Clean, modern design with rounded corners and professional color scheme
- Real-time progress tracking and status updates
- Emoji icons for better visual clarity
- Color-coded file changes (green for additions, orange for updates, red for removals)
- Dark-themed log output for easy reading
- Responsive layout with adjustable panels

## Getting Started

### Prerequisites

- Python 3.10 or later
- Pip (Python package manager)

### Installation

1. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Windows:**
- Double-click `run.bat` or run in command prompt:
  ```cmd
  run.bat
  ```

**Linux/Mac:**
```bash
./run.sh
```

**Or using Python directly:**
```bash
python -m app.main
# or
python run.py
# or from the app directory
cd app
python main.py
```

On first launch the app attempts to use the default Windows paths `F:\Game\Minecraft\Instances` and `F:\Game\Minecraft\game`. Use the directory controls at the top of the window to point the tool at custom locations if needed.

## Key Features

- **Modpack Detection**: Automatically discovers available modpacks and displays them for selection.
- **Sync Preview**: Shows a colour-coded list of pending actions before syncing, including additions, updates, and removals.
- **Confirmations & Safety**: Requests confirmation before replacing or deleting files, with optional automatic backups.
- **History & Exclusions**: Tracks synced files and enables excluding specific items from future operations.
- **Configurable Paths**: Save custom directories for both CurseForge instances and the custom launcher.
- **Progress & Logs**: Displays real-time progress and maintains a log of operations for review.

## 📝 Notes

- Sync history, exclusions, and configuration are stored under `~/.minecraft_modsync/` by default
- The application follows the folder structure inside each modpack, copying matching directories into the target launcher folder
- Removed files are highlighted and require explicit confirmation before being deleted from the target directory
- All operations are logged with timestamps for easy troubleshooting
- The GUI automatically validates paths and provides helpful error messages

## 🎨 UI Features

The modernized GUI includes:
- **Professional color scheme** with Material Design inspired colors
- **Smooth interactions** with hover effects and visual feedback
- **Better organization** with clearly grouped sections
- **Improved readability** with proper spacing and typography
- **Status indicators** with emoji icons for quick visual reference
- **Responsive design** that adapts to different window sizes
- **Dark log console** for better readability of technical output

## Development

The source code lives under `app/` and is organised into:

- `core/` for configuration, persistence, scanning, and sync execution logic.
- `gui/` for the PyQt6 user interface components.
- `utils/` for filesystem helper utilities.

You can extend the application by adding new features to these modules or introducing additional GUI panels.