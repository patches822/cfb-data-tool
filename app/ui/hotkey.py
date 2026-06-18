# SPDX-License-Identifier: GPL-3.0-or-later
"""Global hotkey bridged to a Qt signal.

The ``keyboard`` callback fires on its own thread; emitting a Qt signal from
there is delivered to the main thread via a queued connection. Global hooks can
require elevated privileges on some setups, so failures are swallowed — the
on-screen Scan button is always the reliable fallback.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class HotkeyManager(QObject):
    triggered = Signal()

    def __init__(self, key: str = "s", parent=None):
        super().__init__(parent)
        self._key = key
        self._handle = None

    def start(self) -> bool:
        try:
            import keyboard
            self._handle = keyboard.add_hotkey(self._key, self.triggered.emit)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning("Global hotkey '%s' unavailable: %s", self._key, exc)
            self._handle = None
            return False

    def stop(self):
        if self._handle is None:
            return
        try:
            import keyboard
            keyboard.remove_hotkey(self._handle)
        except Exception:  # noqa: BLE001
            pass
        self._handle = None
