# SPDX-License-Identifier: GPL-3.0-or-later
"""Pytest wrapper around the standalone smoke tests.

Run with:  pytest tests/test_smoke.py -v
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
SMOKE_SCRIPTS = sorted(TESTS_DIR.glob("smoke_*.py"))
FIXTURES_DIR = TESTS_DIR / "fixtures" / "screenshots"
NEEDS_FIXTURES = {"smoke_ui", "smoke_calibration"}


@pytest.mark.parametrize(
    "script",
    SMOKE_SCRIPTS,
    ids=[s.stem for s in SMOKE_SCRIPTS],
)
def test_smoke(script: Path):
    if script.stem in NEEDS_FIXTURES and not any(FIXTURES_DIR.rglob("*.png")):
        pytest.skip("fixture screenshots not available (gitignored)")

    env = {**os.environ, "QT_QPA_PLATFORM": "offscreen"}
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(TESTS_DIR.parent),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        pytest.fail(f"{script.name} failed (exit {result.returncode}):\n{result.stdout}\n{result.stderr}")
