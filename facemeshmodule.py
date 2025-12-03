import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, staticMode =False , maxFaces =3 , minDetectionCon =0.5, minTrackCon =0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw =mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh

        self.FaceMesh = self.mpFaceMesh.FaceMesh(
            static_image_mode=self.staticMode,
            max_num_faces=self.maxFaces,
            min_detection_confidence=self.minDetectionCon,
            min_tracking_confidence=self.minTrackCon
        )
        self.DrawSpec = self.mpDraw.DrawingSpec((255,0,255),thickness =1 ,  circle_radius=1)
    def findFaceMesh(self, img,draw= True):
        self.imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results= self.FaceMesh.process(self.imgRGB)

        faces=[]

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img , faceLms, self.mpFaceMesh.FACEMESH_TESSELATION ,self.DrawSpec,self.DrawSpec)
                face =[]
                for id, lm in enumerate(faceLms.landmark):
                    # print (lm)
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    cv2.putText(img, str(id), (x,y), cv2.FONT_HERSHEY_PLAIN, 0.1, (225, 2, 225), 1)

                    # print(id, x, y)
                    face.append([x,y])
                faces.append(face)
        return img, faces



def main():
    cap = cv2.VideoCapture('faceDetectionData/test5.mp4')
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        img ,faces = detector.findFaceMesh(img)
        if len(faces)!=0:
            print(faces[0])
        if not success:
            break
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'{int(fps)}', (20, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (220, 220, 22), 5)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




if __name__ =="__main__":
   main()