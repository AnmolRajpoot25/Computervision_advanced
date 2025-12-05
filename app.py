import os
import cv2
import av
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

import handTracingModue as htm  # your existing module

st.set_page_config(page_title="AI Painter – Webcam", page_icon="🎨")

st.title("AI Painter – Hand Gesture Drawing")
st.write("Raise your index finger to draw, use index+middle to change color / eraser.")

BRUSH_THICKNESS = 25
ERASER_THICKNESS = 100
CANVAS_W, CANVAS_H = 1280, 720


class AIPainterProcessor(VideoProcessorBase):
    def __init__(self):
        # --- Header / toolbar images ---
        folderpath = "AI_painter"
        self.overlaylist = []
        if os.path.isdir(folderpath):
            for impath in sorted(os.listdir(folderpath)):
                image = cv2.imread(os.path.join(folderpath, impath))
                if image is not None:
                    self.overlaylist.append(image)

        if self.overlaylist:
            self.header = self.overlaylist[0]
        else:
            # fallback blank header
            self.header = np.zeros((131, CANVAS_W, 3), np.uint8)

        # --- Painter state ---
        self.drawColor = (255, 0, 255)  # default purple
        self.brushThickness = BRUSH_THICKNESS
        self.eraserThickness = ERASER_THICKNESS

        self.detector = htm.handDetector()
        self.imgCanvas = np.zeros((CANVAS_H, CANVAS_W, 3), np.uint8)

        self.xp, self.yp = 0, 0  # previous point

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Get frame as BGR numpy
        img = frame.to_ndarray(format="bgr24")

        # Resize & flip like your original script
        img = cv2.resize(img, (CANVAS_W, CANVAS_H))
        img = cv2.flip(img, 1)

        # Detect hands
        img = self.detector.findHands(img)
        lmList, bbox = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]   # index finger tip
            x2, y2 = lmList[12][1:]  # middle finger tip

            fingers = self.detector.fingersup()

            if fingers:
                # ------- Selection mode: index + middle up -------
                if fingers[1] and fingers[2]:
                    self.xp, self.yp = 0, 0  # reset when changing tool
                    cv2.rectangle(
                        img, (x1, y1 - 25), (x2, y2 + 25),
                        (255, 0, 255), cv2.FILLED
                    )

                    # Top toolbar area
                    if y1 < 125 and self.overlaylist:
                        # adjust these x-ranges to your header layout
                        if 250 < x1 < 450 and len(self.overlaylist) > 0:
                            self.header = self.overlaylist[0]
                            self.drawColor = (255, 0, 255)   # purple
                        elif 550 < x1 < 750 and len(self.overlaylist) > 1:
                            self.header = self.overlaylist[1]
                            self.drawColor = (255, 0, 0)     # blue
                        elif 800 < x1 < 950 and len(self.overlaylist) > 2:
                            self.header = self.overlaylist[2]
                            self.drawColor = (0, 255, 0)     # green
                        elif 1050 < x1 < 1200 and len(self.overlaylist) > 3:
                            self.header = self.overlaylist[3]
                            self.drawColor = (0, 0, 0)       # eraser

                        cv2.rectangle(
                            img, (x1, y1 - 25), (x2, y2 + 25),
                            self.drawColor, cv2.FILLED
                        )

                # ------- Drawing mode: only index up -------
                if fingers[1] and not fingers[2]:
                    cv2.circle(img, (x1, y1), 15, self.drawColor, cv2.FILLED)

                    if self.xp == 0 and self.yp == 0:
                        self.xp, self.yp = x1, y1

                    # Eraser
                    if self.drawColor == (0, 0, 0):
                        cv2.line(
                            img, (self.xp, self.yp), (x1, y1),
                            self.drawColor, self.eraserThickness
                        )
                        cv2.line(
                            self.imgCanvas, (self.xp, self.yp), (x1, y1),
                            self.drawColor, self.eraserThickness
                        )
                    # Normal brush
                    else:
                        cv2.line(
                            img, (self.xp, self.yp), (x1, y1),
                            self.drawColor, self.brushThickness
                        )
                        cv2.line(
                            self.imgCanvas, (self.xp, self.yp), (x1, y1),
                            self.drawColor, self.brushThickness
                        )

                    self.xp, self.yp = x1, y1

        # ---- Merge canvas with camera image ----
        imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, self.imgCanvas)

        # ---- Draw header toolbar on top ----
        if self.header is not None:
            header_resized = cv2.resize(self.header, (CANVAS_W, 131))
            img[0:131, 0:CANVAS_W] = header_resized

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="ai-painter",
    video_processor_factory=AIPainterProcessor,
    media_stream_constraints={"video": True, "audio": False},
)
