"""Filesystem helper utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import hashlib
import os
import shutil
import time


BUFFER_SIZE = 1024 * 1024


def hash_file(path: Path) -> str:
    """Calculate a SHA-256 hash for the given file."""

    digest = hashlib.sha256()
    try:
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(BUFFER_SIZE), b""):
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest()


def normalize_relative(rel_path: str) -> str:
    """Normalize a relative path to a standard forward-slash form."""

    return rel_path.replace("\\", "/")


def ensure_parent(path: Path) -> None:
    """Create parent directories for the given path if they do not exist."""

    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(source: Path, destination: Path) -> None:
    """Copy a file to the destination, preserving metadata."""

    ensure_parent(destination)
    shutil.copy2(source, destination)


def remove_file(path: Path) -> None:
    """Remove the given file if it exists."""

    try:
        path.unlink()
    except FileNotFoundError:
        return


def create_backup(source: Path, backup_root: Path) -> Optional[Path]:
    """Create a timestamped backup of a file under the backup directory."""

    if not backup_root:
        return None

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    relative = source.name
    backup_dir = backup_root / timestamp
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        target = backup_dir / relative
        shutil.copy2(source, target)
        return target
    except OSError:
        return None


def prune_empty_dirs(base_path: Path) -> None:
    """Remove empty directories under the given base path."""

    if not base_path.exists():
        return

    # Walk bottom-up to remove empty folders
    for root, dirs, _ in os.walk(base_path, topdown=False):
        root_path = Path(root)
        for d in dirs:
            candidate = root_path / d
            try:
                candidate.rmdir()
            except OSError:
                continue
