# Minecraft Modpack Sync Tool

This project provides a desktop application for synchronising Minecraft modpacks installed via CurseForge with a custom launcher directory. The tool offers:

- Automatic modpack detection within the CurseForge instances directory.
- Clear preview of files that will be added, updated, or removed before committing changes.
- File-level confirmations for updates and removals.
- Persistent history to track which files were synced previously.
- Optional exclusions to keep specific files from being synced again.
- Configurable source/target paths, optional backups, progress reporting, and a detailed log view.

The application is built with Python and PyQt6, providing a modern and intuitive GUI.

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

```bash
python -m app.main
```

On first launch the app attempts to use the default Windows paths `F:\Game\Minecraft\Instances` and `F:\Game\Minecraft\game`. Use the directory controls at the top of the window to point the tool at custom locations if needed.

## Key Features

- **Modpack Detection**: Automatically discovers available modpacks and displays them for selection.
- **Sync Preview**: Shows a colour-coded list of pending actions before syncing, including additions, updates, and removals.
- **Confirmations & Safety**: Requests confirmation before replacing or deleting files, with optional automatic backups.
- **History & Exclusions**: Tracks synced files and enables excluding specific items from future operations.
- **Configurable Paths**: Save custom directories for both CurseForge instances and the custom launcher.
- **Progress & Logs**: Displays real-time progress and maintains a log of operations for review.

## Notes

- Sync history, exclusions, and configuration are stored under `~/.minecraft_modsync/` by default.
- The application follows the folder structure inside each modpack, copying matching directories into the target launcher folder.
- Removed files are highlighted and require explicit confirmation before being deleted from the target directory.

## Development

The source code lives under `app/` and is organised into:

- `core/` for configuration, persistence, scanning, and sync execution logic.
- `gui/` for the PyQt6 user interface components.
- `utils/` for filesystem helper utilities.

You can extend the application by adding new features to these modules or introducing additional GUI panels.