import pytest
import cv2 as cv
from computer_vision.computer_vision import grab_frame, capture_elixir, show_frame
from classifications.identification import identify

def test_elixir_grabbing():
    efrme = cv.imread("Assets/elixir_grabbing.png")
    show_frame(eframe)

if __name__ == "__main__":
    test_elixir_grabbing()