"""Configuration management for the modpack sync application."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any, Set
import json


APP_DIR_NAME = "minecraft_modsync"
CONFIG_FILENAME = "config.json"
HISTORY_FILENAME = "sync_history.json"


def _default_instances_path() -> Path:
    """Return the default CurseForge instances path depending on the OS."""

    # Default to Windows-style path requested by the user, but fall back gracefully.
    candidate = Path("F:/Game/Minecraft/Instances")
    if candidate.exists():
        return candidate

    # Try common alternative locations
    home = Path.home()
    ideas = [
        home / "CurseForge" / "minecraft" / "Instances",
        home / "Documents" / "CurseForge" / "minecraft" / "Instances",
    ]
    for idea in ideas:
        if idea.exists():
            return idea

    return candidate


def _default_game_path() -> Path:
    """Return the default custom launcher path."""

    candidate = Path("F:/Game/Minecraft/game")
    if candidate.exists():
        return candidate

    home = Path.home()
    ideas = [
        home / ".minecraft",
        home / "Games" / "Minecraft",
    ]
    for idea in ideas:
        if idea.exists():
            return idea

    return candidate


@dataclass
class AppConfig:
    """Configuration data for the application."""

    instances_path: Path
    game_path: Path
    backup_dir: Optional[Path] = None
    auto_confirm_new_files: bool = True
    auto_confirm_updates: bool = False
    auto_confirm_removals: bool = False
    exclusions_path: Optional[Path] = None
    history_path: Optional[Path] = None

    @classmethod
    def default(cls) -> "AppConfig":
        """Return the default configuration."""

        app_dir = ConfigManager.default_app_dir()
        return cls(
            instances_path=_default_instances_path(),
            game_path=_default_game_path(),
            backup_dir=app_dir / "backups",
            exclusions_path=app_dir / "exclusions.json",
            history_path=app_dir / HISTORY_FILENAME,
        )

    def to_json(self) -> Dict[str, Any]:
        """Serialize configuration to JSON-compatible dict."""

        data = asdict(self)
        for key, value in list(data.items()):
            if isinstance(value, Path):
                data[key] = str(value)
        return data

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "AppConfig":
        """Deserialize configuration from JSON-compatible dict."""

        kwargs: Dict[str, Any] = {}
        path_fields: Set[str] = {
            "instances_path",
            "game_path",
            "backup_dir",
            "exclusions_path",
            "history_path",
        }

        for field_name in cls.__dataclass_fields__:
            if field_name in data:
                value = data[field_name]
                if value is not None and field_name in path_fields:
                    kwargs[field_name] = Path(value)
                else:
                    kwargs[field_name] = value

        defaults = cls.default()
        for field_name, default_value in defaults.__dict__.items():
            kwargs.setdefault(field_name, default_value)

        return cls(**kwargs)


class ConfigManager:
    """Handle loading/saving of the application configuration."""

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config_path = config_path or self.default_config_path()
        self._config: Optional[AppConfig] = None

    @staticmethod
    def default_app_dir() -> Path:
        """Return the default directory for storing application data."""

        app_dir = Path.home() / APP_DIR_NAME
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir

    @classmethod
    def default_config_path(cls) -> Path:
        """Return the default configuration file path."""

        return cls.default_app_dir() / CONFIG_FILENAME

    def load(self) -> AppConfig:
        """Load configuration from disk, creating defaults if needed."""

        if self._config is not None:
            return self._config

        if self.config_path.exists():
            try:
                raw_data = json.loads(self.config_path.read_text(encoding="utf-8"))
                self._config = AppConfig.from_json(raw_data)
            except (json.JSONDecodeError, OSError):
                self._config = AppConfig.default()
        else:
            self._config = AppConfig.default()
            self.save(self._config)

        if self._config.backup_dir:
            self._config.backup_dir.mkdir(parents=True, exist_ok=True)

        return self._config

    def save(self, config: Optional[AppConfig] = None) -> None:
        """Persist configuration to disk."""

        config_to_save = config or self._config
        if config_to_save is None:
            config_to_save = AppConfig.default()
        self.config_path.write_text(
            json.dumps(config_to_save.to_json(), indent=2), encoding="utf-8"
        )
        self._config = config_to_save
