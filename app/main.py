"""Application entry point for the Minecraft modpack sync tool."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Fix imports to work when running directly or as module
if __name__ == "__main__" and __package__ is None:
    # Add parent directory to path when running directly
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "app"

from PyQt6 import QtWidgets

from app.gui.main_window import create_main_window


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(name)s: %(message)s",
    )


def main() -> int:
    setup_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = create_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
