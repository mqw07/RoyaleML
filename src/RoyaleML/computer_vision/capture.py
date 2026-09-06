from pathlib import Path
import sys
import time

import cv2 as cv
import numpy as np
from mss import MSS

for _parent in Path(__file__).resolve().parents:
    if _parent.name == "src" and (_parent / "RoyaleML").is_dir():
        if str(_parent) not in sys.path:
            sys.path.insert(0, str(_parent))
        break

from RoyaleML.classifications import classification, identification
from RoyaleML.logic.decisions import make_decision
from RoyaleML.paths import ASSETS

capture = {
    "top": 150,
    "left": 1755,
    "width": 760,
    "height": 1100,
}

capture_elixir = {
    "top": 1375,
    "left": 1952,
    "width": 45,
    "height": 40,
}


def grab_frame(region: dict):
    """Grab the current gameplay frame for ``region``."""
    with MSS() as sct:
        ss = sct.grab(region)
        img = np.asarray(ss)
    return cv.cvtColor(img, cv.COLOR_BGRA2BGR)


def show_frame(image):
    """Show a captured image. Use with ``grab_frame()``."""
    cv.imshow("Screenshot", image)
    cv.waitKey(0)


def identify_frame(region: dict) -> dict:
    """Run a single frame through the identification model."""
    gameplay_capture = grab_frame(region)
    return identification.identify(gameplay_capture)


def run_loop(region: dict):
    """Identify troops and elixir on a fixed interval until ``q`` is pressed."""
    frame_interval = 0.7

    skip = False
    prev_identification = None
    with MSS() as sct:
        prev_identification = {}
        while True:
            loop_start = time.perf_counter()
            ss = sct.grab(region)
            img = np.asarray(ss)
            frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            identifications = identification.identify(frame)

            ess = sct.grab(capture_elixir)
            eimg = np.asarray(ess)
            eframe = cv.cvtColor(eimg, cv.COLOR_BGRA2BGR)
            e_count = identification.grab_elixir(eframe)
            cv.imshow("Live", eframe)
            cv.imshow("Game", frame)

            if skip:
                prev_identification = identifications
                prev_ecount = e_count
            else:
                troop_classifications = classification.infer_from_movement(
                    prev_identification, identifications
                )
                print(troop_classifications)
                prev_identification = identifications
                make_decision(troop_classifications, int(e_count))

            key = cv.waitKey(1)
            if key == ord("q"):
                break

            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            skip = not skip

    cv.destroyAllWindows()


def assign_teams(region: dict, frame_rate=1):
    """Capture frames to ``Assets`` at ``frame_rate`` until ``q`` is pressed."""
    frame_interval = 1.0 / frame_rate

    with MSS() as sct:
        assets_dir = ASSETS
        assets_dir.mkdir(parents=True, exist_ok=True)

        loop_count = 0
        while True:
            loop_start = time.perf_counter()
            ss = sct.grab(region)
            img = np.asarray(ss)
            frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

            ess = sct.grab(capture)
            eimg = np.asarray(ess)
            output_path = assets_dir / f"{loop_count}.png"
            loop_count += 1
            cv.imwrite(str(output_path), eimg)

            key = cv.waitKey(1)
            if key == ord("q"):
                break

            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    cv.destroyAllWindows()


class Prediction:
    """An instance of troop detection."""

    pass


if __name__ == "__main__":
    run_loop(capture)
