import cv2 as cv
from classifications import classification, identification
import numpy as np
from mss import MSS    
import time
from pathlib import Path

capture = {
            "top": 55,
            "left": 1755,
            "width": 760,
            "height": 1310
            }

capture_elixir = {
                    "top": 1315,
                    "left": 1963,
                    "width": 38,
                    "height": 40
                }

def grab_frame(region: dict):
    # Grabs the current frame of Gameplay

    with MSS() as sct:
        ss = sct.grab(region)
        img = np.asarray(ss)
    return cv.cvtColor(img, cv.COLOR_BGRA2BGR)

def show_frame(image):
    # Shows the image captured. Use in tandem with grab_frame()

    cv.imshow('Screenshot', image)
    cv.waitKey(0)

def identify_frame(region: dict) -> dict:
    # Run a single frame through the identification model

    gameplay_capture = grab_frame(region)
    return identification.identify(gameplay_capture)

def run_loop(region: dict):
    """
     Create a running loop, identifying the region and current elixir at the given frame rate.
    """
    frame_interval = 0.7

    skip = False
    prev_identification = None
    with MSS() as sct:
        
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

            #print({x: len(identifications[x]) for x in identifications}, {'e': elixir_count})
            #print(f"{identifications}, {elixir_count}")
            # Pass in identifications, elixir_count
            if skip:
                prev_identification = identifications
                prev_ecount = e_count
            else:
                # TODO: Factor in prev elixir_count
            
                print(classification.infer_from_movement(prev_identification, identifications))
                prev_identification = identifications

            key = cv.waitKey(1)
            if key == ord('q'):
                break
            
            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            skip = not(skip)

    cv.destroyAllWindows()
    

def assign_teams(region: dict, frame_rate = 1):
    # Create a running loop, identifying the region at the given frame rate.
    frame_interval = 1.0 / frame_rate

    with MSS() as sct:
        script_dir = Path(__file__).resolve().parent
        assets_dir = script_dir / "Assets"

        loop_count = 0
        while True:
            loop_start = time.perf_counter()
            ss = sct.grab(region)
            img = np.asarray(ss)

            frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            #identifications = identification.identify(frame)

            ess = sct.grab(capture)
            eimg = np.asarray(ess)
            output_path = assets_dir / f"{loop_count}.png"
            loop_count += 1
            cv.imwrite(output_path, eimg)

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


