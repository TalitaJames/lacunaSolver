import cv2
import numpy as np
import sys
import circleCropping as circle
import colorManipulation as color
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
    if newCircleCoords is not None:
        oldCircleCoords.append(newCircleCoords)

    if(len(oldCircleCoords)==0): # haven't got any historical data yet
        return (0,0,0), oldCircleCoords
    elif (len(oldCircleCoords)>25): # number of previous data it cares about
        oldCircleCoords.pop()

    oldCircleCoords_NP = np.array(oldCircleCoords)
    circleCoords = np.mean(oldCircleCoords_NP, axis=0).astype(int).tolist()

    # print(f"{newCircleCoords=}, {circleCoords=}", flush=True)
    circleCoords[2] +=15

    return circleCoords, oldCircleCoords

def mainVideoLoop(videoFilename = "/dev/video4"):
    timestamp = time.strftime("%Y%m%d-%H%M%S",time.localtime())

    #region init camera & openCV
    cam = cv2.VideoCapture(videoFilename)
    assert cam.isOpened(), "cannot open camera"

    # Set the camera width and height
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    cam.set(cv2.CAP_PROP_FPS, 20)

    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = int(cam.get(cv2.CAP_PROP_FPS))
    print(f"{frame_width=}, {frame_height=}, {frame_fps=}")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'out/logs/{timestamp}.mp4', fourcc, frame_fps, (frame_width, frame_height))


    cv2.namedWindow("Normal", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Normal", 800, 650)

    cv2.namedWindow("Circle", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Circle", 800, 650)

    cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Colour", 800, 650)
    # endregion init camera & openCV

    i = 1
    circleCoords = (0,0,0)
    historicalCircleCoords = []

    startup()
    while True:
        ret, frame = cam.read()

        if i%10 == 0 and i>50:
            circleCoords, historicalCircleCoords = periodicly(frame, historicalCircleCoords)

        circleFrame = circle.cropToCircle(frame, circleCoords)
        # colourFrame = color.hsvColorFilterTupple(circleFrame, colorTuppleOrange)
        colourFrame = color.locateAllColors(circleFrame)
        out.write(frame) # Save the camera footage

        # Display the captured frame
        cv2.imshow("Normal", frame)
        cv2.imshow("Circle", circleFrame)
        cv2.imshow("Colour", colourFrame)
        # cv2.imwrite(f"out/logs/CIRCLE_{time.strftime('%Y%m%d-%H%M%S',time.localtime())}.png",circleFrame)

        # Press "q" to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

        i+=1
        # print(i)

    # Release the capture and writer objects
    cam.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    mainVideoLoop()

    # img = cv2.imread("out/logs/CIRCLE_20241104-155642.png")
    # color.locateAllColors(img)
