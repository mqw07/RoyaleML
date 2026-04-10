import json
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent / "Assets"
CARDS_CSV = _ASSETS / "clash_royale_cards_1.json"

def load_cards_json(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return json.load(f)

