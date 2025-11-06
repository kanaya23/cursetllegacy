"""Discovery and diff logic for modpack syncing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple
import os

from .models import FileAction, FileChange, ModpackInfo, SyncPlan
from .persistence import SyncHistoryStore
from ..utils import filesystem


@dataclass
class SnapshotEntry:
    """Metadata describing a file captured during scanning."""

    relative_path: Path
    absolute_path: Path
    size: int
    mtime: float
    hash_digest: str


def discover_modpacks(instances_path: Path) -> list[ModpackInfo]:
    """Find potential modpacks inside the CurseForge instances directory."""

    if not instances_path.exists():
        return []

    modpacks: list[ModpackInfo] = []
    for entry in sorted(instances_path.iterdir()):
        if not entry.is_dir():
            continue
        manifest = entry / "manifest.json"
        mods_dir = entry / "mods"

        if manifest.exists() or mods_dir.exists():
            icon_path = next((entry / name for name in ("icon.png", "pack.png") if (entry / name).exists()), None)
            modpacks.append(
                ModpackInfo(
                    name=entry.name,
                    path=entry,
                    icon_path=icon_path,
                    manifest_path=manifest if manifest.exists() else None,
                )
            )

    return modpacks


def _gather_snapshot(base_path: Path, exclusions: Iterable[str]) -> Dict[Path, SnapshotEntry]:
    """Collect metadata for files under a base path."""

    normalized_exclusions = {filesystem.normalize_relative(exclusion) for exclusion in exclusions}
    snapshot: Dict[Path, SnapshotEntry] = {}

    if not base_path.exists():
        return snapshot

    for root, _, files in os.walk(base_path):
        root_path = Path(root)
        for filename in files:
            abs_path = root_path / filename
            rel_path = abs_path.relative_to(base_path)
            norm_rel = filesystem.normalize_relative(str(rel_path))
            if norm_rel in normalized_exclusions:
                continue
            try:
                stat_info = abs_path.stat()
            except OSError:
                continue

            hash_digest = filesystem.hash_file(abs_path)
            snapshot[rel_path] = SnapshotEntry(
                relative_path=rel_path,
                absolute_path=abs_path,
                size=stat_info.st_size,
                mtime=stat_info.st_mtime,
                hash_digest=hash_digest,
            )

    return snapshot


def build_sync_plan(
    modpack: ModpackInfo,
    target_path: Path,
    history_store: SyncHistoryStore,
) -> Tuple[SyncPlan, Dict[str, Dict[str, str]], Dict[Path, SnapshotEntry], Dict[Path, SnapshotEntry]]:
    """Generate a synchronization plan for the given modpack.

    Returns the plan, the new snapshot payload, and the raw source/target snapshots.
    """

    plan = SyncPlan()
    history = history_store.get_history(modpack.name)
    exclusions = history.exclusions

    source_snapshot = _gather_snapshot(modpack.path, exclusions)
    target_snapshot = _gather_snapshot(target_path, [])

    history_files = {Path(k): v for k, v in history.files.items()}

    # Determine additions and updates
    for rel_path, source_entry in source_snapshot.items():
        target_entry = target_snapshot.get(rel_path)

        change = FileChange(
            relative_path=rel_path,
            action=FileAction.COPY,
            source_path=source_entry.absolute_path,
            target_path=target_path / rel_path,
            size_bytes=source_entry.size,
            hash_digest=source_entry.hash_digest,
        )

        if target_entry is None:
            plan.adds.append(change)
        else:
            if target_entry.hash_digest != source_entry.hash_digest:
                change.action = FileAction.UPDATE
                change.reason = "Content differs"
                plan.updates.append(change)
            else:
                # Already in sync; mark as skipped
                change.action = FileAction.SKIP
                plan.skipped.append(change)

        # Remove from history tracking to keep track of potential deletions later
        history_files.pop(rel_path, None)

    # Determine removals based on history (files previously synced but no longer present)
    for rel_path, info in history_files.items():
        target_entry = target_snapshot.get(rel_path)
        target_abs = target_path / rel_path

        if info.get("hash") and target_entry and target_entry.hash_digest != info.get("hash"):
            # The target file has drifted; treat as update instead of deletion
            plan.updates.append(
                FileChange(
                    relative_path=rel_path,
                    action=FileAction.UPDATE,
                    source_path=None,
                    target_path=target_abs,
                    reason="Target file changed since last sync",
                )
            )
            continue

        if target_abs.exists():
            plan.removals.append(
                FileChange(
                    relative_path=rel_path,
                    action=FileAction.DELETE,
                    target_path=target_abs,
                    reason="Removed from modpack",
                )
            )

    snapshot_payload = {
        str(rel_path): {
            "hash": entry.hash_digest,
            "size": str(entry.size),
            "mtime": str(entry.mtime),
        }
        for rel_path, entry in source_snapshot.items()
    }

    return plan, snapshot_payload, source_snapshot, target_snapshot
