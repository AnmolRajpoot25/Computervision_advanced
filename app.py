import av
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import streamlit as st

st.set_page_config(page_title="Webcam Demo", page_icon="📷")

st.title("Webcam Test on Streamlit")
st.write("Allow camera access in the browser to see the live feed.")

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        # Convert the incoming frame to numpy array (BGR)
        img = frame.to_ndarray(format="bgr24")

        #  Put your OpenCV / MediaPipe logic here
        # Example: draw a simple rectangle
        h, w, _ = img.shape
        cv2.rectangle(img, (int(w*0.3), int(h*0.3)), (int(w*0.7), int(h*0.7)), (255, 255, 255), 2)

        # Return processed frame
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
)
## streamlit run app.py to run locally

