#!/usr/bin/env python3
"""Quarto post-render hook: export every marimo notebook in apps-src/ to a
self-contained WebAssembly site under <output-dir>/apps/<name>/.

Runs after full renders (`quarto render`, CI). During `quarto preview` of a
single file it only builds apps that are missing, to stay fast.
Set BUILD_APPS=1 to force a rebuild, BUILD_APPS=0 to skip entirely.

Requires either `uv` (preferred; uses pyproject.toml) or `marimo` on PATH.
If neither is available it prints a warning and exits 0 so prose authors
without Python can still render the book.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "apps-src"
OUT = ROOT / os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_book") / "apps"


def marimo_cmd() -> list[str] | None:
    if shutil.which("uv"):
        return ["uv", "run", "--project", str(ROOT), "marimo"]
    if shutil.which("marimo"):
        return ["marimo"]
    return None


def main() -> int:
    flag = os.environ.get("BUILD_APPS")
    if flag == "0":
        return 0
    full_render = bool(os.environ.get("QUARTO_PROJECT_RENDER_ALL")) or flag == "1"

    apps = sorted(p for p in SRC.glob("*.py") if not p.name.startswith("_"))
    todo = [p for p in apps if full_render or not (OUT / p.stem / "index.html").exists()]
    if not todo:
        return 0

    cmd = marimo_cmd()
    if cmd is None:
        print("[build_apps] WARNING: neither `uv` nor `marimo` found; "
              "skipping interactive apps.", file=sys.stderr)
        return 0

    for app in todo:
        dest = OUT / app.stem
        print(f"[build_apps] {app.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
        subprocess.run(
            [*cmd, "export", "html-wasm", str(app), "-o", str(dest),
             "--mode", "run", "--no-show-code", "-f"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
