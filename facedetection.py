import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture("faceDetectionData/test2.mp4")
ptime =0

mpfaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
facedetection = mpfaceDetection.FaceDetection()

while True :
    success , img = cap.read()
    if not success or img is None:
        print ("LOL")
        break

    imgRGB= cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = facedetection.process(imgRGB)
    # img = cv2.resize(img, (1000, 1000))
    print(results)

    if results.detections:
        for id , detection , in enumerate (results.detections):
            # mpDraw.draw_detection(img , detection)
            # print(id, detection)
            # print(detection.score)
            print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih , iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih),\
            int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 255, 0), 2)
    # cv2.imshow("Image", img )
    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img , f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 222,222), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

