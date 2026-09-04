import json
from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

from RoyaleML.paths import GAME_DATA

CARDS_JSON = GAME_DATA / "clash_royale_cards_1.json"
SAMPLE_JSON = GAME_DATA / "sample.json"

translation = {
    "archere": "Archers",
    "chevalier": "Knight",
    "gargouille": "Minions",
    "geant": "Giant",
    "gobelin": "Goblin",
    "gobelin_lances": "Spear Goblins",
    "mini_PEKKA": "Mini P.E.K.K.A",
    "mousquetaire": "Musketeer",
    "squelette": "Skeletons",
    "valkyrie": "Valkyrie",
    "zappy": "Zappies",
    "bat": "Bats",
}


def load_cards_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        items = json.load(f)["items"]
        return {card["name"]: card for card in items}


if __name__ == "__main__":
    cards = load_cards_json(SAMPLE_JSON)
    print(f"Loaded {len(cards)} cards from {SAMPLE_JSON.name}")
    print(list(cards)[:8])
