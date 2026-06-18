# SPDX-License-Identifier: GPL-3.0-or-later
"""Result card: shows a ScanResult's fields, confidence, and validity.

Confidence colouring lays the groundwork for Phase 5 (inline correction of
low-confidence fields). For now it's read-only display.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QWidget,
)

from ...core.profiles.recruits import BASIC_INFO_HEADERS

# Fields produced by computer vision (not OCR) have no confidence score.
_CV_FIELDS = {"STARS", "GEM"}


def _conf_color(conf: float, threshold: float) -> str:
    if conf is None:
        return "#888888"
    if conf >= 0.90:
        return "#2e7d32"  # green
    if conf >= threshold:
        return "#f9a825"  # amber
    return "#c62828"      # red


class ResultCard(QWidget):
    def __init__(self, confidence_threshold: float = 0.80, parent=None):
        super().__init__(parent)
        self.threshold = confidence_threshold

        root = QVBoxLayout(self)

        self.status = QLabel("No scan yet")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("font-weight: bold; padding: 6px; border-radius: 4px;")
        root.addWidget(self.status)

        # Basic fields
        basics_box = QGroupBox("Recruit")
        self._basics = QGridLayout(basics_box)
        self._basics.setColumnStretch(1, 1)
        root.addWidget(basics_box)

        # Attributes
        attrs_box = QGroupBox("Attributes")
        self._attrs = QGridLayout(attrs_box)
        root.addWidget(attrs_box)

        root.addStretch(1)
        self._value_labels: dict[str, QLabel] = {}

    def _clear(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def show_result(self, result):
        rec = result.record
        conf = rec.get("_confidence", {})

        # Status banner
        if result.valid:
            self.status.setText("✔ VALID")
            self.status.setStyleSheet(
                "font-weight: bold; padding: 6px; border-radius: 4px;"
                "background:#2e7d32; color:white;")
        else:
            self.status.setText("✘ INVALID — " + ", ".join(result.missing))
            self.status.setStyleSheet(
                "font-weight: bold; padding: 6px; border-radius: 4px;"
                "background:#c62828; color:white;")

        # Basic fields
        self._clear(self._basics)
        for row, key in enumerate(BASIC_INFO_HEADERS):
            name = QLabel(key.title())
            name.setStyleSheet("color:#555;")
            value = QLabel(str(rec.get(key, "")))
            value.setTextInteractionFlags(Qt.TextSelectableByMouse)
            c = None if key in _CV_FIELDS else conf.get(key)
            value.setStyleSheet(f"color:{_conf_color(c, self.threshold)}; font-weight:600;")
            self._basics.addWidget(name, row, 0)
            self._basics.addWidget(value, row, 1)

        # Attributes (2 columns)
        self._clear(self._attrs)
        attrs = rec.get("attributes", {})
        items = list(attrs.items())
        half = (len(items) + 1) // 2
        for i, (k, v) in enumerate(items):
            col = 0 if i < half else 2
            row = i if i < half else i - half
            self._attrs.addWidget(QLabel(k.title()), row, col)
            val = QLabel(str(v))
            val.setStyleSheet("font-weight:600;")
            self._attrs.addWidget(val, row, col + 1)
