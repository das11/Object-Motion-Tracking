import cv2
import numpy as np
import math
import copy

# parameters
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 90  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 70
learningRate = 0

# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


# Fetching BG from frame after MOG
def fetch_bgMask(frame, fgMask):

    res_bgMask = cv2.bitwise_xor(frame, fgMask)
    return res_bgMask

# Remove BG
def removeBG(frame):

    fgmask = bgModel.apply(frame,learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)

    res = cv2.bitwise_and(frame, frame, mask=fgmask)

    # print("camera 2: " + str(frame.shape ))
    # print("fg mask after BG MODEL : " + str(fgmask.shape))
    return res

# camera 
camera = cv2.VideoCapture(0)
camera.set(10, 200)
cv2.namedWindow("Tracker")
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)

# global scope
buffer = None


while camera.isOpened():
    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    cv2.imshow('camera', frame)

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        img = removeBG(frame)

        # if(buffer != None):
        #     diff = cv2.absdiff(buffer, frame)
        #     diif = diff.astype(np.uint8)

        #     percentage = (((np.count_nonzero(diff))/5) * 100)/ diff.size
        #     print(percentage)

        #     buffer = frame


        bgmask = fetch_bgMask(frame, img)

        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI

        cv2.imshow('mask', img)
        cv2.imshow("bgmask", bgmask)

        # convert the image into BW image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)

        # print((adapter.estimate_intensity(gray))[0])
        cv2.imshow('blur', blur)

        buffer = frame

    # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        # cv2.imshow("bgMask", bgModel)
        isBgCaptured = 1
        print( '!!!Background Captured!!!')

        i1 = cv2.imread("/Users/Interface/Coding 2/CV/motion_detection/i1.png")
        i2 = cv2.imread("/Users/Interface/Coding 2/CV/motion_detection/i2.png")

        diff = cv2.absdiff(i1, i2)
        diff = diff.astype(np.uint8)
        percentage = ((np.count_nonzero(diff)) * 100)/diff.size
        print(percentage)


    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')
    elif k == ord('n'):
        triggerSwitch = True
        print ('!!!Trigger On!!!')

