import cv2 as cv
import numpy as np

needle = cv.imread("Assets/Game_Data/Skeletons_icon.png", cv.IMREAD_GRAYSCALE)
haystack = cv.imread("Assets/Game_Data/IMG_7789.png", cv.IMREAD_GRAYSCALE)

needle = cv.Canny(needle, 50, 150)
haystack = cv.Canny(haystack, 50, 150)

result = cv.matchTemplate(haystack, needle, cv.TM_CCORR_NORMED)

cv.imshow("Result", result)
cv.waitKey()
cv.destroyAllWindows()

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('Best match location:', max_loc)
print('Best match confidence:', max_val)
