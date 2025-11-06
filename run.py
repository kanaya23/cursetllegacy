#!/usr/bin/env python3
"""Launcher script for the Minecraft Modpack Sync application.

This script ensures the application can be run from anywhere.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add the workspace to the path
workspace_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(workspace_dir))

# Now import and run the application
from app.main import main

if __name__ == "__main__":
    raise SystemExit(main())
