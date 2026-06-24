# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate icon.icns from icon.png (runs on any platform — requires Pillow).

Usage:  python packaging/gen_icns.py
"""

from pathlib import Path

from PIL import Image

SRC = Path(__file__).resolve().parent.parent / "app" / "resources" / "icon.png"
OUT = Path(__file__).resolve().parent / "icon.icns"

SIZES = [16, 32, 64, 128, 256, 512]

img = Image.open(SRC).convert("RGBA")
out_images = []
for size in SIZES:
    out_images.append(img.resize((size, size), Image.LANCZOS))
    out_images.append(img.resize((size * 2, size * 2), Image.LANCZOS))

out_images[0].save(OUT, format="ICNS", append_images=out_images[1:])
print(f"Created {OUT}")
