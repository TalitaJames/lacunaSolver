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
    structuringElement = cv.getStructuringElement(cv.MORPH_RECT, kernalSize) #or: MORPH_ELLIPSE
    dilate = cv.dilate(imgBW, structuringElement, iterations=2)

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
                centers.append([cx, cy])

    if not centers: # centers array is empty, no points found
        centersNP = np.empty((7,2))
        centersNP[:] = np.nan
        return centersNP
    centersNP = np.asarray(sorted(centers)).astype(int) #sorted so same values are in same pos

    #ensure 7x2 shape
    if centersNP.shape[0] > 7: # Trim to the first 7 rows if there are more than 7
        centersNP = centersNP[:7, :]
    elif centersNP.shape[0] < 7: # Less than 7, add nan values to make 7x2 shape
        padding = np.full((7 - centersNP.shape[0], 2), np.nan)
        centersNP = np.vstack([centersNP, padding])

    # print(f"{centersNP=}")
    # centersNP = centersNP.astype(int)
    return centersNP

def locateAllColors(img):
    '''given a frame, find the position of all lacuna tiles'''

    #region colors
    #Color in the form (Hue minMax, saturation minMax, value minMax)
    colorTuppleOrange = ([7,10], [100,255],[200, 255])
    colorTuppleBlue =   ([100,120], [150,225],[170, 255])
    colorTuppleAqua =   ([85,95], [100,225],[175, 255])
    colorTuppleYellow = ([10,20], [140,190],[230, 255]) #gets yellow, and gold user #gets yellow, and gold user (but cleaner)
    colorTuppleBrown =  ([15,30], [100,225],[0, 255]) #gets yellow, and gold user
    colorTupplePink =   ([7,10], [0,100],[0, 255]) #WIP
    colorTupplePurple = ([140,170], [0,75],[150, 255])

    allColors = [colorTuppleOrange, colorTuppleBlue, colorTuppleAqua, colorTuppleYellow, colorTuppleBrown, colorTupplePink, colorTupplePurple]
    #endregion colors
    # return locateOneColor(img, allColors[0][0]);

    allColorPositions = np.empty((7,7,2))

    for i, color in enumerate(allColors):
        colorXY = locateOneColor(img, color);
        allColorPositions[i] = colorXY

    return allColorPositions

#given an int, return a BGR colour
def getColor(color):
    colorBGR = ""
    match color:
        case 0: # Red/Orange
            colorBGR = (  0, 123, 255)
        case 1: # Blue
            colorBGR = (236,  16, 234)
        case 2: # Aqua/Cyan
            colorBGR = (222, 236,  16)
        case 3: # Yellow
            colorBGR = (246,  18, 160)
        case 4: # Brown/green
            colorBGR = (246, 118, 160)
        case 5: # Pink
            colorBGR = ( 18, 246,  93)
        case 6: # Purple
            colorBGR = ( 18, 246, 213)
        case _: #Unknown (Black)
            colorBGR = (  0,  0,   0)

    return colorBGR


def plotAllColors(img, allColors):
    for i, color in enumerate(allColors):
        for x,y in color:
            print(f"{x},{y}")

            if (not np.isnan(x) and not np.isnan(y)) and x>0 and y>0:
                cv.circle(img, (int(x),int(y)), 9, getColor(i), -1)

    return img

def convertColorListToDict(colorList):
    '''given a list [[color], [(x,y), (x,y), ... (x,y)] ... [color]]
    convert the data into the format used by the Board class,
    ie: (id, {nodeData})
    where {nodeData} is {"pos": (x,y), "type": i}
        pos is the x,y position of the token
        type is an int (0-6 inclusive) that represents the color
    '''

    colorGraphData = []
    i = 0 # an itterator to ID each node
    for colorID, colorData in enumerate(colorList):
        for token in colorData:
            tokenInfo = {"pos" : token, "type": colorID}
            colorGraphData.append((i, tuple(tokenInfo)))

    return colorGraphData