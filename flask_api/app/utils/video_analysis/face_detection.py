import cv2
from mediapipe import solutions

class FaceDetector:
    def __init__(self):
        self.mp_face_detection = solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.mp_drawing = solutions.drawing_utils

    def detect_faces(self, image):
        return self.face_detection.process(cv2.cvtColor(image, cv2.COLOR_RGB2BGR)).detections

    def draw_detection(self, image, detection):
        self.mp_drawing.draw_detection(image, detection)
