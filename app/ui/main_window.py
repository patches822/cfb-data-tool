# SPDX-License-Identifier: GPL-3.0-or-later
"""Main window: tabbed shell. Capture + Settings are live in Phase 2;
Calibrate (Phase 3) and Data (Phase 4) are placeholders."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QTabWidget, QWidget, QVBoxLayout

from ..config.settings_store import Settings
from .calibration_tab import CalibrationTab
from .capture_tab import CaptureTab
from .settings_tab import SettingsTab


def _placeholder(text: str) -> QWidget:
    w = QWidget()
    layout = QVBoxLayout(w)
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color:#888; font-size:14px;")
    layout.addWidget(label)
    return w


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings | None = None):
        super().__init__()
        self.settings = settings or Settings.load()
        self.setWindowTitle("CFB Data Tool")
        self.resize(1100, 680)

        tabs = QTabWidget()
        self.capture_tab = CaptureTab(self.settings)
        self.calibration_tab = CalibrationTab(self.settings)
        tabs.addTab(self.capture_tab, "Capture")
        tabs.addTab(self.calibration_tab, "Calibrate")
        tabs.addTab(_placeholder("Recruit table, filtering & export — Phase 4"), "Data")
        tabs.addTab(SettingsTab(self.settings), "Settings")
        self.setCentralWidget(tabs)

        # Auto-commit calibration edits when leaving the Calibrate tab, so the
        # Capture tab always reflects them without a manual Save.
        self._tabs = tabs
        self._calib_index = tabs.indexOf(self.calibration_tab)
        self._prev_index = tabs.currentIndex()
        tabs.currentChanged.connect(self._on_tab_changed)

        # Share the OCR engine with the calibration tab's "Test OCR" once ready,
        # and refresh capture's ROIs live when a calibration is saved.
        self.capture_tab.engine_ready.connect(
            lambda engine: self.calibration_tab.set_ocr(engine.ocr))
        if self.capture_tab.engine is not None:
            self.calibration_tab.set_ocr(self.capture_tab.engine.ocr)
        self.calibration_tab.saved.connect(self.capture_tab.reload_calibration)

    def _on_tab_changed(self, index):
        if self._prev_index == self._calib_index:
            self.calibration_tab.commit_if_dirty()
        self._prev_index = index

    def closeEvent(self, event):
        self.calibration_tab.commit_if_dirty()
        self.capture_tab.shutdown()
        super().closeEvent(event)
