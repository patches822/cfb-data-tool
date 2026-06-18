# SPDX-License-Identifier: GPL-3.0-or-later
"""Application entry point."""

from __future__ import annotations

import logging
import sys


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    from PySide6.QtWidgets import QApplication

    from .ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("CFB Data Tool")
    app.setOrganizationName("cfb-data-tool")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
