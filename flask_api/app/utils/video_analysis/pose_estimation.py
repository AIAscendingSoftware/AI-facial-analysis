import mediapipe as mp
from mediapipe import solutions
import cv2

class PoseEstimator:
    def __init__(self):
        self.mp_pose = solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def estimate_pose(self, image):
        return self.pose.process(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    def draw_landmarks(self, image, pose_results):
        self.mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
