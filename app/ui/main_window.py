# SPDX-License-Identifier: GPL-3.0-or-later
"""Main window: tabbed shell. Capture + Settings are live in Phase 2;
Calibrate (Phase 3) and Data (Phase 4) are placeholders."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QTabWidget, QWidget, QVBoxLayout

from ..config.settings_store import Settings
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
        tabs.addTab(self.capture_tab, "Capture")
        tabs.addTab(_placeholder("Visual ROI editor & auto-calibration — Phase 3"), "Calibrate")
        tabs.addTab(_placeholder("Recruit table, filtering & export — Phase 4"), "Data")
        tabs.addTab(SettingsTab(self.settings), "Settings")
        self.setCentralWidget(tabs)

    def closeEvent(self, event):
        self.capture_tab.shutdown()
        super().closeEvent(event)
