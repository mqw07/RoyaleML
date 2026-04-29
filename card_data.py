import json
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent / "Assets"
CARDS_CSV = _ASSETS / "clash_royale_cards_1.json"
SAMPLE_JSON = _ASSETS / "sample.json"

def load_cards_json(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as f:
        items = json.load(f)["items"]
        return {card["name"]: card for card in items}

translation = {
                'archere': 'Archers', 'chevalier': 'Knight', 'gargouille': "Minions", 'geant': 'Giant', 'gobelin': 'Goblin',
                'gobelin_lances': 'Spear Goblins', 'mini_PEKKA': "Mini P.E.K.K.A", 'mousquetaire': 'Musketeer', 'squelette': 'Skeletons',
                'valkyrie': 'Valkyrie', 'zappy': 'Zappies', 'bat': 'Bats'
              }


if __name__ == '__main__':
    cards = load_cards_json(SAMPLE_JSON)
    print(cards)

