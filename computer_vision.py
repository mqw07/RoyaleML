import cv2 as cv
import numpy as np
from mss import MSS    
import identification
import time

capture = {
            "top": 55,
            "left": 1755,
            "width": 760,
            "height": 1310
            }

def grab_frame(region: dict):
    # Grabs the current frame of Gameplay

    with MSS() as sct:
        ss = sct.grab(region)
        img = np.asarray(ss)
    return cv.cvtColor(img, cv.COLOR_BGRA2BGR)

def show_frame(image):
    # Shows the image captured

    cv.imshow('Screenshot', image)
    cv.waitKey(0)

def identify_frame(region: dict) -> dict:
    # Run a single frame through the identification model

    gameplay_capture = grab_frame(region)
    return identification.identify(gameplay_capture)

def run_loop(region: dict, frame_rate = 1):
    # Create a running loop, identifying the region at the given frame rate.
    frame_interval = 1.0 / frame_rate

    with MSS() as sct:
        while True:
            loop_start = time.perf_counter()
            ss = sct.grab(region)
            img = np.asarray(ss)
            frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            cv.imshow("Live", frame)
            identifications = identification.identify(frame)
            print({x: len(identifications[x]) for x in identifications})

            # Call elixir counting function here

            key = cv.waitKey(1)
            if key == ord('q'):
                break

            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    cv.destroyAllWindows()

# NEEDS WORK
def game_loop(region: dict, frame_rate = 1):
    # Create a running loop, identifying the region at the given frame rate while using class based identification to make predictions.
    frame_interval = 1.0 / frame_rate

    with MSS() as sct:
        while True:
            loop_start = time.perf_counter()
            ss = sct.grab(region)
            img = np.asarray(ss)
            frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            cv.imshow("Live", frame)
            identifications = identification.identify(frame)
            print({x: len(identifications[x]) for x in identifications})

            # Call elixir counting function here

            key = cv.waitKey(1)
            if key == ord('q'):
                break

            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    cv.destroyAllWindows()
    
class Prediction:
    # An instance of troop detection. 
    pass

if __name__ == '__main__':
    run_loop(capture)


