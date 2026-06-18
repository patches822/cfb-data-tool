# SPDX-License-Identifier: GPL-3.0-or-later
"""Screen capture via mss.

Returns BGR numpy arrays (OpenCV convention) so frames flow straight into the
engine and CV helpers. Capture objects are created per-call because mss
instances are not safe to share across threads.
"""

from __future__ import annotations

import cv2
import mss
import numpy as np


def grab_region(region: dict) -> np.ndarray:
    """Grab an absolute screen region. ``region`` = {top, left, width, height}."""
    with mss.mss() as sct:
        shot = sct.grab(region)
        return cv2.cvtColor(np.array(shot), cv2.COLOR_BGRA2BGR)


def list_monitors() -> list[dict]:
    """Return per-monitor geometry. Index 0 is the virtual 'all monitors' bounds;
    real monitors start at index 1 (matching mss)."""
    with mss.mss() as sct:
        return [dict(m) for m in sct.monitors]


def monitor_region(monitor_number: int) -> dict:
    """Full-screen region for a given monitor number (1-based, as in mss)."""
    with mss.mss() as sct:
        monitors = sct.monitors
        idx = monitor_number if 0 <= monitor_number < len(monitors) else 1
        m = monitors[idx]
        return {"top": m["top"], "left": m["left"], "width": m["width"], "height": m["height"]}


def offsets_for_monitor(global_offsets: dict, monitor_number: int) -> dict:
    """Translate preset global_offsets (relative to a monitor's top-left) into an
    absolute capture region on that monitor."""
    with mss.mss() as sct:
        monitors = sct.monitors
        idx = monitor_number if 0 <= monitor_number < len(monitors) else 1
        m = monitors[idx]
        return {
            "top": m["top"] + global_offsets["top"],
            "left": m["left"] + global_offsets["left"],
            "width": global_offsets["width"],
            "height": global_offsets["height"],
        }
