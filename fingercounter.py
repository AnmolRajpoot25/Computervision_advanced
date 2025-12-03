import cv2
import numpy as np
import handTracingModue as htm

cap = cv2.VideoCapture()
while True:
    success , img = cap.read()
    if not success :
        print("LOL")
        break
cv2.imshow('image', img)
cv2.waitKey(1)
