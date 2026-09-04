"""Project and asset locations.

Import this after putting ``src`` on ``sys.path`` (see ``_bootstrap``).
"""

from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PACKAGE_ROOT.parent
PROJECT_ROOT = SRC_ROOT.parent
ASSETS = PROJECT_ROOT / "Assets"
GAME_DATA = ASSETS / "Game_Data"
ELIXIR_TEMPLATES = ASSETS / "elixir_templates"
ELIXIR_IDENTIFICATIONS = ASSETS / "elixir_identifications"


def elixir_digits_dir() -> Path:
    if ELIXIR_TEMPLATES.is_dir():
        return ELIXIR_TEMPLATES
    return ELIXIR_IDENTIFICATIONS


def ensure_src_on_path() -> None:
    src = str(SRC_ROOT)
    if src not in sys.path:
        sys.path.insert(0, src)


if __name__ == "__main__":
    print(f"PROJECT_ROOT={PROJECT_ROOT}")
    print(f"ASSETS={ASSETS} exists={ASSETS.is_dir()}")
    print(f"GAME_DATA={GAME_DATA} exists={GAME_DATA.is_dir()}")
    print(f"elixir_digits_dir={elixir_digits_dir()}")
