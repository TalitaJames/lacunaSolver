import cv2
import numpy as np
import colorManipulation as color
import time


def cropToCircle(img, circle=None):
    if circle is None:
        circle = findCircle(img)
        if circle is None: # If a circle wasn't found, don't crop the image
            return None

    x, y, r = circle
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    cv2.circle(mask, (x,y), r, (255), thickness=-1)

    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return masked_img


def findCircle(img) -> tuple:
    '''Given an image of Lacuna, return the image masked to only show the inside play circle'''
    colourRangeAqua = ([110, 130], [50, 100], [0,255])

    kernel = np.ones((5,5),np.float32)/25
    blured = cv2.filter2D(img,-1,kernel)

    imgAquaCircle = color.hsvColorFilterTupple(blured, colourRangeAqua)
    imgGray = cv2.cvtColor(imgAquaCircle, cv2.COLOR_BGR2GRAY)
    _,imgBW = cv2.threshold(imgGray, 50,255,cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(imgBW, cv2.HOUGH_GRADIENT, 1.2, 750)

    if circles is None:
        return None

    # circles = np.squeeze(circles).astype(int)
    circles = np.reshape(circles, newshape=(circles.shape[1],3))
    circles = circles.astype(int)

    if len(circles) == 1: #Only one circle found, it must be the best
        closest_index = 0
    else:
        # get the (x,y) center of image
        centerY, centerX = img.shape[:2] # height, width
        centerX = int(centerX/2)
        centerY = int(centerY/2)
        distance_toCenter = np.sqrt((circles[:, 0] - centerX) ** 2 + (circles[:, 1] - centerY) ** 2) # find distance from each circle to img center
        closest_index = np.argmin(distance_toCenter) # Find the index of the circle closest to center of img

    bestCircle = circles[closest_index] # best circle
    return bestCircle.tolist()

def findSquare(img):
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (13,13), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Two pass dilate with horizontal and vertical kernel
    kernalSize = (3,3)
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, kernalSize)
    dilate = cv2.dilate(thresh, structuringElement, iterations=2)

    # Find contours, filter using contour threshold area, and draw rectangle
    cnts,hierarchy = cv2.findContours(dilate, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # print(f"{cnts=}, {hierarchy=}")

    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.drawContours(img, cnts, -1, (0,255,0), 3)
    return dilate
    # for c in cnts:
    #     area = cv2.contourArea(c)
    #     if area > 20:
    #         x,y,w,h = cv2.boundingRect(c)
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 3)


    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # imagem = (255-gray)
    # ret,thresh = cv2.threshold(imagem,120,200,1)
    # contours,h = cv2.findContours(thresh,1,2)
    # print(f"{len(contours)=}")

    # for cnt in contours:
    #     approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    #     # print (len(approx))
    #     print(f"{cnt=}, {approx=}")
    #     if len(approx)==4:
    #         cv2.drawContours(img,[cnt],0,(0,0,255))
    #     pass

    return img


def cropToBlob(img):
    '''Given an image of Lacuna, return the image masked to only show the inside play circle'''
    # Convert the image to grayscale
    imgGS = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarize the grayscale image with a threshold of 0.5 (128 in OpenCV scale)
    _, imgBW = cv2.threshold(imgGS, 128, 255, cv2.THRESH_BINARY)

    # Structuring element (disk-shaped) for morphological closing
    structureElement = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200, 200))  # Approx. 'disk' in MATLAB
    closedImg = cv2.morphologyEx(imgBW, cv2.MORPH_CLOSE, structureElement)

    # Find connected components and retain the largest blob
    num_labels, labels_im = cv2.connectedComponents(closedImg)
    sizes = np.bincount(labels_im.ravel())

    # The second largest component corresponds to the largest blob (ignore background)
    largest_blob_label = np.argmax(sizes[1:]) + 1
    largest_blob = np.uint8(labels_im == largest_blob_label) * 255 # if in the largest blob, go black
    largest_blob_inverse = cv2.bitwise_not(largest_blob)

    # Apply the mask to the original image
    croppedImg = np.copy(img)
    croppedImg = cv2.bitwise_and(croppedImg, croppedImg, mask=largest_blob_inverse)

    return croppedImg