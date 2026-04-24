import cv2 as cv
import numpy as np
from mss import mss    

capture = {
            "top": 55,
            "left": 1755,
            "width": 760,
            "height": 1310
            }

def grab_frame(region):
    with mss() as sct:
        ss = sct.grab(region)
        img = np.asarray(ss)
    return cv.cvtColor(img, cv.COLOR_BGRA2BGR)

cv.imshow('Screenshot', grab_frame(capture))
cv.waitKey(0)