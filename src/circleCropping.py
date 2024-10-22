import cv2 as cv
import numpy as np
import colorManipulation as color


def cropToCircle(img):
    '''Given an image of Lacuna, return the image masked to only show the inside play circle'''
    colourRangeAqua = ([110, 130], [50, 100], [0,255])

    imgAquaCircle = color.hsvColorFilterTupple(img, colourRangeAqua)
    imgGray = cv.cvtColor(imgAquaCircle, cv.COLOR_BGR2GRAY)
    _,imgBW = cv.threshold(imgGray, 50,255,cv.THRESH_BINARY)

    circles = cv.HoughCircles(imgBW, cv.HOUGH_GRADIENT, 1.2, 750)
    circles = np.squeeze(circles).astype(int)

    # get the (x,y) center of image
    centerY, centerX = img.shape[:2] # height, width
    centerX = int(centerX/2)
    centerY = int(centerY/2)

    distance_toCenter = np.sqrt((circles[:, 0] - centerX) ** 2 + (circles[:, 1] - centerY) ** 2) # find distance from each circle to img center
    closest_index = np.argmin(distance_toCenter) # Find the index of the circle closest to center of img

    # Draw the circle on a mask (filled circle)
    x, y, r = circles[closest_index] # best circle

    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    cv.circle(mask, (x,y), r, (255), thickness=-1)

    masked_img = cv.bitwise_and(img, img, mask=mask)

    return masked_img




def cropToBlob(img):
    '''Given an image of Lacuna, return the image masked to only show the inside play circle'''
    # Convert the image to grayscale
    imgGS = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Binarize the grayscale image with a threshold of 0.5 (128 in OpenCV scale)
    _, imgBW = cv.threshold(imgGS, 128, 255, cv.THRESH_BINARY)

    # Structuring element (disk-shaped) for morphological closing
    structureElement = cv.getStructuringElement(cv.MORPH_ELLIPSE, (200, 200))  # Approx. 'disk' in MATLAB
    closedImg = cv.morphologyEx(imgBW, cv.MORPH_CLOSE, structureElement)

    # Find connected components and retain the largest blob
    num_labels, labels_im = cv.connectedComponents(closedImg)
    sizes = np.bincount(labels_im.ravel())

    # The second largest component corresponds to the largest blob (ignore background)
    largest_blob_label = np.argmax(sizes[1:]) + 1
    largest_blob = np.uint8(labels_im == largest_blob_label) * 255 # if in the largest blob, go black
    largest_blob_inverse = cv.bitwise_not(largest_blob)

    # Apply the mask to the original image
    croppedImg = np.copy(img)
    croppedImg = cv.bitwise_and(croppedImg, croppedImg, mask=largest_blob_inverse)

    return croppedImg