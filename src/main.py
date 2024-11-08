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

def averageDataList(newData, oldData, size=5):
    '''adds a new peice of data to the range
    data is averaged based on size (int) of previous data'''

    if newData is not None: # sometimes the data maybe none (ie not found)
        oldData.append(newData)

    if(len(oldData)==0): # haven't got any historical data yet
        return newData, oldData

    elif (len(oldData)>size): # number of previous data it cares about
        oldData.pop()

    # work out the average data
    oldData_NP = np.array(oldData)
    averagedResult = np.mean(oldData_NP, axis=0).astype(int).tolist()

    return averagedResult, oldData

def averageDataNumpy(newData, oldData, size=5):
    '''adds a new peice of data to the range
    data is averaged based on size (int) of previous data'''

    if newData is not None: # sometimes the data maybe none (ie not found)
        oldData = np.vstack([oldData, newData])

    if(len(oldData)==0): # haven't got any historical data yet
        return newData, oldData

    elif (len(oldData)>size): # number of previous data it cares about
        oldData = np.delete(oldData, 0, axis=0)

    # work out the average data
    oldData_NP = np.array(oldData)
    averagedResult = np.mean(oldData_NP, axis=0).astype(int)

    print(f"\t{averagedResult.shape}, {oldData.shape}")
    return averagedResult, oldData


def colorUpdate(frame, historicalTokenData):

    tokenData = color.locateAllColors(frame)
    averagedTokenData = tokenData.copy()

    for i in range(tokenData.shape[0]): # colour counter
        for j in range(tokenData.shape[1]): # each token
            print(f"({i},{j})\t{tokenData[i][j].shape}, {historicalTokenData[i][j].shape}")

            dataNew, historicalUpdate = averageDataNumpy(tokenData[i][j],historicalTokenData[i][j])

            averagedTokenData[i][j]=dataNew
            historicalTokenData[i][j]=historicalUpdate

    return averagedTokenData, historicalTokenData

def circleUpdate(frame, oldCircleCoords) -> tuple:
    '''
    take in current frame
    finds the new circle, then add it to the previous circle circle coordinates
    averate all
    update circle
    '''

    newCircleCoords = circle.findCircle(frame)
    # print(f"{newCircleCoords=}, {circleCoords=}", flush=True)

    return averageDataList(newCircleCoords, oldCircleCoords)


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
    print(f"Setup Camera, details: {frame_width=}, {frame_height=}, {frame_fps=}")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    if save:
        out = cv2.VideoWriter(f'out/logs/{timestamp}.mp4', fourcc, frame_fps, (frame_width, frame_height))

    cv2.namedWindow("Normal", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Normal", 800, 650)

    cv2.namedWindow("Circle", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Circle", 800, 650)
    # endregion init camera & openCV

    loopIterator = 1
    circleCoords = (616,310, 300) #initial circle estimate
    historicalCircleCoords = [] # colour ID, then token ID, then avg data

    colorNum = 7
    historicalTokenCoords = np.empty((7,7,5,2))
    tokenCoords =  np.empty((7,7,2))

    #region camera loop
    while True:
        ret, frame = cam.read()
        if save: #if the footage is new save it
            out.write(frame) # Save the camera footage

        # Get the positions of the tokens
        circleFrame = circle.cropToCircle(frame, circleCoords)
        colorFrame = color.plotAllColors(circleFrame, tokenCoords)

        if loopIterator%100 == 0 and loopIterator>100:
            circleCoords, historicalCircleCoords = circleUpdate(frame, historicalCircleCoords)
            tokenCoords, historicalTokenCoords = colorUpdate(frame, historicalTokenCoords)

            print(f"{loopIterator}, {circleCoords=}", flush=True)

        color.convertColorListToDict(tokenCoords)

        # Display the captured frame
        cv2.imshow("Normal", frame)
        cv2.imshow("Circle", colorFrame)
        # cv2.imwrite(f"out/logs/CIRCLE_{time.strftime('%Y%m%d-%H%M%S',time.localtime())}.png",circleFrame)

        # Press "q" to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

        loopIterator+=1
        # input(loopIterator)

    # Release the capture and writer objects[694, 294, 210]

    cam.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # mainVideoLoop(videoFilename="out/logs/20241107-154335.mp4", save=False)
    mainVideoLoop(videoFilename="out/logs/20241107-164358.mp4", save=False)
    # mainVideoLoop()