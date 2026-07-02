# Changelog

All notable changes to CFB Data Tool are documented here.

## [0.2.0] — 2026-07-02

### Added

- **Multi-game-version support with in-app switcher** — recruit profiles, ROI presets, and the SQLite store are now versioned per game (CFB 26 / CFB 27), selected via a persistent "Game version" dropdown above the tabs (replacing the buried Settings-tab option). Switching rebuilds the store, reloads the Capture tab's engine/profile, and refreshes the Data tab; if recruits are sitting in the review queue it confirms first, since their ability/mental dropdowns would otherwise silently start reflecting the new game.
- **CFB 27 preset** (`app/config/presets/cfb27/`) as the second supported game version.
- **Linux desktop support (Wayland-first)** — new `app/platform/` layer with pluggable capture, hotkey, and sound backends. Wayland live capture uses xdg-desktop-portal monitor screencast (PipeWire) with client-side ROI cropping; Windows and macOS continue using `mss`.
- **Linux AppImage packaging** — `packaging/build_linux.sh` produces a portable AppImage with Qt Wayland/XCB platform plugins bundled.
- **Linux sound playback** — `paplay`/`aplay` with freedesktop sound theme discovery and bundled fallback `.wav` files.
- **CI and release** — `ubuntu-latest` smoke tests; Linux AppImage attached to GitHub Releases alongside Windows and macOS artifacts.
- **External-tool CSV export format** — "Export CSV" now writes a fixed column set for a downstream external tool instead of the app's internal schema: renamed/computed fields (`player_name`, `scouting_status`, `is_athlete`), a resolved real position for ATH cards via a per-game-version archetype whitelist, separate abilities/mentals columns, and abbreviated attribute codes. Adds two newly captured fields, `national_rank` (both versions) and `nil_value` (CFB 27 only).
- **Per-game-version star rating template** — star count detection now uses the correct template image for the active game version.

### Fixed

- **Position names aligned to CFB 26** — updated throughout (`POSITION_ATTRIBUTE_COUNT`, `abilities.json`, and the `POSITIONS` constant) to match what the game shows on recruit cards: OT → LT/RT, OG → LG/RG, DE → LEDG/REDG, OLB → WILL/SAM, MLB → MIKE.
- **Platform icon generation** now runs during the build process, with a corrected ICO saving method.
- **Portal D-Bus stream parsing** hardened against compositor variants (Linux Wayland capture).
- **Calibrate tab** now reloads its ROI list on a game-version switch instead of showing stale ROIs from the previous version.
- **Result card field list** is now built from the profile's version-aware headers instead of a static header constant, so `nil_value` appears for CFB 27.
- **Review queue** (Save All / Remove Selected / Clear) now resets the result card once the queue empties, instead of leaving the last reviewed recruit's data on screen.
- **CFB 27 ATH position resolution** — the archetype → real-position whitelist for CFB 27 (`_ath_positions`) was empty, so ATH recruits exported with the literal position `ATH` instead of their resolved real position; populated it for all 10 known CFB 27 ATH archetypes.
- **Linux AppImage smoke test** — the bundled smoke-test writer defaulted to writing its result next to the running executable, which fails because an AppImage mounts itself read-only; it now writes next to the `.AppImage` file instead.

### Changed

- `app/core/capture.py` and `app/core/sound.py` are now thin facades over platform backends.
- macOS dark theme setup moved to `app/platform/ui_theme.py`.
- Documentation (README, QUICKSTART, CLAUDE.md) updated for the game-version header bar and per-version preset/table layout.

---

## [0.1.3] — 2026-06-29

### Added

- **Ability & mental trait scraping** — recruit scans now extract up to 5 abilities and 3 mental traits, each with their tier (Bronze / Silver / Gold / Platinum) detected via HSV icon-color classification. OCR results are fuzzy-matched against a bundled ability table keyed by position + archetype for higher accuracy. The result card shows editable name + tier dropdown for each ability and mental.
- **Missing-attribute correction slots** — the result card now renders empty attribute rows (with a dropdown of remaining attribute names and a value input) when a scan returns fewer attributes than expected for the position, making it easy to fill in missed fields without re-scanning.
- **Automatic schema migration** — existing SQLite databases are transparently upgraded with new columns (abilities, mentals) on first load, so users upgrading from earlier versions keep their data.
- **Calibration preset merging** — when new ROI keys are added to a bundled preset (e.g. `abilities`, `mentals`), they are automatically merged into saved user calibrations so new features work without re-calibrating.

### Fixed

- **"Save All" keeps invalid scans in queue** — previously, "Save All to Collection" silently discarded records that failed validation. Now only valid recruits are saved; invalid ones remain in the queue for correction or removal.

### Changed

- **Expanded recruit schema** — the CSV/SQLite schema now includes `ABILITY_1–5`, `ABILITY_1_LEVEL–5_LEVEL`, `MENTAL_1–3`, and `MENTAL_1_LEVEL–3_LEVEL` columns between basic info and attributes.
- **Documentation refresh** — README expanded with ability/mental feature description and reorganized test instructions; QUICKSTART updated with save-all behavior clarification; updated screenshots.

---

## [0.1.2] — 2026-06-26

### Added

- **macOS support** — cross-platform sound playback (`.aiff` via `afplay` on macOS), PyInstaller `.app` bundle, optional DMG packaging via `create-dmg`, and CI smoke tests on macOS.
- **Snapshot review for auto-capture** — each auto-captured recruit now caches the screen frame at scan time. Clicking a queued recruit pauses the live preview and shows the original screenshot with a "SNAPSHOT" badge, making it easy to compare OCR results against the source. A "Back to Live" button resumes the feed.

### Fixed

- **Star template matching fallback** — when the scaled star template exceeds the ROI dimensions, it is now shrunk to fit rather than falling back to less accurate contour detection.

### Changed

- Python version requirement raised to **3.12+**.

---

## [0.1.1] — 2026-06-24

### Added

- **Update checker** — checks GitHub Releases on launch and shows a banner when a newer version is available.

### Fixed

- **Scan crash at non-base resolutions** — the star-rating template (captured at 1440p) is now scaled to match the user's actual resolution, fixing a `matchTemplate` assertion failure when the capture region was smaller than the template.
- **Window expanding to full screen width on scan** — the result card is now scrollable, so populating scan results no longer forces the window wider (fixes capture-card setups where the scraper shares screen space with a capture utility).

---

## [0.1.0] — 2026-06-23

First public release. Feature-complete desktop app for capturing recruit cards.

### Added

- **Profile-driven capture engine** — pluggable `ScrapeProfile` interface with recruits as the first profile. OCR (RapidOCR/ONNX) + computer-vision pipeline (star counting via template match, gem/bust via HSV).
- **PySide6 desktop UI** — tabbed interface (Capture, Calibrate, Data, Settings) replacing the original CLI.
- **Visual ROI editor + auto-calibration** — drag/resize capture regions over a live screenshot; auto-scale bundled 1440p preset to any resolution.
- **SQLite data viewer + CSV export** — sortable, filterable, de-duplicated table; re-scanning a recruit updates instead of duplicating.
- **Live OCR confidence + inline correction** — low-confidence fields are flagged; click to fix before saving.
- **Auto-capture / batch mode** — detects new recruit cards via frame-diff and queues them for review.
- **Windows installer** — PyInstaller + Inno Setup; per-user install, no admin required (~320 MB).
- **Configurable settings** — scan hotkey, success/fail sounds, confidence threshold, auto-save.
