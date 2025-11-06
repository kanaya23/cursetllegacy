#!/bin/bash
# Linux/Mac launcher script for Minecraft Modpack Sync

# Find Python
if command -v python3 &> /dev/null; then
    python3 run.py
elif command -v python &> /dev/null; then
    python run.py
else
    echo "ERROR: Python not found! Please install Python 3.10 or later."
    exit 1
fi
