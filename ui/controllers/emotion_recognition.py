import os
import time

import cv2
import tensorflow as tf
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the absolute path to the Haar Cascade file
cascade_path = os.path.join(script_dir, '..', 'ml', 'haarcascade_frontalface_default.xml')

# Load the cascade
cascade = cv2.CascadeClassifier(cascade_path)

# Check if the cascade was loaded correctly
if cascade.empty():
    raise IOError(f"Failed to load Haar Cascade from {cascade_path}")

# Load the model
model = tf.keras.models.load_model("/Users/alizargari/PycharmProjects/SocialSync/ui/ml/model.h5")

def detect_emotion(frame_p):
    emotion = model.predict(tf.expand_dims(frame_p, axis=0), verbose=0)
    emotion = emotion[0]  # Get the first (and only) element
    num = np.max(emotion)
    idx = np.argmax(emotion)
    return idx, num

def preprocess(frame_p):
    frame_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2RGB)
    frame_p = cv2.resize(frame_p, (48, 48))
    frame_p = frame_p / 255.0
    return frame_p

def detect_face(frame_p):
    gray = cv2.cvtColor(frame_p, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    return gray, faces

class EmotionDetectionWorker(QThread):
    result_signal = pyqtSignal(np.ndarray, dict, float)  # Frame, emotions, confidence

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_source = cv2.VideoCapture(0)  # Use the default camera
        self.video_source.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video_source.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.running = True
        # Load your model and class names
        self.model = model
        self.class_names = ['Annoyed', 'Happiness', 'Sad', 'Upset']

    def run(self):
        while self.running:
            ret, frame = self.video_source.read()
            if not ret:
                continue

            # Downscale the frame before processing
            frame = cv2.resize(frame, (320, 240))

            gray, faces = detect_face(frame)
            emotions = {}
            total_confidence = 0

            # Process each detected face
            for (x, y, w, h) in faces:
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                # Get the emotion label based on the detected index
                emotion_label = self.class_names[idx]
                emotions[emotion_label] = emotions.get(emotion_label, 0) + conf
                total_confidence += conf

                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

                # Display the emotion label on the bounding box
                label_position = (x, y - 10) if y > 20 else (x, y + h + 20)
                cv2.putText(
                    frame,
                    emotion_label,
                    label_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,  # Font scale
                    (0, 255, 0),  # Green color
                    1,  # Thickness
                    cv2.LINE_AA,
                )

            avg_confidence = total_confidence / len(faces) if len(faces) > 0 else 0

            # Emit the processed frame and emotion data back to main thread
            self.result_signal.emit(frame, emotions, avg_confidence)

    def stop(self):
        self.running = False
        self.video_source.release()
