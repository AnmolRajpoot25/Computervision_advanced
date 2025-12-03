import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture('faceDetectionData/test1.mp4')
pTime =0
mpDraw =mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
FaceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)
DrawSpec = mpDraw.DrawingSpec((255,0,255),thickness =1 ,  circle_radius=1)


while True:
    success, img = cap.read()
    if not success:
        break
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results= FaceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img , faceLms, mpFaceMesh.FACEMESH_TESSELATION ,DrawSpec,DrawSpec)
            for lm in faceLms.landmark:
                print (lm)
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                print(id, x, y)


    cTime = time.time()
    fps = 1/(cTime -pTime)
    pTime = cTime
    cv2.putText(img , f'{int(fps)}', (20,100),cv2.FONT_HERSHEY_COMPLEX,3, (220,220,22), 5  )

    cv2.imshow("Image " , img )
    cv2.waitKey(1)

