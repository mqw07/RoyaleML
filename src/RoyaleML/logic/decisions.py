from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

from RoyaleML.logic.actions import mid_left, place_card


def make_decision(identifications: dict, e_count: int):
    """Make decisions wrt the current game state."""
    y_danger_threshold = 580  # Y level on ally side past bridge
    right_side_threshold = 2125  # X that determines which side the troop is on

    if identifications == {} and e_count >= 7:
        place_card(2, mid_left)
        return

    for troop, positions in identifications.items():
        for position in positions:
            for (x, y), classification in position.items():
                if y > y_danger_threshold and classification == "enemy" and e_count >= 4:
                    if x < right_side_threshold:
                        place_card(1, (x + 1760, y + 150))
                        return
                    else:
                        place_card(1, (x + 1770, y + 150))
                        return


if __name__ == "__main__":
    sample = {"gargouille": [{(151.5, 509.0): "enemy"}, {(194.5, 650.0): "enemy"}]}
    print("Sample identifications:", sample)
    print("Would call make_decision(sample, 6) - skipped so it does not click.")
    # make_decision(sample, 6)
