import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, mindetectionCon = 0.5):
        self.minDetectionCon = mindetectionCon
        self.mpfaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.facedetection = self.mpfaceDetection.FaceDetection(mindetectionCon)

    def findfaces(self, img, draw= True):
        imgRGB= cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results = self.facedetection.process(imgRGB)
        # img = cv2.resize(img, (1000, 1000))
        # print(self.results)
        bboxs =[]
        if self.results.detections:
            for id , detection , in enumerate (self.results.detections):
                # mpDraw.draw_detection(img , detection)
                # print(id, detection)
                # print(detection.score)
                # print(detection.location_data.relative_bounding_box)
                bboxC = detection.location_data.relative_bounding_box
                ih , iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih),\
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id , bbox, detection.score])
                if draw:
                    img = self.fancyDraw(img, bbox)

                cv2.rectangle(img, bbox, (255, 0, 255), 1)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 255, 0), 2)
        # cv2.imshow("Image", img )
        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5, rt=1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + l), (255, 0, 255), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        return img


def main():
    cap = cv2.VideoCapture("faceDetectionData/test2.mp4")
    ptime = 0
    detector = FaceDetector()
    while True:

        success, img = cap.read()
        img, bboxs = detector.findfaces(img)
        print(bboxs)

        if not success or img is None:
            print("LOL")
            break

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 222, 222), 5)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

