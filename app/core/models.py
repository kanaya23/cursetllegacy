"""Domain models for the modpack sync application."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Sequence


class FileAction(str, Enum):
    """Possible actions to take on a file during sync."""

    COPY = "copy"
    UPDATE = "update"
    DELETE = "delete"
    SKIP = "skip"


@dataclass
class FileChange:
    """Represents a single file change between source and target directories."""

    relative_path: Path
    action: FileAction
    source_path: Optional[Path] = None
    target_path: Optional[Path] = None
    size_bytes: Optional[int] = None
    hash_digest: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class SyncPlan:
    """Planned actions for synchronizing a modpack."""

    adds: List[FileChange] = field(default_factory=list)
    updates: List[FileChange] = field(default_factory=list)
    removals: List[FileChange] = field(default_factory=list)
    skipped: List[FileChange] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not (self.adds or self.updates or self.removals)

    def all_changes(self) -> Sequence[FileChange]:
        return [*self.adds, *self.updates, *self.removals, *self.skipped]


@dataclass
class ModpackInfo:
    """Metadata for a detected modpack."""

    name: str
    path: Path
    icon_path: Optional[Path] = None
    manifest_path: Optional[Path] = None


@dataclass
class SyncLogEntry:
    """Record of a sync operation."""

    modpack_name: str
    timestamp: float
    changes: List[FileChange]
    notes: Optional[str] = None


@dataclass
class SyncHistory:
    """Persistent history for a modpack."""

    modpack_name: str
    files: Dict[str, Dict[str, Optional[str]]] = field(default_factory=dict)
    exclusions: List[str] = field(default_factory=list)
    last_synced: Optional[float] = None
