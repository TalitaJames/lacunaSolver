import cv2 as cv
import numpy as np
import sys

if __name__ == "__main__":
    
    img = cv.imread('out/progress/hsv_image_aqua.jpg', cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img = cv.medianBlur(img,5)
    # cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    _, cimg = cv.threshold(img, 50, 255, cv.THRESH_BINARY)

    
    print("image loaded!")

    circles = cv.HoughCircles(cimg,cv.HOUGH_GRADIENT,1,250,
                                param1=50,param2=30,minRadius=500,maxRadius=0)
    
    print("Circles drawn!")
    print(f"{circles=}")
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(cimg,(i[0],i[1]),2,(0,0,255),2)
    
    win_name='detected circles'
    cv.namedWindow(win_name, cv.WINDOW_NORMAL)
    cv.imshow(win_name, img)
    cv.resizeWindow(win_name, 500, 900)
    cv.waitKey(0)
    cv.destroyAllWindows()
    