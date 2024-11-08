import cv2
import numpy as np
from matplotlib import pyplot as plt


def templateMatch(img, needle):
    threshold = 0.8

    # Split Both into each R, G, B Channel
    imageMainR, imageMainG, imageMainB = cv2.split(img)
    needleR, needleG, needleB = cv2.split(needle)

    # Match each channel
    resultB = cv2.matchTemplate(imageMainR, needleR, cv2.TM_SQDIFF)
    resultG = cv2.matchTemplate(imageMainG, needleG, cv2.TM_SQDIFF)
    resultR = cv2.matchTemplate(imageMainB, needleB, cv2.TM_SQDIFF)

    # Add together to get the total score
    result = resultB * resultG * resultR
    print(result)
    loc = np.where(result >= 3 * threshold)
    print(loc)
    print("loc: ", loc)