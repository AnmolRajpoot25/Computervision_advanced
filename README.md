**ComputerVision Advanced**

This repository is a collection of modular and real-time Computer Vision pipelines built using OpenCV, MediaPipe, and Python.
The scripts demonstrate practical implementations of hand-tracking, pose-estimation, face-mesh extraction, landmark-based gesture recognition, and system-control applications using image-processing algorithms. 
Each component is designed to be lightweight, easily readable, and reusable in other projects.

**Features**

The repository covers a wide range of vision tasks including multi-hand landmark extraction, 2D body-pose estimation, facial feature mapping, gesture-controlled interfaces, and AI-assisted motion tracking. These scripts also highlight concepts such as pixel-wise drawing, frame differencing, distance-based feature engineering, bounding-box generation, and landmark-vector processing.
Each file is written as an independent experiment, making it easy to run any demo directly without complex configuration.

Repository Structure
AI_Trainer.py

Implements an exercise-tracking system using MediaPipe Pose. The script computes angles between joints, monitors body alignment, counts repetitions, and delivers feedback in real time. It demonstrates pose-vector interpretation and kinematic-pattern analysis.

HandtracingMin.py

A minimal hand-tracking demo that detects palms, returns 21 landmarks per frame, and overlays them using OpenCV drawing utilities. It introduces landmark indexing, coordinate extraction, and gesture-trigger logic.

handTracingModue.py

A fully-modular hand-tracking class that encapsulates initialization, detection, landmark extraction, handedness estimation, and distance calculations. This module is designed for reuse across all gesture-driven scripts.

PoseEstimationMin.py

A concise implementation that detects and draws skeletal connections. It demonstrates how to extract raw pose-landmark tensors and process them for tasks like posture analysis or motion classification.

posemodule.py

A wrapper module for pose estimation that abstracts MediaPipe’s complex graph-processing pipeline. It exposes functions to locate joints, retrieve pixel coordinates, compute geometric angles, and support downstream analytics such as rep-counting.

VolumHandControl.py

A gesture-based system-volume controller that uses the distance between thumb and index finger to map hand motion to volume levels. It integrates pycaw, normalizes distances to a defined range, and applies smoothing to prevent jitter.

facedetection.py

Runs face-detection using Haar cascades or MediaPipe’s lightweight models. It identifies facial regions, draws bounding boxes, and shows concepts like scale-factor tuning, non-max suppression, and image-pyramid operations.

facedetectionModule.py

A face-detection abstraction that wraps initialization, detection thresholds, box extraction, and optional confidence scoring. This enables plug-and-play integration into any script requiring face-based triggers or filters.

facemesh.py

Extracts dense facial landmarks (approx. 468 points) using MediaPipe FaceMesh. It demonstrates mesh rendering, contour highlighting, landmark-region segmentation, and advanced applications like face-driven AR effects.

facemeshmodule.py

A reusable face-mesh module providing functions to obtain mesh indices, convert normalized coordinates to pixel positions, compute facial vectors, and support tasks such as eye-blink detection or head-movement analysis.

fingercounter.py

A finger-counting system using geometry-based analysis of landmark positions. It checks finger-tip coordinates relative to joint lines to determine which fingers are raised, enabling gesture-based numeric input in real time.

ImageDetection_count_fingers/

Contains images used for testing finger-counting logic without a live webcam. Useful for validating static landmark predictions and testing the pipeline under controlled conditions.

faceDetectionData/

Stores model files such as Haar cascade XML classifiers or supporting detection datasets required for face-localization modules.

posedetectionvideo/

Contains example videos for pose-analysis experiments. These are helpful for debugging frame-by-frame joint detection, angle calculations, and skeleton-tracking consistency.

.idea/

PyCharm project settings including interpreter paths, virtual-environment mappings, and project-level metadata.


Getting Started

Install all required dependencies:

pip install opencv-python mediapipe numpy


For audio-control scripts on Windows:

pip install pycaw comtypes


Run any file directly:

python fingercounter.py
python VolumHandControl.py
python facemesh.py


Ensure your webcam is enabled, as most modules process real-time video streams.
