"""Application entry point for the Minecraft modpack sync tool."""

from __future__ import annotations

import logging
import sys

from PyQt6 import QtWidgets

from .gui.main_window import create_main_window


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
