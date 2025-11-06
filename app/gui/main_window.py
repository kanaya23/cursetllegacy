"""Main window for the Minecraft modpack sync application."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets

from ..core.config import ConfigManager
from ..core.models import FileChange, ModpackInfo, SyncPlan
from ..core.syncer import SyncEngine


class MainWindow(QtWidgets.QMainWindow):
    """Primary application window."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Minecraft Modpack Sync")
        self.resize(1200, 720)

        self.config_manager = ConfigManager()
        self.engine = SyncEngine(config_manager=self.config_manager, log_callback=self.append_log)

        self.modpacks: list[ModpackInfo] = []
        self.selected_modpack: Optional[ModpackInfo] = None
        self.current_plan: Optional[SyncPlan] = None
        self.current_snapshot_payload: Optional[dict] = None

        self._setup_ui()
        self._load_initial_state()

    # ------------------------------------------------------------------ UI SETUP
    def _setup_ui(self) -> None:
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Paths configuration area
        paths_group = QtWidgets.QGroupBox("Directories", parent=central_widget)
        paths_layout = QtWidgets.QGridLayout(paths_group)

        self.instances_path_edit = QtWidgets.QLineEdit(paths_group)
        self.instances_browse_btn = QtWidgets.QPushButton("Browse…", paths_group)
        self.instances_browse_btn.clicked.connect(self._browse_instances_path)

        self.game_path_edit = QtWidgets.QLineEdit(paths_group)
        self.game_browse_btn = QtWidgets.QPushButton("Browse…", paths_group)
        self.game_browse_btn.clicked.connect(self._browse_game_path)

        self.save_paths_btn = QtWidgets.QPushButton("Save Paths", paths_group)
        self.save_paths_btn.clicked.connect(self._save_paths)

        paths_layout.addWidget(QtWidgets.QLabel("CurseForge Instances:"), 0, 0)
        paths_layout.addWidget(self.instances_path_edit, 0, 1)
        paths_layout.addWidget(self.instances_browse_btn, 0, 2)
        paths_layout.addWidget(QtWidgets.QLabel("Custom Launcher Game:"), 1, 0)
        paths_layout.addWidget(self.game_path_edit, 1, 1)
        paths_layout.addWidget(self.game_browse_btn, 1, 2)
        paths_layout.addWidget(self.save_paths_btn, 0, 3, 2, 1)

        main_layout.addWidget(paths_group)

        # Main splitter area
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Left: modpack list
        left_widget = QtWidgets.QWidget(splitter)
        left_layout = QtWidgets.QVBoxLayout(left_widget)

        self.refresh_modpacks_btn = QtWidgets.QPushButton("Refresh Modpacks", left_widget)
        self.refresh_modpacks_btn.clicked.connect(self._refresh_modpacks)
        left_layout.addWidget(self.refresh_modpacks_btn)

        self.modpack_list = QtWidgets.QListWidget(left_widget)
        self.modpack_list.currentRowChanged.connect(self._on_modpack_selected)
        left_layout.addWidget(self.modpack_list, stretch=1)

        self.modpack_details_label = QtWidgets.QLabel("", left_widget)
        self.modpack_details_label.setWordWrap(True)
        left_layout.addWidget(self.modpack_details_label)

        # Right: preview and log
        right_widget = QtWidgets.QWidget(splitter)
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        # Preview
        preview_group = QtWidgets.QGroupBox("Sync Preview", right_widget)
        preview_layout = QtWidgets.QVBoxLayout(preview_group)

        self.preview_tree = QtWidgets.QTreeWidget(preview_group)
        self.preview_tree.setColumnCount(4)
        self.preview_tree.setHeaderLabels(["Action", "Relative Path", "Size", "Details"])
        self.preview_tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.preview_tree.itemSelectionChanged.connect(self._on_preview_selection_changed)
        preview_layout.addWidget(self.preview_tree)

        buttons_layout = QtWidgets.QHBoxLayout()
        self.preview_btn = QtWidgets.QPushButton("Preview", preview_group)
        self.preview_btn.clicked.connect(self._preview_selected_modpack)

        self.sync_btn = QtWidgets.QPushButton("Sync", preview_group)
        self.sync_btn.clicked.connect(self._sync_selected_modpack)
        self.sync_btn.setEnabled(False)

        self.exclude_btn = QtWidgets.QPushButton("Exclude Selected", preview_group)
        self.exclude_btn.clicked.connect(self._exclude_selected)
        self.exclude_btn.setEnabled(False)

        self.backup_checkbox = QtWidgets.QCheckBox("Create backup before syncing", preview_group)

        buttons_layout.addWidget(self.preview_btn)
        buttons_layout.addWidget(self.sync_btn)
        buttons_layout.addWidget(self.exclude_btn)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.backup_checkbox)

        preview_layout.addLayout(buttons_layout)
        right_layout.addWidget(preview_group, stretch=3)

        # Log area
        log_group = QtWidgets.QGroupBox("Sync Log", right_widget)
        log_layout = QtWidgets.QVBoxLayout(log_group)
        self.log_output = QtWidgets.QPlainTextEdit(log_group)
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        right_layout.addWidget(log_group, stretch=2)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        main_layout.addWidget(splitter, stretch=1)

        # Status bar widgets
        self.status_widget = QtWidgets.QWidget()
        status_layout = QtWidgets.QHBoxLayout(self.status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QtWidgets.QProgressBar(self.status_widget)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(0)
        status_layout.addWidget(self.progress_bar)
        self.status_message = QtWidgets.QLabel("Ready", self.status_widget)
        status_layout.addWidget(self.status_message)
        self.statusBar().addPermanentWidget(self.status_widget, 1)

    # ----------------------------------------------------------------- INIT LOAD
    def _load_initial_state(self) -> None:
        config = self.engine.config
        self.instances_path_edit.setText(str(config.instances_path))
        self.game_path_edit.setText(str(config.game_path))
        self.backup_checkbox.setChecked(bool(config.backup_dir))
        self._refresh_modpacks()

    # ----------------------------------------------------------------- UTILITIES
    def append_log(self, message: str) -> None:
        self.log_output.appendPlainText(message)
        self.log_output.ensureCursorVisible()

    def _set_status(self, message: str) -> None:
        self.status_message.setText(message)

    def _browse_instances_path(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select CurseForge Instances Directory")
        if directory:
            self.instances_path_edit.setText(directory)

    def _browse_game_path(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Custom Launcher Game Directory")
        if directory:
            self.game_path_edit.setText(directory)

    def _save_paths(self) -> None:
        instances_path = Path(self.instances_path_edit.text()).expanduser()
        game_path = Path(self.game_path_edit.text()).expanduser()
        self.engine.update_paths(instances_path, game_path)
        self._set_status("Paths saved")
        self._refresh_modpacks()

    def _refresh_modpacks(self) -> None:
        self.modpack_list.clear()
        self.modpacks = self.engine.list_modpacks()
        for modpack in self.modpacks:
            item = QtWidgets.QListWidgetItem(modpack.name)
            self.modpack_list.addItem(item)

        if self.modpacks:
            self.modpack_list.setCurrentRow(0)
        else:
            self.modpack_details_label.setText("No modpacks detected.")
            self.preview_tree.clear()
            self.sync_btn.setEnabled(False)
            self.exclude_btn.setEnabled(False)

    def _on_modpack_selected(self, index: int) -> None:
        if index < 0 or index >= len(self.modpacks):
            self.selected_modpack = None
            self.modpack_details_label.clear()
            self.sync_btn.setEnabled(False)
            self.exclude_btn.setEnabled(False)
            return

        self.selected_modpack = self.modpacks[index]
        info_lines = [f"Path: {self.selected_modpack.path}"]
        if self.selected_modpack.manifest_path:
            info_lines.append(f"Manifest: {self.selected_modpack.manifest_path}")
        self.modpack_details_label.setText("\n".join(info_lines))
        self.preview_tree.clear()
        self.current_plan = None
        self.current_snapshot_payload = None
        self.sync_btn.setEnabled(False)
        self.exclude_btn.setEnabled(False)

    def _preview_selected_modpack(self) -> None:
        if not self.selected_modpack:
            return

        self._set_status("Building sync plan…")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        try:
            plan, snapshot_payload, *_ = self.engine.create_sync_plan(self.selected_modpack)
            self.current_plan = plan
            self.current_snapshot_payload = snapshot_payload
            self._populate_preview(plan)
            self.sync_btn.setEnabled(True and not plan.is_empty())
            self.exclude_btn.setEnabled(False)
            if plan.is_empty():
                self._set_status("Everything is already in sync.")
            else:
                self._set_status("Preview ready. Review changes before syncing.")
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def _populate_preview(self, plan: SyncPlan) -> None:
        self.preview_tree.clear()

        def add_items(category: str, changes: list[FileChange], color: QtGui.QColor) -> None:
            for change in changes:
                item = QtWidgets.QTreeWidgetItem(self.preview_tree)
                item.setText(0, category)
                item.setText(1, change.relative_path.as_posix())
                if change.size_bytes is not None:
                    item.setText(2, self._format_size(change.size_bytes))
                item.setText(3, change.reason or "")
                item.setData(0, QtCore.Qt.ItemDataRole.UserRole, change)
                for column in range(4):
                    item.setForeground(column, QtGui.QBrush(color))

        add_items("Add", plan.adds, QtGui.QColor("#2E7D32"))
        add_items("Update", plan.updates, QtGui.QColor("#F9A825"))
        add_items("Remove", plan.removals, QtGui.QColor("#C62828"))
        add_items("Skip", plan.skipped, QtGui.QColor("#546E7A"))

        self.preview_tree.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

    def _on_preview_selection_changed(self) -> None:
        has_selection = bool(self.preview_tree.selectedItems())
        self.exclude_btn.setEnabled(has_selection)

    @staticmethod
    def _format_size(size: int) -> str:
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
            f"Exclude {change.relative_path} from future syncs?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        if response == QtWidgets.QMessageBox.StandardButton.Yes:
            self.engine.add_exclusion(self.selected_modpack.name, change.relative_path.as_posix())
            self.append_log(f"Excluded {change.relative_path}")
            self._preview_selected_modpack()

    def _sync_selected_modpack(self) -> None:
        if not self.selected_modpack or not self.current_plan or not self.current_snapshot_payload:
            return

        if self.current_plan.is_empty():
            QtWidgets.QMessageBox.information(self, "Sync", "Everything is already in sync.")
            return

        total_changes = len(self.current_plan.adds) + len(self.current_plan.updates) + len(self.current_plan.removals)
        summary = (
            f"Add: {len(self.current_plan.adds)}\n"
            f"Update: {len(self.current_plan.updates)}\n"
            f"Remove: {len(self.current_plan.removals)}"
        )
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Sync",
            f"Proceed with syncing {self.selected_modpack.name}?\n\n{summary}",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        if confirm != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        self.progress_bar.setMaximum(max(total_changes, 1))
        self.progress_bar.setValue(0)
        self._set_status("Sync in progress…")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)

        def progress_handler(message: str, current: int, total: int) -> None:
            self.progress_bar.setMaximum(max(total, 1))
            self.progress_bar.setValue(current)
            self._set_status(message)
            QtWidgets.QApplication.processEvents()

        def confirm_update(change: FileChange) -> bool:
            result = QtWidgets.QMessageBox.question(
                self,
                "Confirm Update",
                f"Replace existing file?\n\n{change.relative_path}",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            )
            return result == QtWidgets.QMessageBox.StandardButton.Yes

        def confirm_removal(change: FileChange) -> bool:
            result = QtWidgets.QMessageBox.question(
                self,
                "Confirm Removal",
                f"Delete file removed from modpack?\n\n{change.relative_path}",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            )
            return result == QtWidgets.QMessageBox.StandardButton.Yes

        try:
            self.engine.execute_plan(
                modpack=self.selected_modpack,
                plan=self.current_plan,
                snapshot_payload=self.current_snapshot_payload,
                create_backups=self.backup_checkbox.isChecked(),
                confirm_update=confirm_update,
                confirm_removal=confirm_removal,
                progress_callback=progress_handler,
            )
            self._set_status("Sync completed")
            self.progress_bar.setValue(self.progress_bar.maximum())
            QtWidgets.QMessageBox.information(self, "Sync", "Synchronization complete.")
        except Exception as exc:  # pragma: no cover - GUI side effect
            QtWidgets.QMessageBox.critical(self, "Sync Failed", str(exc))
            self._set_status("Sync failed")
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
            self._preview_selected_modpack()


def create_main_window() -> MainWindow:
    return MainWindow()
