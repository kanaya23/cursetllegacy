"""Main window for the Minecraft modpack sync application."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from ..core.config import ConfigManager
from ..core.models import FileChange, ModpackInfo, SyncPlan
from ..core.syncer import SyncEngine


# Modern color scheme
COLORS = {
    "primary": "#42A5F5",          # Mid blue accent
    "primary_dark": "#1E88E5",     # Darker blue accent
    "primary_light": "#64B5F6",    # Lighter blue accent
    "success": "#66BB6A",          # Green accent
    "warning": "#FFA726",          # Amber accent
    "danger": "#EF5350",           # Red accent
    "background": "#121212",       # App background
    "surface": "#1E1E1E",          # Surface panels
    "text_primary": "#E0E0E0",     # Light gray text
    "text_secondary": "#B0BEC5",   # Muted text
    "border": "#2D2D2D",           # Subtle border
    "hover": "#1F2A33",            # Hover highlight
}


def get_modern_stylesheet() -> str:
    """Return a modern stylesheet for the application."""
    return f"""
        QMainWindow {{
            background-color: {COLORS['background']};
            color: {COLORS['text_primary']};
        }}

        QWidget {{
            color: {COLORS['text_primary']};
        }}

        QGroupBox {{
            font-weight: bold;
            font-size: 13px;
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: {COLORS['surface']};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 5px;
            color: {COLORS['primary_light']};
        }}

        QPushButton {{
            background-color: {COLORS['primary']};
            color: #ffffff;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 12px;
            font-weight: 500;
            min-height: 20px;
        }}

        QPushButton:hover {{
            background-color: {COLORS['primary_dark']};
        }}

        QPushButton:pressed {{
            background-color: {COLORS['primary_dark']};
            padding-top: 12px;
            padding-bottom: 8px;
        }}

        QPushButton:disabled {{
            background-color: {COLORS['border']};
            color: {COLORS['text_secondary']};
        }}

        QPushButton#syncButton {{
            background-color: {COLORS['success']};
            color: #0B130C;
        }}

        QPushButton#syncButton:hover {{
            background-color: #57A75F;
        }}

        QPushButton#excludeButton {{
            background-color: {COLORS['warning']};
            color: #23170A;
        }}

        QPushButton#excludeButton:hover {{
            background-color: #F18F1C;
        }}

        QPushButton#refreshButton {{
            background-color: {COLORS['primary']};
        }}

        QLineEdit {{
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #181818;
            font-size: 12px;
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['primary_dark']};
            selection-color: #ffffff;
        }}

        QLineEdit:focus {{
            border-color: {COLORS['primary']};
        }}

        QListWidget {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            background-color: {COLORS['surface']};
            padding: 8px;
            font-size: 12px;
            alternate-background-color: #181818;
        }}

        QListWidget::item {{
            border-radius: 4px;
            padding: 10px;
            margin: 2px;
        }}

        QListWidget::item:selected {{
            background-color: {COLORS['primary_dark']};
            color: #ffffff;
        }}

        QListWidget::item:hover {{
            background-color: {COLORS['hover']};
        }}

        QTreeWidget {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            background-color: {COLORS['surface']};
            alternate-background-color: #181818;
            font-size: 12px;
        }}

        QTreeWidget::item {{
            padding: 6px;
            border-radius: 4px;
        }}

        QTreeWidget::item:selected {{
            background-color: {COLORS['primary_dark']};
            color: {COLORS['text_primary']};
        }}

        QTreeWidget::item:hover {{
            background-color: {COLORS['hover']};
        }}

        QHeaderView::section {{
            background-color: {COLORS['primary_dark']};
            color: #ffffff;
            padding: 8px;
            border: none;
            font-weight: bold;
            font-size: 12px;
        }}

        QHeaderView::section:first {{
            border-top-left-radius: 8px;
        }}

        QHeaderView::section:last {{
            border-top-right-radius: 8px;
        }}

        QPlainTextEdit {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            background-color: #0F1720;
            color: #C5CED9;
            padding: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            line-height: 1.5;
        }}

        QProgressBar {{
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            text-align: center;
            background-color: {COLORS['surface']};
            color: {COLORS['text_primary']};
            font-weight: 500;
            font-size: 11px;
        }}

        QProgressBar::chunk {{
            background-color: {COLORS['success']};
            border-radius: 4px;
        }}

        QCheckBox {{
            font-size: 12px;
            color: {COLORS['text_primary']};
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            background-color: {COLORS['surface']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {COLORS['primary']};
            border-color: {COLORS['primary']};
        }}

        QLabel {{
            color: {COLORS['text_primary']};
            font-size: 12px;
        }}

        QStatusBar {{
            background-color: {COLORS['surface']};
            color: {COLORS['text_secondary']};
            border-top: 1px solid {COLORS['border']};
            font-size: 11px;
        }}

        QToolTip {{
            background-color: #2A2F37;
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 5px;
            font-size: 11px;
        }}

        QSplitter::handle {{
            background-color: {COLORS['border']};
            width: 2px;
        }}

        QSplitter::handle:hover {{
            background-color: {COLORS['primary']};
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {COLORS['background']};
            width: 14px;
            border-radius: 7px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {COLORS['border']};
            border-radius: 7px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {COLORS['primary']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            border: none;
            background-color: {COLORS['background']};
            height: 14px;
            border-radius: 7px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {COLORS['border']};
            border-radius: 7px;
            min-width: 30px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {COLORS['primary']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """


# ============================================================================
# Worker Threads for Long-Running Operations
# ============================================================================

class RefreshModpacksWorker(QtCore.QThread):
    """Worker thread for refreshing the modpack list."""
    
    finished = QtCore.pyqtSignal(list)  # list of ModpackInfo
    error = QtCore.pyqtSignal(str)
    
    def __init__(self, engine: SyncEngine, parent=None):
        super().__init__(parent)
        self.engine = engine
    
    def run(self):
        try:
            modpacks = self.engine.list_modpacks()
            self.finished.emit(modpacks)
        except Exception as e:
            self.error.emit(str(e))


class PreviewWorker(QtCore.QThread):
    """Worker thread for building a sync plan."""
    
    finished = QtCore.pyqtSignal(object, dict)  # SyncPlan, snapshot_payload
    error = QtCore.pyqtSignal(str)
    
    def __init__(self, engine: SyncEngine, modpack: ModpackInfo, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.modpack = modpack
    
    def run(self):
        try:
            plan, snapshot_payload, *_ = self.engine.create_sync_plan(self.modpack)
            self.finished.emit(plan, snapshot_payload)
        except Exception as e:
            self.error.emit(str(e))


class SyncWorker(QtCore.QThread):
    """Worker thread for executing a sync plan."""
    
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(str, int, int)  # message, current, total
    confirm_update_signal = QtCore.pyqtSignal(object)  # FileChange
    confirm_removal_signal = QtCore.pyqtSignal(object)  # FileChange
    
    def __init__(
        self,
        engine: SyncEngine,
        modpack: ModpackInfo,
        plan: SyncPlan,
        snapshot_payload: dict,
        create_backups: bool,
        parent=None
    ):
        super().__init__(parent)
        self.engine = engine
        self.modpack = modpack
        self.plan = plan
        self.snapshot_payload = snapshot_payload
        self.create_backups = create_backups
        self.confirmation_responses = {}
        self._mutex = QtCore.QMutex()
        self._wait_condition = QtCore.QWaitCondition()
    
    def confirm_update(self, change: FileChange) -> bool:
        """Called from worker thread, signals GUI thread for confirmation."""
        key = id(change)
        self.confirm_update_signal.emit(change)
        
        # Wait for response from GUI thread
        self._mutex.lock()
        self._wait_condition.wait(self._mutex)
        result = self.confirmation_responses.get(key, False)
        self._mutex.unlock()
        return result
    
    def confirm_removal(self, change: FileChange) -> bool:
        """Called from worker thread, signals GUI thread for confirmation."""
        key = id(change)
        self.confirm_removal_signal.emit(change)
        
        # Wait for response from GUI thread
        self._mutex.lock()
        self._wait_condition.wait(self._mutex)
        result = self.confirmation_responses.get(key, False)
        self._mutex.unlock()
        return result
    
    def set_confirmation_response(self, change: FileChange, response: bool):
        """Called from GUI thread to provide confirmation response."""
        key = id(change)
        self._mutex.lock()
        self.confirmation_responses[key] = response
        self._wait_condition.wakeAll()
        self._mutex.unlock()
    
    def run(self):
        try:
            self.engine.execute_plan(
                modpack=self.modpack,
                plan=self.plan,
                snapshot_payload=self.snapshot_payload,
                create_backups=self.create_backups,
                confirm_update=self.confirm_update,
                confirm_removal=self.confirm_removal,
                progress_callback=lambda msg, cur, tot: self.progress.emit(msg, cur, tot),
            )
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    """Primary application window."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Minecraft Modpack Sync")
        self.resize(1400, 850)
        
        # Set application icon (using default system icon if no custom one)
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon))

        self.config_manager = ConfigManager()
        self.engine = SyncEngine(config_manager=self.config_manager, log_callback=self.append_log)

        self.modpacks: list[ModpackInfo] = []
        self.selected_modpack: Optional[ModpackInfo] = None
        self.current_plan: Optional[SyncPlan] = None
        self.current_snapshot_payload: Optional[dict] = None
        
        # Worker thread references
        self.refresh_worker: Optional[RefreshModpacksWorker] = None
        self.preview_worker: Optional[PreviewWorker] = None
        self.sync_worker: Optional[SyncWorker] = None

        self._setup_ui()
        self._apply_modern_styling()
        self._load_initial_state()

    def _apply_modern_styling(self) -> None:
        """Apply modern stylesheet to the application."""
        self.setStyleSheet(get_modern_stylesheet())

    # ------------------------------------------------------------------ UI SETUP
    def _setup_ui(self) -> None:
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Header with title
        header_layout = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("🎮 Minecraft Modpack Sync")
        title_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS['primary']};
            padding: 10px;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Paths configuration area
        paths_group = QtWidgets.QGroupBox("📁 Directory Configuration", parent=central_widget)
        paths_layout = QtWidgets.QGridLayout(paths_group)
        paths_layout.setContentsMargins(16, 20, 16, 16)
        paths_layout.setHorizontalSpacing(12)
        paths_layout.setVerticalSpacing(12)

        # CurseForge Instances path
        instances_label = QtWidgets.QLabel("CurseForge Instances:")
        instances_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_primary']};")
        self.instances_path_edit = QtWidgets.QLineEdit(paths_group)
        self.instances_path_edit.setPlaceholderText("Select your CurseForge instances directory...")
        self.instances_browse_btn = QtWidgets.QPushButton("📂 Browse", paths_group)
        self.instances_browse_btn.setMaximumWidth(120)
        self.instances_browse_btn.clicked.connect(self._browse_instances_path)

        # Custom Launcher Game path
        game_label = QtWidgets.QLabel("Custom Launcher Game:")
        game_label.setStyleSheet(f"font-weight: 600; color: {COLORS['text_primary']};")
        self.game_path_edit = QtWidgets.QLineEdit(paths_group)
        self.game_path_edit.setPlaceholderText("Select your game directory...")
        self.game_browse_btn = QtWidgets.QPushButton("📂 Browse", paths_group)
        self.game_browse_btn.setMaximumWidth(120)
        self.game_browse_btn.clicked.connect(self._browse_game_path)

        self.save_paths_btn = QtWidgets.QPushButton("💾 Save Paths", paths_group)
        self.save_paths_btn.setMaximumWidth(140)
        self.save_paths_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: #0D1B0E;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #57A75F;
            }}
        """)
        self.save_paths_btn.clicked.connect(self._save_paths)

        paths_layout.addWidget(instances_label, 0, 0)
        paths_layout.addWidget(self.instances_path_edit, 0, 1)
        paths_layout.addWidget(self.instances_browse_btn, 0, 2)
        paths_layout.addWidget(game_label, 1, 0)
        paths_layout.addWidget(self.game_path_edit, 1, 1)
        paths_layout.addWidget(self.game_browse_btn, 1, 2)
        paths_layout.addWidget(self.save_paths_btn, 0, 3, 2, 1)

        paths_layout.setColumnStretch(1, 1)
        main_layout.addWidget(paths_group)

        # Main splitter area
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)

        # Left: modpack list
        left_widget = QtWidgets.QWidget(splitter)
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # Modpack list group
        modpack_group = QtWidgets.QGroupBox("📦 Available Modpacks", left_widget)
        modpack_layout = QtWidgets.QVBoxLayout(modpack_group)
        modpack_layout.setContentsMargins(12, 16, 12, 12)
        modpack_layout.setSpacing(10)

        self.refresh_modpacks_btn = QtWidgets.QPushButton("🔄 Refresh Modpacks", modpack_group)
        self.refresh_modpacks_btn.setObjectName("refreshButton")
        self.refresh_modpacks_btn.clicked.connect(self._refresh_modpacks)
        modpack_layout.addWidget(self.refresh_modpacks_btn)

        self.modpack_list = QtWidgets.QListWidget(modpack_group)
        self.modpack_list.currentRowChanged.connect(self._on_modpack_selected)
        modpack_layout.addWidget(self.modpack_list, stretch=1)

        self.modpack_details_label = QtWidgets.QLabel("", modpack_group)
        self.modpack_details_label.setWordWrap(True)
        self.modpack_details_label.setStyleSheet(f"""
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            padding: 10px;
            font-size: 11px;
            color: {COLORS['text_secondary']};
        """)
        self.modpack_details_label.setMinimumHeight(60)
        modpack_layout.addWidget(self.modpack_details_label)

        left_layout.addWidget(modpack_group)

        # Right: preview and log
        right_widget = QtWidgets.QWidget(splitter)
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        # Preview
        preview_group = QtWidgets.QGroupBox("👁️ Sync Preview", right_widget)
        preview_layout = QtWidgets.QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(12, 16, 12, 12)
        preview_layout.setSpacing(10)

        self.preview_tree = QtWidgets.QTreeWidget(preview_group)
        self.preview_tree.setColumnCount(4)
        self.preview_tree.setHeaderLabels(["Action", "Relative Path", "Size", "Details"])
        self.preview_tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.preview_tree.setAlternatingRowColors(True)
        self.preview_tree.itemSelectionChanged.connect(self._on_preview_selection_changed)
        
        # Set column widths
        self.preview_tree.setColumnWidth(0, 100)
        self.preview_tree.setColumnWidth(1, 300)
        self.preview_tree.setColumnWidth(2, 100)
        
        preview_layout.addWidget(self.preview_tree)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.preview_btn = QtWidgets.QPushButton("🔍 Preview Changes", preview_group)
        self.preview_btn.clicked.connect(self._preview_selected_modpack)
        self.preview_btn.setMinimumHeight(35)

        self.sync_btn = QtWidgets.QPushButton("✨ Sync Now", preview_group)
        self.sync_btn.setObjectName("syncButton")
        self.sync_btn.clicked.connect(self._sync_selected_modpack)
        self.sync_btn.setEnabled(False)
        self.sync_btn.setMinimumHeight(35)

        self.exclude_btn = QtWidgets.QPushButton("🚫 Exclude Selected", preview_group)
        self.exclude_btn.setObjectName("excludeButton")
        self.exclude_btn.clicked.connect(self._exclude_selected)
        self.exclude_btn.setEnabled(False)

        self.backup_checkbox = QtWidgets.QCheckBox("💾 Create backup before syncing", preview_group)
        self.backup_checkbox.setStyleSheet("font-weight: 500;")

        buttons_layout.addWidget(self.preview_btn)
        buttons_layout.addWidget(self.sync_btn)
        buttons_layout.addWidget(self.exclude_btn)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.backup_checkbox)

        preview_layout.addLayout(buttons_layout)
        right_layout.addWidget(preview_group, stretch=3)

        # Log area
        log_group = QtWidgets.QGroupBox("📋 Sync Log", right_widget)
        log_layout = QtWidgets.QVBoxLayout(log_group)
        log_layout.setContentsMargins(12, 16, 12, 12)
        log_layout.setSpacing(10)
        
        self.log_output = QtWidgets.QPlainTextEdit(log_group)
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        
        # Clear log button
        clear_log_btn = QtWidgets.QPushButton("🗑️ Clear Log", log_group)
        clear_log_btn.setMaximumWidth(120)
        clear_log_btn.clicked.connect(lambda: self.log_output.clear())
        log_layout.addWidget(clear_log_btn)
        
        right_layout.addWidget(log_group, stretch=2)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter, stretch=1)

        # Status bar widgets
        self.status_widget = QtWidgets.QWidget()
        status_layout = QtWidgets.QHBoxLayout(self.status_widget)
        status_layout.setContentsMargins(5, 5, 5, 5)
        status_layout.setSpacing(10)
        
        self.progress_bar = QtWidgets.QProgressBar(self.status_widget)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumWidth(300)
        self.progress_bar.setMinimumHeight(20)
        
        self.status_message = QtWidgets.QLabel("✅ Ready", self.status_widget)
        self.status_message.setStyleSheet(f"font-weight: 500; color: {COLORS['success']};")
        
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.status_message)
        status_layout.addStretch()
        
        self.statusBar().addPermanentWidget(self.status_widget, 1)

    # ----------------------------------------------------------------- INIT LOAD
    def _load_initial_state(self) -> None:
        config = self.engine.config
        self.instances_path_edit.setText(str(config.instances_path))
        self.game_path_edit.setText(str(config.game_path))
        self.backup_checkbox.setChecked(bool(config.backup_dir))
        self.append_log("🚀 Application started successfully")
        self._refresh_modpacks()

    # ----------------------------------------------------------------- UTILITIES
    def append_log(self, message: str) -> None:
        """Append a message to the log with timestamp."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_output.appendPlainText(formatted_message)
        self.log_output.ensureCursorVisible()

    def _set_status(self, message: str, is_error: bool = False) -> None:
        """Update the status bar message with appropriate styling."""
        icon = "❌" if is_error else "ℹ️"
        color = COLORS['danger'] if is_error else COLORS['primary']
        self.status_message.setText(f"{icon} {message}")
        self.status_message.setStyleSheet(f"font-weight: 500; color: {color};")

    def _browse_instances_path(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "Select CurseForge Instances Directory",
            str(Path.home())
        )
        if directory:
            self.instances_path_edit.setText(directory)

    def _browse_game_path(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "Select Custom Launcher Game Directory",
            str(Path.home())
        )
        if directory:
            self.game_path_edit.setText(directory)

    def _save_paths(self) -> None:
        # Get and validate input
        instances_text = self.instances_path_edit.text().strip()
        game_text = self.game_path_edit.text().strip()
        
        if not instances_text or not game_text:
            QtWidgets.QMessageBox.warning(
                self,
                "Missing Paths",
                "Please enter both the CurseForge instances path and game path."
            )
            return
        
        try:
            instances_path = Path(instances_text).expanduser().resolve()
            game_path = Path(game_text).expanduser().resolve()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Path",
                f"Invalid path format: {str(e)}"
            )
            return
        
        # Validate paths
        if not instances_path.exists():
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Path",
                f"CurseForge instances path does not exist:\n{instances_path}"
            )
            return
        
        if not game_path.exists():
            response = QtWidgets.QMessageBox.question(
                self,
                "Create Directory",
                f"Game path does not exist. Create it?\n{game_path}",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if response == QtWidgets.QMessageBox.StandardButton.Yes:
                game_path.mkdir(parents=True, exist_ok=True)
            else:
                return
        
        self.engine.update_paths(instances_path, game_path)
        self._set_status("✅ Paths saved successfully")
        self.append_log(f"📁 Updated instances path: {instances_path}")
        self.append_log(f"📁 Updated game path: {game_path}")
        self._refresh_modpacks()

    # ----------------------------------------------------------------- REFRESH MODPACKS
    def _refresh_modpacks(self) -> None:
        """Start background thread to refresh modpack list."""
        # Prevent multiple simultaneous refresh operations
        if self.refresh_worker and self.refresh_worker.isRunning():
            self.append_log("⚠️ Refresh already in progress")
            return
        
        self.modpack_list.clear()
        self.append_log("🔄 Refreshing modpack list...")
        self._set_status("🔄 Scanning for modpacks...")
        
        # Disable buttons during refresh
        self.refresh_modpacks_btn.setEnabled(False)
        self.preview_btn.setEnabled(False)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        
        # Create and start worker thread
        self.refresh_worker = RefreshModpacksWorker(self.engine, self)
        self.refresh_worker.finished.connect(self._on_refresh_finished)
        self.refresh_worker.error.connect(self._on_refresh_error)
        self.refresh_worker.start()

    def _on_refresh_finished(self, modpacks: list[ModpackInfo]) -> None:
        """Handle completion of modpack refresh."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.refresh_modpacks_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        self.modpacks = modpacks
        
        for modpack in self.modpacks:
            item = QtWidgets.QListWidgetItem(f"📦 {modpack.name}")
            self.modpack_list.addItem(item)

        if self.modpacks:
            self.modpack_list.setCurrentRow(0)
            self.append_log(f"✅ Found {len(self.modpacks)} modpack(s)")
            self._set_status(f"✅ Found {len(self.modpacks)} modpack(s)")
        else:
            self.modpack_details_label.setText("ℹ️ No modpacks detected. Check your CurseForge instances path.")
            self.preview_tree.clear()
            self.sync_btn.setEnabled(False)
            self.exclude_btn.setEnabled(False)
            self.append_log("⚠️ No modpacks found in the specified directory")
            self._set_status("⚠️ No modpacks found", is_error=True)

    def _on_refresh_error(self, error_msg: str) -> None:
        """Handle error during modpack refresh."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.refresh_modpacks_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        
        self.append_log(f"❌ Refresh failed: {error_msg}")
        self._set_status("Refresh failed", is_error=True)
        QtWidgets.QMessageBox.critical(
            self,
            "Refresh Error",
            f"Failed to refresh modpacks:\n{error_msg}"
        )

    def _on_modpack_selected(self, index: int) -> None:
        if index < 0 or index >= len(self.modpacks):
            self.selected_modpack = None
            self.modpack_details_label.clear()
            self.sync_btn.setEnabled(False)
            self.exclude_btn.setEnabled(False)
            return

        self.selected_modpack = self.modpacks[index]
        info_lines = [
            f"<b>Modpack:</b> {self.selected_modpack.name}",
            f"<b>Path:</b> {self.selected_modpack.path}"
        ]
        if self.selected_modpack.manifest_path:
            info_lines.append(f"<b>Manifest:</b> {self.selected_modpack.manifest_path.name}")
        
        self.modpack_details_label.setText("<br>".join(info_lines))
        self.preview_tree.clear()
        self.current_plan = None
        self.current_snapshot_payload = None
        self.sync_btn.setEnabled(False)
        self.exclude_btn.setEnabled(False)
        self.append_log(f"📦 Selected modpack: {self.selected_modpack.name}")

    # ----------------------------------------------------------------- PREVIEW
    def _preview_selected_modpack(self) -> None:
        """Start background thread to build sync plan."""
        if not self.selected_modpack:
            QtWidgets.QMessageBox.warning(
                self,
                "No Selection",
                "Please select a modpack first."
            )
            return
        
        # Prevent multiple simultaneous preview operations
        if self.preview_worker and self.preview_worker.isRunning():
            self.append_log("⚠️ Preview already in progress")
            return

        self._set_status("🔍 Building sync plan...")
        self.append_log(f"🔍 Analyzing changes for {self.selected_modpack.name}...")
        
        # Disable buttons during preview
        self.preview_btn.setEnabled(False)
        self.sync_btn.setEnabled(False)
        self.exclude_btn.setEnabled(False)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        
        # Create and start worker thread
        self.preview_worker = PreviewWorker(self.engine, self.selected_modpack, self)
        self.preview_worker.finished.connect(self._on_preview_finished)
        self.preview_worker.error.connect(self._on_preview_error)
        self.preview_worker.start()

    def _on_preview_finished(self, plan: SyncPlan, snapshot_payload: dict) -> None:
        """Handle completion of sync plan building."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.preview_btn.setEnabled(True)
        
        self.current_plan = plan
        self.current_snapshot_payload = snapshot_payload
        self._populate_preview(plan)
        self.sync_btn.setEnabled(True and not plan.is_empty())
        self.exclude_btn.setEnabled(False)
        
        if plan.is_empty():
            self._set_status("✅ Everything is already in sync")
            self.append_log("✅ No changes needed - everything is up to date")
            QtWidgets.QMessageBox.information(
                self,
                "Sync Status",
                "Everything is already in sync! No changes needed."
            )
        else:
            total_changes = len(plan.adds) + len(plan.updates) + len(plan.removals)
            self._set_status(f"✅ Preview ready - {total_changes} change(s) detected")
            self.append_log(f"📊 Found {len(plan.adds)} additions, {len(plan.updates)} updates, {len(plan.removals)} removals")

    def _on_preview_error(self, error_msg: str) -> None:
        """Handle error during sync plan building."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.preview_btn.setEnabled(True)
        
        self._set_status(f"Error building sync plan", is_error=True)
        self.append_log(f"❌ Error: {error_msg}")
        QtWidgets.QMessageBox.critical(
            self,
            "Error",
            f"Failed to build sync plan:\n{error_msg}"
        )

    def _populate_preview(self, plan: SyncPlan) -> None:
        self.preview_tree.clear()

        def add_items(category: str, changes: list[FileChange], color: QtGui.QColor, icon: str) -> None:
            for change in changes:
                item = QtWidgets.QTreeWidgetItem(self.preview_tree)
                item.setText(0, f"{icon} {category}")
                item.setText(1, change.relative_path.as_posix())
                if change.size_bytes is not None:
                    item.setText(2, self._format_size(change.size_bytes))
                item.setText(3, change.reason or "")
                item.setData(0, QtCore.Qt.ItemDataRole.UserRole, change)
                
                # Apply color to all columns
                for column in range(4):
                    item.setForeground(column, QtGui.QBrush(color))
                    # Make action column bold
                    if column == 0:
                        font = item.font(column)
                        font.setBold(True)
                        item.setFont(column, font)

        # Add items with appropriate colors and icons
        add_items("Add", plan.adds, QtGui.QColor(COLORS['success']), "➕")
        add_items("Update", plan.updates, QtGui.QColor(COLORS['warning']), "🔄")
        add_items("Remove", plan.removals, QtGui.QColor(COLORS['danger']), "🗑️")
        add_items("Skip", plan.skipped, QtGui.QColor(COLORS['text_secondary']), "⏭️")

        self.preview_tree.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        
        # Expand all items for better visibility
        self.preview_tree.expandAll()

    def _on_preview_selection_changed(self) -> None:
        has_selection = bool(self.preview_tree.selectedItems())
        self.exclude_btn.setEnabled(has_selection and self.current_plan is not None)

    @staticmethod
    def _format_size(size: int) -> str:
        """Format file size in a human-readable format."""
        if size < 1024:
            return f"{size} B"
        for unit in ["KB", "MB", "GB"]:
            size /= 1024
            if size < 1024:
                return f"{size:.2f} {unit}"
        return f"{size:.2f} TB"

    def _exclude_selected(self) -> None:
        selected_items = self.preview_tree.selectedItems()
        if not selected_items or not self.selected_modpack:
            return

        item = selected_items[0]
        change: FileChange = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if not change:
            return

        response = QtWidgets.QMessageBox.question(
            self,
            "Exclude File",
            f"Exclude this file from future syncs?\n\n{change.relative_path}\n\n"
            "This file will be ignored in all future sync operations.",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        
        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            self.engine.add_exclusion(self.selected_modpack.name, change.relative_path.as_posix())
            self.append_log(f"🚫 Excluded: {change.relative_path}")
            self._preview_selected_modpack()

    # ----------------------------------------------------------------- SYNC
    def _sync_selected_modpack(self) -> None:
        """Start background thread to execute sync plan."""
        if not self.selected_modpack or not self.current_plan or not self.current_snapshot_payload:
            return

        if self.current_plan.is_empty():
            QtWidgets.QMessageBox.information(
                self, 
                "Sync Status", 
                "Everything is already in sync."
            )
            return
        
        # Prevent multiple simultaneous sync operations
        if self.sync_worker and self.sync_worker.isRunning():
            self.append_log("⚠️ Sync already in progress")
            return

        total_changes = len(self.current_plan.adds) + len(self.current_plan.updates) + len(self.current_plan.removals)
        summary = (
            f"<b>Add:</b> {len(self.current_plan.adds)} file(s)<br>"
            f"<b>Update:</b> {len(self.current_plan.updates)} file(s)<br>"
            f"<b>Remove:</b> {len(self.current_plan.removals)} file(s)"
        )
        
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Sync",
            f"<b>Proceed with syncing {self.selected_modpack.name}?</b><br><br>{summary}",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            self.append_log("⏸️ Sync cancelled by user")
            return

        self.append_log(f"▶️ Starting sync for {self.selected_modpack.name}...")
        self.progress_bar.setMaximum(max(total_changes, 1))
        self.progress_bar.setValue(0)
        self._set_status("🔄 Sync in progress...")
        
        # Disable buttons during sync
        self.preview_btn.setEnabled(False)
        self.sync_btn.setEnabled(False)
        self.exclude_btn.setEnabled(False)
        self.refresh_modpacks_btn.setEnabled(False)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)

        # Create and start worker thread
        self.sync_worker = SyncWorker(
            self.engine,
            self.selected_modpack,
            self.current_plan,
            self.current_snapshot_payload,
            self.backup_checkbox.isChecked(),
            self
        )
        self.sync_worker.finished.connect(self._on_sync_finished)
        self.sync_worker.error.connect(self._on_sync_error)
        self.sync_worker.progress.connect(self._on_sync_progress)
        self.sync_worker.confirm_update_signal.connect(self._handle_confirm_update)
        self.sync_worker.confirm_removal_signal.connect(self._handle_confirm_removal)
        self.sync_worker.start()

    def _on_sync_progress(self, message: str, current: int, total: int) -> None:
        """Handle progress updates from sync worker."""
        self.progress_bar.setMaximum(max(total, 1))
        self.progress_bar.setValue(current)
        self._set_status(f"🔄 {message}")

    def _handle_confirm_update(self, change: FileChange) -> None:
        """Handle confirmation request from sync worker for file update."""
        result = QtWidgets.QMessageBox.question(
            self,
            "Confirm Update",
            f"Replace existing file?\n\n<b>{change.relative_path}</b>",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        response = (result == QtWidgets.QMessageBox.StandardButton.Yes)
        self.sync_worker.set_confirmation_response(change, response)

    def _handle_confirm_removal(self, change: FileChange) -> None:
        """Handle confirmation request from sync worker for file removal."""
        result = QtWidgets.QMessageBox.question(
            self,
            "Confirm Removal",
            f"Delete file removed from modpack?\n\n<b>{change.relative_path}</b>",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        response = (result == QtWidgets.QMessageBox.StandardButton.Yes)
        self.sync_worker.set_confirmation_response(change, response)

    def _on_sync_finished(self) -> None:
        """Handle completion of sync operation."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.preview_btn.setEnabled(True)
        self.refresh_modpacks_btn.setEnabled(True)
        
        self._set_status("✅ Sync completed successfully")
        self.append_log(f"✅ Sync completed for {self.selected_modpack.name}")
        self.progress_bar.setValue(self.progress_bar.maximum())
        
        QtWidgets.QMessageBox.information(
            self, 
            "Sync Complete", 
            f"<b>Synchronization complete!</b><br><br>"
            f"Your modpack has been successfully synced."
        )
        
        # Refresh the preview to show updated state
        self._preview_selected_modpack()

    def _on_sync_error(self, error_msg: str) -> None:
        """Handle error during sync operation."""
        QtWidgets.QApplication.restoreOverrideCursor()
        self.preview_btn.setEnabled(True)
        self.refresh_modpacks_btn.setEnabled(True)
        
        self._set_status("Sync failed", is_error=True)
        self.append_log(f"❌ Sync failed: {error_msg}")
        QtWidgets.QMessageBox.critical(
            self, 
            "Sync Failed", 
            f"<b>Synchronization failed:</b><br><br>{error_msg}"
        )


def create_main_window() -> MainWindow:
    """Factory function to create the main window."""
    return MainWindow()
