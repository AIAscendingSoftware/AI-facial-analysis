
# #updated code accelarating GPU 
# import cv2
# import numpy as np
# import tensorflow as tf
# from deepface import DeepFace
# from mediapipe import solutions
# from multiprocessing.pool import ThreadPool

# class GestureAnalyzer:
#     def __init__(self, video_path):
#         self.video_path = video_path
#         self.frame_count = 0
#         self.emotion_counts = {"happy": 0, "neutral": 0, "surprise": 0, "angry": 0, "fear": 0, "disgust": 0, "sad": 0}
#         self.emotion_confidences = {emotion: [] for emotion in self.emotion_counts}
#         self.smile_count = 0
#         self.eye_contact_count = 0
#         self.looking_straight_count = 0
#         self.hand_usage_count = 0
#         self.arms_crossed_count = 0
#         self.wrists_closed_count = 0
#         self.leg_movement_count = 0
#         self.weight_balanced_count = 0
#         self.weight_on_one_leg_count = 0
#         self.face_confidences = []

#     def _process_deepface(self, frame):
#         try:
#             with tf.device('/GPU:0'):  # Specify that operations should run on GPU
#                 result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
#                 if isinstance(result, list):
#                     result = result[0]
#                 emotion = result["dominant_emotion"]
#                 self.emotion_counts[emotion] += 1
#                 for e, conf in result["emotion"].items():
#                     if e in self.emotion_confidences:
#                         self.emotion_confidences[e].append(conf)
#         except Exception as e:
#             print(f"Error analyzing frame with DeepFace: {e}")

#     def _process_mediapipe(self, image, pose, face_detection):
#         face_results = face_detection.process(image)
#         if face_results.detections:
#             for detection in face_results.detections:
#                 self.face_confidences.append(detection.score)

#         pose_results = pose.process(image)
#         if pose_results.pose_landmarks:
#             landmarks = pose_results.pose_landmarks.landmark
#             self._analyze_landmarks(landmarks)

#     def _analyze_landmarks(self, landmarks):
        # mp_pose = solutions.pose

        # left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
        # right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
        # nose = landmarks[mp_pose.PoseLandmark.NOSE]

        # if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
        #     self.eye_contact_count += 1
        #     if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
        #         self.looking_straight_count += 1

        # if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
        #     self.smile_count += 1

        # if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.5:
        #     self.hand_usage_count += 1

        # if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
        #     self.arms_crossed_count += 1

        # left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        # right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        # if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
        #     wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
        #     if wrist_distance < 0.1:
        #         self.wrists_closed_count += 1

        # left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        # right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        # if (left_foot.visibility > 0.5 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.5):
        #     self.weight_on_one_leg_count += 1

        # if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
        #     self.leg_movement_count += 1

        # if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
        #     self.weight_balanced_count += 1

#     def analyze_gestures(self):
#         video = cv2.VideoCapture(self.video_path)
#         mp_pose = solutions.pose
#         pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#         mp_face_detection = solutions.face_detection
#         face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

#         # Use ThreadPool to parallelize frame processing
#         pool = ThreadPool(processes=4)

#         while video.isOpened():
#             ret, frame = video.read()
#             if not ret:
#                 break

#             self.frame_count += 1
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Parallelize DeepFace and MediaPipe processing
#             pool.apply_async(self._process_deepface, (frame,))
#             pool.apply_async(self._process_mediapipe, (image, pose, face_detection))

#         pool.close()
#         pool.join()
#         video.release()

#     def get_results(self):
#         total_frames = self.frame_count
#         emotion_percentages = {emotion: count / total_frames * 100 for emotion, count in self.emotion_counts.items()}
#         emotion_avg_confidences = {emotion: np.mean(confidences) if confidences else 0 for emotion, confidences in self.emotion_confidences.items()}
#         eye_contact_percentage = self.eye_contact_count / total_frames * 100

#         avg_face_confidence = np.mean(self.face_confidences) if self.face_confidences else 0
#         looking_straight_percentage = self.looking_straight_count / total_frames * 100
#         smile_percentage = self.smile_count / total_frames * 100
#         hand_usage_percentage = self.hand_usage_count / total_frames * 100
#         arms_crossed_percentage = self.arms_crossed_count / total_frames * 100
#         wrists_closed_percentage = self.wrists_closed_count / total_frames * 100
#         weight_on_one_leg_percentage = self.weight_on_one_leg_count / total_frames * 100
#         leg_movement_percentage = self.leg_movement_count / total_frames * 100
#         weight_balanced_percentage = self.weight_balanced_count / total_frames * 100

#         fixed_keys = ["happy", "nautral", "surprise", "angry", "fear", "disgust", "sad"]
#         emotion_percentage_data = {emotion: emotion_percentages.get(emotion, 0.0) for emotion in fixed_keys}
        
#         additional_data = {
#             "faceConfidence":  float(f"{avg_face_confidence:.2f}"),
#             "lookingStraight":  float(f"{looking_straight_percentage:.2f}"),
#             "smileCount":  float(f"{smile_percentage:.2f}"),
#             "handUsage":float(f"{hand_usage_percentage :.2f}"),
#             "armsCrossed": float(f"{arms_crossed_percentage:.2f}"),
#             "wristsClosed":  float(f"{wrists_closed_percentage:.2f}"),
#             "weightOnOneLeg": float(f"{weight_on_one_leg_percentage:.2f}"),
#             "legMovement":  float(f"{leg_movement_percentage:.2f}"),
#             "weightBalancedOnBothLegs":  float(f"{weight_balanced_percentage:.2f}"),
#             "eyeContact":float(f"{eye_contact_percentage:.2f}")
#         }

#         emotion_percentage_data.update(additional_data)
#         return emotion_percentage_data

import cv2
import numpy as np
import tensorflow as tf
from deepface import DeepFace
from mediapipe import solutions
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

class GestureAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.frame_count = 0
        self.analyzed_frame_count = 0
        self.skipped_frame_count = 0
        self.emotion_counts = defaultdict(int)
        self.emotion_confidences = defaultdict(list)
        self.smile_count = 0
        self.eye_contact_count = 0
        self.looking_straight_count = 0
        self.hand_usage_count = 0
        self.arms_crossed_count = 0
        self.wrists_closed_count = 0
        self.leg_movement_count = 0
        self.weight_balanced_count = 0
        self.weight_on_one_leg_count = 0
        self.face_confidences = []

        # Initialize TensorFlow GPU configuration
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(f"Error configuring GPU: {e}")

    def _process_deepface(self, frame):
        try:
            with tf.device('/GPU:0'):
                result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False, detector_backend="opencv")
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                    emotion = result["dominant_emotion"]
                    self.emotion_counts[emotion] += 1
                    for e, conf in result["emotion"].items():
                        self.emotion_confidences[e].append(conf)
                    self.analyzed_frame_count += 1
                    return result
                else:
                    self.skipped_frame_count += 1
                    return None
        except Exception as e:
            self.skipped_frame_count += 1
            return None

    def _process_mediapipe(self, image, pose, face_detection):
        face_results = face_detection.process(image)
        if face_results.detections:
            for detection in face_results.detections:
                self.face_confidences.append(detection.score[0])

        pose_results = pose.process(image)
        if pose_results.pose_landmarks:
            self._analyze_landmarks(pose_results.pose_landmarks.landmark)
            return True
        return False

    def _analyze_landmarks(self, landmarks):
        mp_pose = solutions.pose.PoseLandmark

        left_eye, right_eye, nose = landmarks[mp_pose.LEFT_EYE], landmarks[mp_pose.RIGHT_EYE], landmarks[mp_pose.NOSE]

        if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
            self.eye_contact_count += 1
            if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
                self.looking_straight_count += 1

        if landmarks[mp_pose.MOUTH_LEFT].y < landmarks[mp_pose.MOUTH_RIGHT].y:
            self.smile_count += 1

        if landmarks[mp_pose.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.RIGHT_WRIST].visibility > 0.5:
            self.hand_usage_count += 1

        if landmarks[mp_pose.LEFT_WRIST].x > landmarks[mp_pose.RIGHT_WRIST].x:
            self.arms_crossed_count += 1

        left_wrist, right_wrist = landmarks[mp_pose.LEFT_WRIST], landmarks[mp_pose.RIGHT_WRIST]
        if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
            wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
            if wrist_distance < 0.1:
                self.wrists_closed_count += 1

        left_foot, right_foot = landmarks[mp_pose.LEFT_FOOT_INDEX], landmarks[mp_pose.RIGHT_FOOT_INDEX]
        if (left_foot.visibility > 0.5) != (right_foot.visibility > 0.5):
            self.weight_on_one_leg_count += 1

        if abs(landmarks[mp_pose.LEFT_KNEE].y - landmarks[mp_pose.RIGHT_KNEE].y) > 0.02:
            self.leg_movement_count += 1

        if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
            self.weight_balanced_count += 1

    def analyze_gestures(self):
        video = cv2.VideoCapture(self.video_path)
        mp_pose = solutions.pose
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_face_detection = solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

        with ThreadPoolExecutor(max_workers=8) as executor:
            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break

                self.frame_count += 1
                
                # Process frame with DeepFace
                executor.submit(self._process_deepface, frame)
                
                # Process frame with MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self._process_mediapipe(rgb_frame, pose, face_detection):
                    self.analyzed_frame_count += 1
                else:
                    self.skipped_frame_count += 1

        video.release()

    def get_results(self):
        total_frames = max(1, self.analyzed_frame_count)  # Use analyzed frames count
        emotion_percentages = {emotion: count / total_frames * 100 for emotion, count in self.emotion_counts.items()}
        emotion_avg_confidences = {emotion: np.mean(confidences) if confidences else 0 for emotion, confidences in self.emotion_confidences.items()}

        fixed_keys = ["happy", "nautral", "surprise", "angry", "fear", "disgust", "sad"]
        emotion_percentage_data = {emotion: emotion_percentages.get(emotion, 0.0) for emotion in fixed_keys}
        
        additional_data = {
            "faceConfidence": float(f"{np.mean(self.face_confidences) if self.face_confidences else 0:.2f}"),
            "lookingStraight": float(f"{self.looking_straight_count / total_frames * 100:.2f}"),
            "smileCount": float(f"{self.smile_count / total_frames * 100:.2f}"),
            "handUsage": float(f"{self.hand_usage_count / total_frames * 100:.2f}"),
            "armsCrossed": float(f"{self.arms_crossed_count / total_frames * 100:.2f}"),
            "wristsClosed": float(f"{self.wrists_closed_count / total_frames * 100:.2f}"),
            "weightOnOneLeg": float(f"{self.weight_on_one_leg_count / total_frames * 100:.2f}"),
            "legMovement": float(f"{self.leg_movement_count / total_frames * 100:.2f}"),
            "weightBalancedOnBothLegs": float(f"{self.weight_balanced_count / total_frames * 100:.2f}"),
            "eyeContact": float(f"{self.eye_contact_count / total_frames * 100:.2f}")
        }

        emotion_percentage_data.update(additional_data)
        
        # Add frame processing summary
        emotion_percentage_data.update({
            "totalFrames": self.frame_count,
            "analyzedFrames": self.analyzed_frame_count,
            "skippedFrames": self.skipped_frame_count,
            "analyzedPercentage": float(f"{self.analyzed_frame_count / self.frame_count * 100:.2f}")
        })

        return emotion_percentage_data

