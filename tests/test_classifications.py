from RoyaleML.classifications.classification import (
    find_new_troops,
    infer_from_movement,
    vertical_movement,
)


def test_vertical_movement():
    assert vertical_movement((100, 200), (100, 210)) == "enemy"
    assert vertical_movement((100, 200), (100, 190)) == "ally"
    assert vertical_movement((100, 200), (100, 201)) == "still"


def test_infer_from_movement():
    before = {"chevalier": [{"Confidence": 0.9, "Position": (400.0, 900.0)}]}
    after = {"chevalier": [{"Confidence": 0.9, "Position": (400.0, 920.0)}]}
    result = infer_from_movement(before, after)
    assert result == {"chevalier": [{(400.0, 920.0): "enemy"}]}


def test_find_new_troops():
    assert find_new_troops({"archere": []}, {"chevalier": []}) == "archere"
    assert find_new_troops({"chevalier": []}, {"chevalier": []}) is None


if __name__ == "__main__":
    test_vertical_movement()
    test_infer_from_movement()
    test_find_new_troops()
    print("classification tests passed")
