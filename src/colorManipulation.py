import cv2 as cv
import numpy as np

def hsvColorFilterTupple(img, colorStats: tuple):
    hue_range, saturation, value = colorStats
    return hsvColorFilter(img, hue_range, saturation, value)

def hsvColorFilter(img, hue_range: list, saturation: list, value: list):
    '''Takes an image, filters it by some colour [hue_min, hue_max] and saturation [min, max], value (all ints 0-255)'''
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) # Convert BGR to HSV

    # define colour range in HSV
    lower_blue = np.array([hue_range[0],saturation[0],value[0]])
    upper_blue = np.array([hue_range[1],saturation[1],value[1]])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    filtered_img = cv.bitwise_and(img,img, mask= mask) # Bitwise-AND mask and original image

    return filtered_img

