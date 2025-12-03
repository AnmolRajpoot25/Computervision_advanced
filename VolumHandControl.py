import cv2
import mediapipe as mp
import numpy as np
import time
import handTracingModue as htm
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
###########################################

Wcam , hcam = 640, 480
###########################################
cap = cv2.VideoCapture(0)
cap.set(3, Wcam)
cap.set(4, hcam)
ptime =0
detector = htm.handDetector(detectionCon=0.8)


devices = AudioUtilities.GetSpeakers()

# In the new pycaw versions, use EndpointVolume directly
volume = devices.EndpointVolume

volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 100
volPer = 0

while True:
     success, img = cap.read()
     img =detector.findHands(img)
     lmList  = detector.findPosition(img, draw = False)
     if len(lmList)!=0 :
          print(lmList[4],  lmList[8])
          x1, y1 = lmList[4][1] , lmList[4][2]
          x2, y2 = lmList[8][1] , lmList[8][2]
          cx , cy = (x1+x2)//2 , (y1+y2)//2

          cv2.circle(img, (x1, y1 ), 10,(255,0,255),cv2.FILLED)
          cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
          cv2.line(img, (x1, y1), (x2, y2 ), (255,0,255),3 )
          cv2.circle(img, ((x1+ x2)//2, (y1+y2)//2 ), 10,(255,0,255),cv2.FILLED)
          length = math.hypot(x2-x1, y2-y1)
          print(length)
          # Hand range = 50 -  300
          # volume range -65 - 0

          vol =np.interp(length, [50, 300], [minVol, maxVol])
          volBar = np.interp(length, [50, 300], [400, 150])
          volPer = np.interp(length, [50, 300], [0, 100])
          print(int(length), vol)
          volume.SetMasterVolumeLevel(vol, None)

          if length < 50:
               cv2.circle(img, (cx, cy), 10, (0,255,0),cv2.FILLED)


     if not success:
         break
     cv2.rectangle(img, (50, 70), (85, 100), (255, 0, 255), 3)
     cv2.rectangle(img, (50, int(volBar)), (85, 100), (0, 255,0), cv2.FILLED)
     cv2.putText(img, f'{int(volPer)} %', (50, 430),
                 cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

     ctime = time.time()
     fps = 1/(ctime -ptime)
     ptime =ctime
     cv2.putText(img , f"{int(fps)}", (70, 40),cv2.FONT_HERSHEY_PLAIN, 4, (0,222,0), 4)
     cv2.imshow("video", img)
     cv2.waitKey(1)
