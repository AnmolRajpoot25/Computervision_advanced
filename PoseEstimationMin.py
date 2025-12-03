import cv2
import mediapipe as mp
import time
mpPose = mp.solutions.pose
pose= mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture('faceDetectionData/test2.mp4')
print("Opened:", cap.isOpened())

ptime =0
while True:
    success, img= cap.read()
    if not success or img is None:
        print("Failed to read frame (end of video or bad frame).")
        break
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img , results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id , lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id, lm)
            cx , cy =int(lm.x*w), int(lm.y*h)
            cv2.circle(img , (cx, cy), 7, (255, 0, 255), cv2.FILLED)

    ctime=time.time()
    fps= 1/(ctime -ptime)
    ptime = ctime

    cv2.putText(img , str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3 , (255,4,22), 6)
    cv2.imshow("Image", img)
    cv2.waitKey(1)



