import cv2
import numpy as np
import sys
import circleCropping as circle
import colorManipulation as color
import notebookCompanion
import time
import statistics


colorTuppleOrange = ([7,10], [100,255],[200, 255])
colorTupplePink = ([7,10], [0,100],[0, 255]) #WIP
colorTuppleAqua = ([85,95], [100,225],[175, 255])
colorTupplePurple = ([140,170], [0,75],[150, 255])
colorTuppleBlue = ([100,120], [150,225],[170, 255])
colorTuppleBrown = ([15,30], [100,225],[0, 255]) #gets yellow, and gold user
colorTuppleYellow = ([10,20], [140,190],[230, 255]) #gets yellow, and gold user (but cleaner)

colorTuppleMess = ([0,20], [0,255],[0, 255]) #gets yellow, and gold user (but cleaner)


def startup():
    '''
    open camera ect
    find first circle
    '''
    
    pass

def periodicly(frame, oldCircleCoords) -> tuple:
    '''
    take in old circle position
    average the old and new circle
    update circle
    '''

    newCircleCoords = circle.findCircle(frame)
    if newCircleCoords is None:
        print("old")
        circleCoords = oldCircleCoords
    elif(sum(oldCircleCoords) == 0): # if the old circle hasn't been "properly" initialized
        circleCoords = newCircleCoords
    else:
        print("new check")
        oldX, oldY, oldR = oldCircleCoords
        newX, newY, newR = newCircleCoords
        avgX = statistics.mean([oldX,newX])
        avgY = statistics.mean([oldY,newY])
        avgR = statistics.mean([oldR,newR])
        circleCoords = (avgX, avgY, avgR)

    print(f"{oldCircleCoords=}, {newCircleCoords=}, {circleCoords=}", flush=True)

    return circleCoords


if __name__ == "__main__":
    timestamp = time.strftime("%Y%m%d-%H%M%S",time.localtime())
    
    # Open the default camera
    cam = cv2.VideoCapture("/dev/video4")
    assert cam.isOpened(), "cannot open camera"

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'out/logs/{timestamp}.mp4', fourcc, 20.0, (frame_width, frame_height))


    cv2.namedWindow("Normal", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Normal", 800, 650)

    cv2.namedWindow("Circle", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Circle", 800, 650)

    cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Colour", 800, 650)
    
    i = 1
    circleCoords = (0,0,0)

    startup()
    while True:
        ret, frame = cam.read()

        colourFrame = color.hsvColorFilterTupple(frame, colorTupplePurple)
        if i%30 == 0 and i>100:
            circleCoords = periodicly(frame, circleCoords)

        circleFrame = circle.cropToCircle(frame, circleCoords)
        cv2.imshow("Circle", circleFrame)

        # Write the frame to the output file
        out.write(frame)

        # Display the captured frame
        cv2.imshow("Normal", frame)
        cv2.imshow("Colour", colourFrame)

        # Press "q" to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

        i+=1
        # print(i)

    # Release the capture and writer objects
    cam.release()
    out.release()
    cv2.destroyAllWindows()