from pathlib import Path

import cv2 as cv

from RoyaleML.classifications.identification import grab_elixir
from RoyaleML.computer_vision.capture import show_frame
from RoyaleML.paths import ASSETS, ELIXIR_IDENTIFICATIONS


def test_elixir_grabbing():
    image_path = ASSETS / "elixir_grabbing.png"
    if not image_path.is_file():
        image_path = ELIXIR_IDENTIFICATIONS / "6.png"
    eframe = cv.imread(str(image_path))
    assert eframe is not None, f"Could not read {image_path}"
    e_count = grab_elixir(eframe)
    assert e_count == "6"


if __name__ == "__main__":
    image_path = ASSETS / "elixir_grabbing.png"
    if not image_path.is_file():
        image_path = ELIXIR_IDENTIFICATIONS / "6.png"
    eframe = cv.imread(str(image_path))
    print(f"{image_path.name} -> {grab_elixir(eframe)}")
    if eframe is not None:
        show_frame(eframe)
