import cv2 as cv
import numpy as np
import time
import math

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

def locateOneColor(img, color):
    '''given an image, return all the locations of that colour'''

    colorFilterFrame = hsvColorFilterTupple(img, color)
    imgGS = cv.cvtColor(colorFilterFrame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(imgGS, (15, 15), 0)
    _, imgBW = cv.threshold(blurred,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    kernalSize = (5,5)
    structuringElement = cv.getStructuringElement(cv.MORPH_RECT, kernalSize)
    dilate = cv.dilate(imgBW, structuringElement, iterations=2)

    return dilate

    # Find contours of the white regions
    contours, _ = cv.findContours(imgBW, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    centers = [] # List of each (x,y) point

    for contour in contours: # Through each contour, find the centroid
        tooClose = False # if the point is "too close" to another, it is deemed to be the same point and is ignored

        M = cv.moments(contour) # Calculate the moment
        if M["m00"] != 0:  # To avoid division by zero
            # Calculate the x and y coordinates of the centroid
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            for d in centers: # Compare to existing centers (to see if too close)
                dx, dy = d
                distance = math.sqrt((cx-dx)**2 + (cy-dy)**2)

                if distance<75: # if not in the same clump
                    tooClose = True
                    break # Don't have to check any more if one is too close

            if not tooClose:
                centers.append((cx, cy))

    return centers

def locateAllColors(img):
    '''given a frame, find the position of all lacuna tiles'''

    #region colors
    #Colour in the form [(Hue minMax, saturation minMax, value minMax), (Blue, Green, Red)]
    colorTuppleOrange = [([7,10], [100,255],[200, 255]),    (  0, 123, 255)]
    colorTupplePink =   [([7,10], [0,100],[0, 255]),        (236,  16, 234)] #WIP
    colorTuppleAqua =   [([85,95], [100,225],[175, 255]),   (222, 236,  16)]
    colorTupplePurple = [([140,170], [0,75],[150, 255]),    (246,  18, 160)]
    colorTuppleBlue =   [([100,120], [150,225],[170, 255]), (246,  18, 160)]
    colorTuppleBrown =  [([15,30], [100,225],[0, 255]),     ( 18, 246,  93)] #gets yellow, and gold user
    colorTuppleYellow = [([10,20], [140,190],[230, 255]),   ( 18, 246, 213)] #gets yellow, and gold user #gets yellow, and gold user (but cleaner)

    # allColors = [colorTuppleOrange, colorTupplePink, colorTuppleAqua, colorTupplePurple, colorTuppleBlue, colorTuppleBrown, colorTuppleYellow]
    allColors = [colorTupplePink]
    #endregion colors

    for color in allColors:
        colorXY = locateOneColor(img, color[0]);
        print(f"\n{color=} (has {len(colorXY)})", flush=True)

        for x,y in colorXY:
            cv.circle(img, (x, y), 4, color[1], -1)
            print(f"\t({x},{y})")

    return img #TODO make this return list of colours instead
