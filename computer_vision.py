import cv2 as cv
import numpy as np
from mss import MSS    
import identification

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
    gameplay_capture = grab_frame(region)
    return identification.identify(gameplay_capture)

class Prediction:
    # An instance of troop detection. 
    pass

if __name__ == '__main__':
    print(identify_frame(capture))


