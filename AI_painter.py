import cv2
import numpy as np
import mediapipe as mp
import time
import handTracingModue as htm
import os

#######################
brushThickness = 25
eraserThickness = 100
########################

folderpath = "AI_painter"
myList = os.listdir(folderpath)
print(myList)
overlaylist =[]
for impath in myList:
    image = cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
# print(len(overlaylist))
header= overlaylist[1]

cap =cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector()
imgCanvas = np.zeros((720, 1280, 3), np.uint8)


while True:
    success, img= cap.read()

    img = cv2.flip(img, 1)
    #  find the alndmarks

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw =False)
    xp, yp = 0, 0

    if len(lmList)!= 0:
        # print(lmList)

        x1 , y1 = lmList[8][1:]
        x2, y2  = lmList[12][1:]


    # check which fingers is up

        fingers = detector.fingersup()
        print(fingers)
        #if selection is hold - two fingers are up

        if fingers is not None:
            if fingers[1] and fingers[2] :
                cv2.rectangle(img , (x1, y1-25), (x2, y2+25), (255,0,255), cv2.FILLED)
                print("selection Mode ")
                if y1<125 :
                    if 250 < x1 < 450:
                        header = overlaylist[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:
                        header = overlaylist[1]
                        drawColor = (255, 0, 0)
                    elif 800 < x1 < 950:
                        header = overlaylist[2]
                        drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200:
                        header = overlaylist[3]
                    drawColor = (0, 0, 0)
                    cv2.rectangle(img, (x1, y1 -25), (x2, y2 + 25), drawColor, cv2.FILLED)


            if fingers[1] and fingers[2] == False:
                drawColor = (255, 0, 255)
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing Mode")
                if xp==0 and yp==0:
                    xp, yp = x1, y1
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

                # # Clear Canvas when all fingers are up
                # if all (x >= 1 for x in fingers):
                # imgCanvas = np.zeros((720, 1280, 3), np.uint8)

                # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                # imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
                # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
                # img = cv2.bitwise_and(img, imgInv)
                # img = cv2.bitwise_or(img, imgCanvas)

        # if Drawing Mode - Index finger is up










    #  setting Header images
    if not success or img is None:
        print("Failed to read from camera")
        break
    header_resized = cv2.resize(header, (1280, 131))



    img[0:131, 0:1280]= header_resized
    cv2.imshow("image", img)
    cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)


