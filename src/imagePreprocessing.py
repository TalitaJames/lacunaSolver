import cv2 as cv
import numpy as np
import statistics
import colorManipulation as color


if __name__ == "__main__":
    # Usage example:
    img = cv.imread('images/training_data/001.jpg')

    cropped_img = cropToCircle(img)
    # cv.imwrite('out/progress/cropped_image2.jpg', cropped_img)

    colourRangeAqua = ([172/255, 182/255], statistics.mean([31,33,39,26, 42])/255, statistics.mean([79,79,73, 74,76])/255)
    lacunaFilteredOne = color.hsvColorFilterTupple(img, colourRangeAqua)
    # cv.imwrite('out/progress/hsv_image_aqua.jpg', lacunaFilteredOne)

