import os
import sys
import time

import cv2
import tensorflow as tf
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource bundled by PyInstaller.
    If running as a PyInstaller-extracted executable, _MEIPASS will be used.
    Otherwise, it will just return the relative path based on this file's directory.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Debugging paths
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
parent_directory = os.path.abspath(os.path.join(base_path, os.pardir))
print(f"Base Path: {base_path}")
print(f"Parent Directory: {parent_directory}")

# Since you've included ui/ml in the spec file, you can reference files as follows:
cascade_path = get_resource_path(os.path.join("ui", "ml", "haarcascade_frontalface_default.xml"))
model_path = get_resource_path(os.path.join("ui", "ml", "model.h5"))

print("Haar Cascade Path:", cascade_path)
print("Model Path:", model_path)

# Ensure files exist before loading
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Haar Cascade file not found: {cascade_path}")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# Load the Haar Cascade
try:
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        raise IOError(f"Failed to load Haar Cascade from {cascade_path}")
except Exception as e:
    print(f"Error loading Haar Cascade: {e}")
    sys.exit(1)

# Load the model
try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

def detect_emotion(frame_p):
    """
    Detects emotion from the preprocessed frame.
    Returns the index of the highest-probability emotion and the confidence.
    """
    emotion = model.predict(tf.expand_dims(frame_p, axis=0), verbose=0)[0]
    idx = np.argmax(emotion)
    conf = np.max(emotion)
    return idx, conf

def preprocess(frame_p):
    """
    Preprocess the frame: Convert to RGB, resize, and normalize.
    """
    frame_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2RGB)
    frame_p = cv2.resize(frame_p, (48, 48))
    frame_p = frame_p / 255.0
    return frame_p

def detect_face(frame_p):
    """
    Detect faces in the frame using the loaded Haar Cascade.
    Returns the grayscale image and the list of detected faces.
    """
    gray = cv2.cvtColor(frame_p, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    return gray, faces

class EmotionDetectionWorker(QThread):
    """
    A QThread that continuously captures frames from the camera,
    detects faces, and estimates emotions.
    """
    result_signal = pyqtSignal(np.ndarray, dict, float)  # (frame, emotions_dict, avg_confidence)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_source = cv2.VideoCapture(0)
        self.video_source.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video_source.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.running = True
        self.class_names = ['Annoyed', 'Happiness', 'Sad', 'Upset']

    def run(self):
        while self.running:
            ret, frame = self.video_source.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (320, 240))
            gray, faces = detect_face(frame)
            emotions = {}
            total_confidence = 0

            for (x, y, w, h) in faces:
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                emotion_label = self.class_names[idx]
                emotions[emotion_label] = emotions.get(emotion_label, 0) + conf
                total_confidence += conf

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                label_position = (x, y - 10) if y > 20 else (x, y + h + 20)
                cv2.putText(
                    frame,
                    emotion_label,
                    label_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )

            avg_confidence = total_confidence / len(faces) if len(faces) > 0 else 0
            self.result_signal.emit(frame, emotions, avg_confidence)

    def stop(self):
        self.running = False
        self.video_source.release()
