"""Synchronization execution for modpack files."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional
import logging

from .config import AppConfig, ConfigManager
from .models import FileAction, FileChange, ModpackInfo, SyncPlan
from .persistence import SyncHistoryStore
from .scanner import build_sync_plan, discover_modpacks
from ..utils import filesystem


logger = logging.getLogger(__name__)


ConfirmationCallback = Callable[[FileChange], bool]
ProgressCallback = Callable[[str, int, int], None]  # message, current, total
LogCallback = Callable[[str], None]


class SyncEngine:
    """High-level controller handling discovery, planning, and execution."""

    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        log_callback: Optional[LogCallback] = None,
    ) -> None:
        self.config_manager = config_manager or ConfigManager()
        self.config: AppConfig = self.config_manager.load()
        history_path = self.config.history_path or ConfigManager.default_app_dir() / "sync_history.json"
        self.history_store = SyncHistoryStore(history_path)
        self.log_callback = log_callback

    def _log(self, message: str) -> None:
        logger.info(message)
        if self.log_callback:
            self.log_callback(message)

    # Discovery -----------------------------------------------------------------
    def list_modpacks(self) -> list[ModpackInfo]:
        return discover_modpacks(self.config.instances_path)

    # Planning -------------------------------------------------------------------
    def create_sync_plan(self, modpack: ModpackInfo) -> tuple[SyncPlan, dict, dict, dict]:
        target_path = self.config.game_path
        return build_sync_plan(modpack, target_path, self.history_store)

    # Execution ------------------------------------------------------------------
    def execute_plan(
        self,
        modpack: ModpackInfo,
        plan: SyncPlan,
        snapshot_payload: dict,
        auto_confirm_updates: Optional[bool] = None,
        auto_confirm_removals: Optional[bool] = None,
        create_backups: bool = False,
        confirm_update: Optional[ConfirmationCallback] = None,
        confirm_removal: Optional[ConfirmationCallback] = None,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> None:
        """Apply a sync plan with optional confirmation callbacks."""

        target_path = self.config.game_path
        
        # Validate target path exists
        if not target_path.exists():
            raise ValueError(f"Target game path does not exist: {target_path}")
        backup_root = self.config.backup_dir if create_backups else None

        total_items = len(plan.adds) + len(plan.updates) + len(plan.removals)
        processed = 0

        auto_confirm_updates = (
            self.config.auto_confirm_updates if auto_confirm_updates is None else auto_confirm_updates
        )
        auto_confirm_removals = (
            self.config.auto_confirm_removals if auto_confirm_removals is None else auto_confirm_removals
        )

        def tick(message: str) -> None:
            nonlocal processed
            processed += 1
            if progress_callback:
                progress_callback(message, processed, total_items)

        for change in plan.adds:
            destination = change.target_path or (target_path / change.relative_path)
            if destination.exists():
                # Treat as update if somehow already exists
                change.action = FileAction.UPDATE
                plan.updates.append(change)
                continue
            source_path = change.source_path
            if not source_path or not source_path.exists():
                self._log(f"Source missing for {change.relative_path}, skipping")
                continue
            filesystem.copy_file(source_path, destination)
            self._log(f"Copied {change.relative_path}")
            tick(f"Copied {change.relative_path}")

        for change in list(plan.updates):
            destination = change.target_path or (target_path / change.relative_path)
            source_path = change.source_path

            if not auto_confirm_updates:
                allowed = confirm_update(change) if confirm_update else False
                if not allowed:
                    plan.skipped.append(change)
                    self._log(f"Skipped update for {change.relative_path}")
                    tick(f"Skipped {change.relative_path}")
                    continue

            if source_path and source_path.exists():
                if backup_root and destination.exists():
                    filesystem.create_backup(destination, backup_root)
                filesystem.copy_file(source_path, destination)
                self._log(f"Updated {change.relative_path}")
            else:
                self._log(f"Target changed externally: {change.relative_path}")
            tick(f"Updated {change.relative_path}")

        for change in plan.removals:
            destination = change.target_path or (target_path / change.relative_path)
            if not destination.exists():
                continue

            if not auto_confirm_removals:
                allowed = confirm_removal(change) if confirm_removal else False
                if not allowed:
                    plan.skipped.append(change)
                    self._log(f"Kept {change.relative_path}")
                    tick(f"Kept {change.relative_path}")
                    continue

            if backup_root:
                filesystem.create_backup(destination, backup_root)
            filesystem.remove_file(destination)
            self._log(f"Removed {change.relative_path}")
            tick(f"Removed {change.relative_path}")

        self.history_store.update_file_snapshot(modpack.name, snapshot_payload)
        filesystem.prune_empty_dirs(self.config.game_path)

    # Exclusions -----------------------------------------------------------------
    def add_exclusion(self, modpack_name: str, relative_path: str) -> None:
        self.history_store.add_exclusion(modpack_name, filesystem.normalize_relative(relative_path))

    def remove_exclusion(self, modpack_name: str, relative_path: str) -> None:
        self.history_store.remove_exclusion(modpack_name, filesystem.normalize_relative(relative_path))

    # Configuration ---------------------------------------------------------------
    def update_paths(self, instances_path: Path, game_path: Path) -> None:
        self.config.instances_path = instances_path
        self.config.game_path = game_path
        self.config_manager.save(self.config)
