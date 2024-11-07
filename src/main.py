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

def averageData(newData, oldData, size):
    print(f"{type(newData)=}")

    if newData is not None: # sometimes the data maybe none (ie not found)
        oldData.append(newData)

    if(len(oldData)==0): # haven't got any historical data yet
        return newData, oldData

    elif (len(oldData)>size): # number of previous data it cares about
        oldData.pop()

    # work out the average data
    oldData_NP = np.array(oldData)
    circleCoords = np.mean(oldData_NP, axis=0).astype(int).tolist()

    return circleCoords, oldData


def circleUpdate(frame, oldCircleCoords) -> tuple:
    '''
    take in current frame
    finds the new circle, then add it to the previous circle circle coordinates
    averate all
    update circle
    '''

    newCircleCoords = circle.findCircle(frame)
    # print(f"{newCircleCoords=}, {circleCoords=}", flush=True)

    return averageData(newCircleCoords, oldCircleCoords, 5)


def mainVideoLoop(videoFilename = "/dev/video4", save=True):
    timestamp = time.strftime("%Y%m%d-%H%M%S",time.localtime())

    #region init camera & openCV
    cam = cv2.VideoCapture(videoFilename)
    assert cam.isOpened(), "cannot open camera"

    # Set the camera width and height
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv2.CAP_PROP_FPS, 30)

    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = int(cam.get(cv2.CAP_PROP_FPS))
    print(f"{frame_width=}, {frame_height=}, {frame_fps=}")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    if save:
        out = cv2.VideoWriter(f'out/logs/{timestamp}.mp4', fourcc, frame_fps, (frame_width, frame_height))

    cv2.namedWindow("Normal", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Normal", 800, 650)

    cv2.namedWindow("Circle", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Circle", 800, 650)
    # endregion init camera & openCV

    i = 1
    circleCoords = (616,310, 300) #initial circle estimate
    historicalCircleCoords = []

    startup()
    while True:
        ret, frame = cam.read()

        if i%300 == 0 and i>50:
            circleCoords, historicalCircleCoords = circleUpdate(frame, historicalCircleCoords)
            print(f"{i}, {circleCoords=}", flush=True)

        circleFrame = circle.cropToCircle(frame, circleCoords)
        colourFrame = color.locateAllColors(circleFrame)
        if save: #if the footage is new save it
            out.write(frame) # Save the camera footage

        # Display the captured frame
        cv2.imshow("Normal", frame)
        cv2.imshow("Circle", colourFrame)
        # cv2.imwrite(f"out/logs/CIRCLE_{time.strftime('%Y%m%d-%H%M%S',time.localtime())}.png",circleFrame)

        # Press "q" to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

        i+=1

    # Release the capture and writer objects[694, 294, 210]

    cam.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # mainVideoLoop(videoFilename="out/logs/20241107-154335.mp4", save=False)
    mainVideoLoop(videoFilename="out/logs/20241107-164358.mp4", save=False)
    # mainVideoLoop()