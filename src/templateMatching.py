import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import imagePreprocessing as IP
 
img_rgb = cv.imread('images/001.jpg')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_rgb = IP.cropToCircle(img_rgb)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread("images/templates/yellow.jpg", cv.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]


res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.4
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
 
cv.imwrite('res.png',img_rgb)