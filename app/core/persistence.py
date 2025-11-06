"""Persistence helpers for sync history and exclusions."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import json
import threading
import time

from .models import SyncHistory, FileChange


class SyncHistoryStore:
    """Manage persistence of sync history data."""

    def __init__(self, history_path: Path) -> None:
        self.history_path = history_path
        self._lock = threading.Lock()
        self._cache: Dict[str, SyncHistory] = {}
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_raw(self) -> Dict[str, Dict]:
        if not self.history_path.exists():
            return {}
        try:
            return json.loads(self.history_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_raw(self, data: Dict[str, Dict]) -> None:
        self.history_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_all(self) -> Dict[str, SyncHistory]:
        with self._lock:
            if self._cache:
                return self._cache
            raw = self._read_raw()
            for modpack, payload in raw.items():
                self._cache[modpack] = SyncHistory(
                    modpack_name=modpack,
                    files=payload.get("files", {}),
                    exclusions=payload.get("exclusions", []),
                    last_synced=payload.get("last_synced"),
                )
            return self._cache

    def get_history(self, modpack_name: str) -> SyncHistory:
        histories = self.load_all()
        if modpack_name in histories:
            return histories[modpack_name]
        history = SyncHistory(modpack_name=modpack_name)
        histories[modpack_name] = history
        return history

    def append_log(self, modpack_name: str, changes: Optional[list[FileChange]] = None) -> None:
        history = self.get_history(modpack_name)
        history.last_synced = time.time()
        self.save_history(history)

    def save_history(self, history: SyncHistory) -> None:
        with self._lock:
            raw = self._read_raw()
            raw[history.modpack_name] = {
                "files": history.files,
                "exclusions": history.exclusions,
                "last_synced": history.last_synced,
            }
            self._write_raw(raw)
            self._cache[history.modpack_name] = history

    def update_file_snapshot(self, modpack_name: str, snapshot: Dict[str, Dict[str, str]]) -> None:
        history = self.get_history(modpack_name)
        history.files = snapshot
        history.last_synced = time.time()
        self.save_history(history)

    def add_exclusion(self, modpack_name: str, relative_path: str) -> None:
        history = self.get_history(modpack_name)
        if relative_path not in history.exclusions:
            history.exclusions.append(relative_path)
            self.save_history(history)

    def remove_exclusion(self, modpack_name: str, relative_path: str) -> None:
        history = self.get_history(modpack_name)
        if relative_path in history.exclusions:
            history.exclusions.remove(relative_path)
            self.save_history(history)
