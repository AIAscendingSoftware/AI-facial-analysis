# # #STAGE 1
# # #updated code accelarating GPU 
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
#         mp_pose = solutions.pose

#         left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
#         right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
#         nose = landmarks[mp_pose.PoseLandmark.NOSE]

#         if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
#             self.eye_contact_count += 1
#             if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
#                 self.looking_straight_count += 1

#         if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
#             self.smile_count += 1

#         if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.5:
#             self.hand_usage_count += 1

#         if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
#             self.arms_crossed_count += 1

#         left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
#         right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
#         if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
#             wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
#             if wrist_distance < 0.1:
#                 self.wrists_closed_count += 1

#         left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
#         right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
#         if (left_foot.visibility > 0.5 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.5):
#             self.weight_on_one_leg_count += 1

#         if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
#             self.leg_movement_count += 1

#         if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
#             self.weight_balanced_count += 1

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



##stage 3
import cv2
import numpy as np
import tensorflow as tf
from deepface import DeepFace
from mediapipe import solutions
from concurrent.futures import ThreadPoolExecutor

class GestureAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.frame_count = 0
        self.emotion_counts = {"happy": 0, "neutral": 0, "surprise": 0, "angry": 0, "fear": 0, "disgust": 0, "sad": 0}
        self.emotion_confidences = {emotion: [] for emotion in self.emotion_counts}
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
        self.skip_frames = 2  # Process every second frame

    def _process_deepface(self, frame):
        try:
            with tf.device('/GPU:0'):
                result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                if isinstance(result, list):
                    result = result[0]
                emotion = result["dominant_emotion"]
                self.emotion_counts[emotion] += 1
                for e, conf in result["emotion"].items():
                    if e in self.emotion_confidences:
                        self.emotion_confidences[e].append(conf)
        except Exception as e:
            print(f"Error analyzing frame with DeepFace: {e}")

    def _process_mediapipe(self, image, pose, face_detection):
        face_results = face_detection.process(image)
        if face_results.detections:
            for detection in face_results.detections:
                self.face_confidences.append(detection.score)

        pose_results = pose.process(image)
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            self._analyze_landmarks(landmarks)

    def _analyze_landmarks(self, landmarks):
        mp_pose = solutions.pose

        left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]

        if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
            self.eye_contact_count += 1
            if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
                self.looking_straight_count += 1

        if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
            self.smile_count += 1

        if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.5:
            self.hand_usage_count += 1

        if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
            self.arms_crossed_count += 1

        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
            wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
            if wrist_distance < 0.1:
                self.wrists_closed_count += 1

        left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        if (left_foot.visibility > 0.5 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.5):
            self.weight_on_one_leg_count += 1

        if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
            self.leg_movement_count += 1

        if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
            self.weight_balanced_count += 1

    def analyze_gestures(self):
        video = cv2.VideoCapture(self.video_path)
        mp_pose = solutions.pose
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_face_detection = solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

        with ThreadPoolExecutor(max_workers=4) as executor:
            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break

                self.frame_count += 1
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process MediaPipe for the current frame
                executor.submit(self._process_mediapipe, image, pose, face_detection)

                # Process DeepFace only for selected frames
                if self.frame_count % self.skip_frames == 0:
                    executor.submit(self._process_deepface, frame)

        video.release()

    def get_results(self):
        total_frames = self.frame_count
        emotion_percentages = {emotion: count / total_frames * 100 for emotion, count in self.emotion_counts.items()}
        emotion_avg_confidences = {emotion: np.mean(confidences) if confidences else 0 for emotion, confidences in self.emotion_confidences.items()}
        eye_contact_percentage = self.eye_contact_count / total_frames * 100 if total_frames > 0 else 0

        avg_face_confidence = np.mean(self.face_confidences) if self.face_confidences else 0
        looking_straight_percentage = self.looking_straight_count / total_frames * 100 if total_frames > 0 else 0
        smile_percentage = self.smile_count / total_frames * 100 if total_frames > 0 else 0
        hand_usage_percentage = self.hand_usage_count / total_frames * 100 if total_frames > 0 else 0
        arms_crossed_percentage = self.arms_crossed_count / total_frames * 100 if total_frames > 0 else 0
        wrists_closed_percentage = self.wrists_closed_count / total_frames * 100 if total_frames > 0 else 0
        weight_on_one_leg_percentage = self.weight_on_one_leg_count / total_frames * 100 if total_frames > 0 else 0
        leg_movement_percentage = self.leg_movement_count / total_frames * 100 if total_frames > 0 else 0
        weight_balanced_percentage = self.weight_balanced_count / total_frames * 100 if total_frames > 0 else 0

        fixed_keys = ["happy", "neutral", "surprise", "angry", "fear", "disgust", "sad"]
        emotion_percentage_data = {emotion: emotion_percentages.get(emotion, 0.0) for emotion in fixed_keys}
        
        additional_data = {
            "faceConfidence": float(f"{avg_face_confidence:.2f}"),
            "lookingStraight": float(f"{looking_straight_percentage:.2f}"),
            "smileCount": float(f"{smile_percentage:.2f}"),
            "handUsage": float(f"{hand_usage_percentage:.2f}"),
            "armsCrossed": float(f"{arms_crossed_percentage:.2f}"),
            "wristsClosed": float(f"{wrists_closed_percentage:.2f}"),
            "weightOnOneLeg": float(f"{weight_on_one_leg_percentage:.2f}"),
            "legMovement": float(f"{leg_movement_percentage:.2f}"),
            "weightBalancedOnBothLegs": float(f"{weight_balanced_percentage:.2f}"),
            "eyeContact": float(f"{eye_contact_percentage:.2f}")
        }

        emotion_percentage_data.update(additional_data)
        return emotion_percentage_data
