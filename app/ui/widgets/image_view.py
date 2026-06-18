# SPDX-License-Identifier: GPL-3.0-or-later
"""Helpers to display BGR numpy frames in Qt."""

from __future__ import annotations

import numpy as np
from PySide6.QtGui import QImage, QPixmap


def bgr_to_qpixmap(frame: np.ndarray) -> QPixmap:
    """Convert a BGR (OpenCV) ndarray to a QPixmap."""
    rgb = np.ascontiguousarray(frame[:, :, ::-1])  # BGR -> RGB
    h, w = rgb.shape[:2]
    image = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
    # copy() so the QImage owns its buffer (the numpy array may be freed).
    return QPixmap.fromImage(image.copy())
