import os
import sys
import time
import cv2
import tensorflow as tf
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

def get_resource_path(relative_path):
    """
    Returns the absolute path to the resource.
    If running in a PyInstaller bundle, it uses _MEIPASS.
    Otherwise, it uses the directory of this file.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Determine paths based on environment
if hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller bundle
    cascade_path = get_resource_path("ui/ml/haarcascade_frontalface_default.xml")
    model_path = get_resource_path("ui/ml/model.h5")
else:
    # Running locally (e.g., from PyCharm)
    # emotion_recognition.py is in ui/controllers
    # ml directory is at ui/ml, so go up one directory and then into ml
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
    cascade_path = os.path.join(parent_directory, "ml", "haarcascade_frontalface_default.xml")
    model_path = os.path.join(parent_directory, "ml", "model.h5")

# Debugging paths
print("Cascade Path:", cascade_path)
print("Model Path:", model_path)

# Validate files
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f"Haar Cascade file not found: {cascade_path}")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# Load Haar Cascade
try:
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        raise IOError(f"Failed to load Haar Cascade from {cascade_path}")
except Exception as e:
    print(f"Error loading Haar Cascade: {e}")
    sys.exit(1)

# Load TensorFlow model
try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

def detect_emotion(frame_p):
    """
    Predicts the emotion given a preprocessed face frame.
    """
    try:
        emotion = model.predict(tf.expand_dims(frame_p, axis=0), verbose=0)[0]
        idx = np.argmax(emotion)
        conf = np.max(emotion)
        return idx, conf
    except Exception as e:
        print("Error in detect_emotion:", e)
        return 0, 0.0

def preprocess(frame_p):
    """
    Converts frame to RGB, resizes to (48,48), and normalizes pixel values.
    """
    try:
        frame_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2RGB)
        frame_p = cv2.resize(frame_p, (48, 48))
        frame_p = frame_p / 255.0
        return frame_p
    except Exception as e:
        print("Error in preprocess:", e)
        return np.zeros((48, 48, 3))

def detect_face(frame_p):
    """
    Detects faces in the given frame using the loaded Haar Cascade.
    """
    try:
        gray = cv2.cvtColor(frame_p, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
        return gray, faces
    except Exception as e:
        print("Error in detect_face:", e)
        return frame_p, []

class EmotionDetectionWorker(QThread):
    """
    A QThread that continuously captures frames from the camera,
    detects faces, and estimates emotions.
    """
    result_signal = pyqtSignal(np.ndarray, dict, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_source = cv2.VideoCapture(0)
        self.video_source.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video_source.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.running = True
        self.class_names = ['Annoyed', 'Happiness', 'Sad', 'Upset']

    def run(self):
        while self.running:
            try:
                ret, frame = self.video_source.read()
                if not ret:
                    continue

                # Resize the frame for consistent processing
                frame = cv2.resize(frame, (320, 240))
                gray, faces = detect_face(frame)
                emotions = {}
                total_confidence = 0

                for (x, y, w, h) in faces:
                    # Extract the face region
                    face_roi_gray = gray[y:y+h, x:x+w]
                    # Preprocess the face before detection
                    face_roi_gray = preprocess(face_roi_gray)
                    idx, conf = detect_emotion(face_roi_gray)

                    emotion_label = self.class_names[idx]
                    emotions[emotion_label] = emotions.get(emotion_label, 0) + conf
                    total_confidence += conf

                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
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

                avg_confidence = total_confidence / len(faces) if faces else 0
                self.result_signal.emit(frame, emotions, avg_confidence)

            except Exception as e:
                print("Exception in EmotionDetectionWorker run loop:", e)

    def stop(self):
        self.running = False
        self.video_source.release()
