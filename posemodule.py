import cv2
import mediapipe as mp
import time
class posedetector():
    def __init__(self, mode =False  , upBody =False , smooth= True, detectionCon =0.5, trackCon=0.5 ):
        self.mode = mode
        self.upBody = upBody
        self.smooth= smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils





    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img





    def findPosition(self , img, draw = True):
        lmList=[]
        if self.results.pose_landmarks:
            for id , lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                #print(id, lm)
                cx , cy =int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw :
                    cv2.circle(img , (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return lmList



        #
        #
        # # print(results.pose_landmarks)
        #



def main():
    cap = cv2.VideoCapture('posedetectionvideo/test2.mp4')
    ptime = 0
    detector = posedetector()
    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Failed to read frame (end of video or bad frame).")
            break
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw = False)
        if len(lmList) !=0 :
            print(lmList[14])
            cv2.circle(img,(lmList[14][1], lmList[14][2]), 15 , (0,255,255),  7, cv2.FILLED)
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 4, 22), 6)
        cv2.imshow("Image", img)
        cv2.waitKey(1)




if __name__ =="__main__":
    main()

