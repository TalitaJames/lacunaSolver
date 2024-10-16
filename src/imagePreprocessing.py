import cv2 as cv
import numpy as np
import statistics
import colorManipulation as color

def cropToCircle(img):
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

if __name__ == "__main__":
    # Usage example:
    img = cv.imread('images/training_data/001.jpg')

    cropped_img = cropToCircle(img)
    # cv.imwrite('out/progress/cropped_image2.jpg', cropped_img)

    colourRangeAqua = ([172/255, 182/255], statistics.mean([31,33,39,26, 42])/255, statistics.mean([79,79,73, 74,76])/255)
    lacunaFilteredOne = color.hsvColorFilterTupple(img, colourRangeAqua)
    # cv.imwrite('out/progress/hsv_image_aqua.jpg', lacunaFilteredOne)

