from pathlib import Path
import sys

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break


def vertical_movement(pos1: tuple, pos2: tuple, min_movement=3) -> str:
    """Determines the movement of a class for two given positions."""
    dy = pos2[1] - pos1[1]
    if dy > min_movement:
        return "enemy"
    elif dy < -min_movement:
        return "ally"
    return "still"


def find_new_troops(identification_1, identification_2) -> str:
    """Returns the single new troop class found, if exactly one appeared."""
    new_troops = identification_1.keys() - identification_2.keys()
    if not new_troops or len(new_troops) > 1:
        return ""
    return new_troops.pop()


def infer_from_movement(identification_1: dict, identification_2: dict) -> dict:
    """Infer team from two adjacent captures of the same troop classes."""
    res = {}
    if not identification_1 or not identification_2:
        return res
    common_troops = identification_1.keys() & identification_2.keys()
    for troop in common_troops:
        res[troop] = []
        for i in range(min(len(identification_1[troop]), len(identification_2[troop]))):
            pos2 = identification_2[troop][i]["Position"]
            res[troop].append(
                {pos2: vertical_movement(identification_1[troop][i]["Position"], pos2)}
            )
    return res


def infer_from_elixir(
    identification_1: dict, identification_2: dict, elixir_1: int, elixir_2: int
) -> dict:
    """
    TODO FINISH THIS
    Infer the team of the current cards based on the user's elixir spent from two adjacent captures
    """
    res = {}
    initial_troops = identification_1.keys()
    final_troops = identification_2.keys()
    if elixir_2 < elixir_1:
        return {}
    return res

if __name__ == "__main__":
    frame_a = {"chevalier": [{"Confidence": 0.9, "Position": (400.0, 900.0)}]}
    frame_b = {"chevalier": [{"Confidence": 0.9, "Position": (400.0, 920.0)}]}
    print("vertical_movement:", vertical_movement((400, 900), (400, 920)))
    print("infer_from_movement:", infer_from_movement(frame_a, frame_b))
    print("find_new_troops:", find_new_troops({"archere": []}, frame_a))
