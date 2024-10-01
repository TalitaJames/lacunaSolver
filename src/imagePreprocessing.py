import cv2 as cv
import numpy as np

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

def hsvColorFilterTupple(img, colorStats: tuple):
    hue_range, saturation, value = colorStats
    return hsvColorFilter(img, hue_range, saturation, value)

def hsvColorFilter(img, hue_range: list, saturation: float, value: float):
    '''Takes an image, filters it by some colour [hue_min, hue_max] and saturation, value (all as decimals 0-1)'''
    # Convert the to HSV color
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Split the HSV channels
    hue_channel, saturation_channel, value_channel = cv.split(hsv_image)

    # Normalize the hue range from [0, 1] to [0, 180] for OpenCV's HSV range
    hue_min = int(hue_range[0] * 180)
    hue_max = int(hue_range[1] * 180)

    # Create the mask for the color range
    colour_mask = (hue_channel >= hue_min) & (hue_channel <= hue_max) & \
                  (saturation_channel >= saturation * 255) & (value_channel >= value * 255)

    # Set pixels outside the mask to black
    filtered_img = np.copy(img)
    filtered_img[~colour_mask] = 0

    return filtered_img


if __name__ == "__main__":
    # Usage example:
    img = cv.imread('images/001.jpg')

    cropped_img = cropToCircle(img)
    cv.imwrite('out/progress/cropped_image.jpg', cropped_img)

    colourRangeAqua = ([172/255, 182/255], statistics.mean([31,33,39,26, 42])/255, statistics.mean([79,79,73, 74,76])/255)
    lacunaFilteredOne = hsvColorFilterTupple(img, colourRangeAqua)
    cv.imwrite('out/progress/hsv_image_aqua.jpg', lacunaFilteredOne)
