from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

from RoyaleML.computer_vision.card_data import SAMPLE_JSON, load_cards_json, translation

cards = load_cards_json(SAMPLE_JSON)


class Troop:
    """A detected troop, mapped from the model class name to card stats."""

    def __init__(self, name, y_cord) -> None:
        self.name = translation[name]
        card_dict = cards[self.name]
        self.elixir_cost = card_dict["elixirCost"]
        self.group_card = card_dict["groupCard"]
        self.y_cord = y_cord
        if self.y_cord < 580:
            self.team = "e"
        else:
            self.team = "f"


class Match:
    """An instance of a Clash Royale match and the cards currently in play."""

    def __init__(self, o_curr_elixir: int = 6):
        self.elixir_rate = 1 / 2.8
        self.current_troops = {}
        self.o_curr_elixir = o_curr_elixir

    def play_card(self, troop: Troop):
        pass


if __name__ == "__main__":
    knight = Troop("chevalier", 900)
    match = Match()
    print(f"{knight.name} cost={knight.elixir_cost} team={knight.team}")
    print(f"Match opponent elixir={match.o_curr_elixir} rate={match.elixir_rate:.3f}")
