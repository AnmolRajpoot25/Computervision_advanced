import cv2
import numpy as np
import mediapipe as mp
import time
import posemodule as pm
cap = cv2.VideoCapture("posedetectionvideo/test1.mp4")


detector = pm.posedetector()
count =0
dir =0
ptime =0
while True:
    success, img =cap.read()
    # img = cv2.imread("posedetectionvideo/test2.png")
    img = cv2.resize(img, (720, 720))
    img= detector.findPose(img)
    lmList = detector.findPosition(img, False)
    if len(lmList)!= 0:
        angle= detector.findAngle(img, 11,13,15)
        per = np.interp(angle, (210, 310),(0 ,100))
        bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle)



        # check for the dumbell curl
        color = (255, 0, 255)
        if per >=55:
            color = (0, 255, 255)
            if dir<=10:
                count += 0.5
                dir =1
        if per ==0 :
            color = (255, 255, 0)
            if dir == 1:
                count+=0.5
                dir =0
        print(count)
        # Draw Bar
        cv2.rectangle(img, (50, 100), (125, 650), color, 3)
        cv2.rectangle(img, (50, int(bar)), (125, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (130, 675), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
        # Draw Curl Count
        cv2.rectangle(img, (570, 450), (770, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (600, 650), cv2.FONT_HERSHEY_PLAIN, 9,
                    (255, 0, 0), 20)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 4, 22), 6)



    cv2.imshow("Image", img)
    cv2.waitKey(1)

