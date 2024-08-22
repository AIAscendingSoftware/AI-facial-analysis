import cv2
import numpy as np
import mediapipe as mp
from deepface import DeepFace
from mediapipe import solutions

class GestureAnalyzer:
    def __init__(self, video_path, target_fps=1): #target_fps=15
        self.video_path = video_path
        self.target_fps = target_fps
        self.frame_count = 0
        self.emotion_confidences ={'happy': [], 'neutral': [], 'surprise': [], 'angry': [], 'fear': [], 'disgust': [], 'sad': []}
        self.smile_count = 0
        self.eye_contact_count = 0
        self.looking_straight_count = 0
        self.hand_usage_count = 0
        self.arms_crossed_count = 0
        self.wrists_closed_count = 0
        self.leg_movement_count = 0
        self.weight_balanced_count = 0
        self.weight_on_one_leg_count = 0
        self.face_confidences = [] #[[0.8773843050003052], [0.9170314073562622], [0.9451085925102234].....]
  
    def analyze_gestures(self):
        video = cv2.VideoCapture(self.video_path)
    
        mp_pose = solutions.pose
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
        mp_face_detection = solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        
        mp_drawing = mp.solutions.drawing_utils
        
        original_fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if int(original_fps) > 15:
            frame_interval = max(1, int(original_fps / self.target_fps))
        else:
            frame_interval = 1
    
        processed_frame_count = 0
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            
            self.frame_count += 1
            if self.frame_count % frame_interval == 0:
                processed_frame_count += 1
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
                # Face detection
                face_results = face_detection.process(image)
                if face_results.detections:
                    for detection in face_results.detections:
                        self.face_confidences.append(detection.score)
                        mp_drawing.draw_detection(image_bgr, detection)
    
                # Emotion analysis
                try:
                    result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                    if isinstance(result, list):
                        result = result[0]
                    emotion = max(result["emotion"], key=result["emotion"].get)
                    cv2.putText(image_bgr, f"Emotion: {emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    for e, conf in result["emotion"].items():
                        if e in self.emotion_confidences:       
                            self.emotion_confidences[e].append(conf)
                except Exception as e:
                    print(f"Error analyzing frame: {e}")
    
                # Pose estimation
                pose_results = pose.process(image)
                if pose_results.pose_landmarks:
                    mp_drawing.draw_landmarks(image_bgr, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = pose_results.pose_landmarks.landmark
                    left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
                    right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
                    nose = landmarks[mp_pose.PoseLandmark.NOSE]
    
                    if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
                        self.eye_contact_count += 1
                        if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
                            self.looking_straight_count += 1
                            cv2.putText(image_bgr, "Looking straight", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
                        self.smile_count += 1
                        cv2.putText(image_bgr, "Smiling", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.5:
                        self.hand_usage_count += 1
                        cv2.putText(image_bgr, "Hand usage", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
                        self.arms_crossed_count += 1
                        cv2.putText(image_bgr, "Arms crossed", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                    if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
                        wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
                        if wrist_distance < 0.1:
                            self.wrists_closed_count += 1
                            cv2.putText(image_bgr, "Wrists closed", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
                    right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
                    if (left_foot.visibility > 0.5 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.5):
                        self.weight_on_one_leg_count += 1
                        cv2.putText(image_bgr, "Weight on one leg", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
                        self.leg_movement_count += 1
                        cv2.putText(image_bgr, "Leg movement", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                    if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
                        self.weight_balanced_count += 1
                        cv2.putText(image_bgr, "Weight balanced", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
                cv2.imshow('Frame', image_bgr)
    
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            
        video.release()
        cv2.destroyAllWindows()
    


    def get_results(self):
        total_frames = self.frame_count

        #to get facial emotion data by averaging them
        emotion_avg_confidences = {emotion: (np.mean(confidences))/10 if confidences else 0 for emotion, confidences in self.emotion_confidences.items()}
        
        # Pre-calculate the division factor
        div_factor = 10 / total_frames if total_frames else 0

        # Body language gestures
        eye_contact_percentage = self.eye_contact_count * div_factor
        avg_face_confidence = (np.mean(self.face_confidences) * 10) if self.face_confidences else 0
        looking_straight_percentage = self.looking_straight_count * div_factor
        smile_percentage = self.smile_count * div_factor
        hand_usage_percentage = self.hand_usage_count * div_factor
        arms_crossed_percentage = self.arms_crossed_count * div_factor
        wrists_closed_percentage = self.wrists_closed_count * div_factor
        weight_on_one_leg_percentage = self.weight_on_one_leg_count * div_factor
        leg_movement_percentage = self.leg_movement_count * div_factor
        weight_balanced_percentage = self.weight_balanced_count * div_factor

        # Arranging the values together, all values are out of 10
        gestures_analysis_data = {
            "happy": round(emotion_avg_confidences['happy'], 2),
            "nautral": round(emotion_avg_confidences['neutral'], 2),
            "surprise": round(emotion_avg_confidences['surprise'], 2),
            "angry": round(emotion_avg_confidences['angry'], 2),
            "fear": round(emotion_avg_confidences['fear'], 2),
            "disgust": round(emotion_avg_confidences['disgust'], 2),
            "sad": round(emotion_avg_confidences['sad'], 2),
            "faceConfidence": round(avg_face_confidence, 2),
            "lookingStraight": round(looking_straight_percentage, 2),
            "smileCount": round(smile_percentage, 2),
            "handUsage": round(hand_usage_percentage, 2),
            "armsCrossed": round(arms_crossed_percentage, 2),
            "wristsClosed": round(wrists_closed_percentage, 2),
            "weightOnOneLeg": round(weight_on_one_leg_percentage, 2),
            "legMovement": round(leg_movement_percentage, 2),
            "weightBalancedOnBothLegs": round(weight_balanced_percentage, 2),
            "eyeContact": round(eye_contact_percentage, 2)
        }

        return gestures_analysis_data


# import cv2, time
# import numpy as np
# from deepface import DeepFace
# from mediapipe import solutions

# class GestureAnalyzer:
#     def __init__(self, video_path):
#         self.video_path = video_path
#         self.frame_count = 0
#         self.emotion_confidences ={'happy': [], 'neutral': [], 'surprise': [], 'angry': [], 'fear': [], 'disgust': [], 'sad': []}
#         self.smile_count = 0
#         self.eye_contact_count = 0
#         self.looking_straight_count = 0
#         self.hand_usage_count = 0
#         self.arms_crossed_count = 0
#         self.wrists_closed_count = 0
#         self.leg_movement_count = 0
#         self.weight_balanced_count = 0
#         self.weight_on_one_leg_count = 0
#         self.face_confidences = [] #[[0.8773843050003052], [0.9170314073562622], [0.9451085925102234].....]
   
#     def analyze_gestures(self):
#         start_time = time.time()
#         video = cv2.VideoCapture(self.video_path) #video: < cv2.VideoCapture 00000230E16ADD90>

#         mp_pose = solutions.pose #mp_pose: <module 'mediapipe.python.solutions.pose' from 'C:\\Users\\ens\\anaconda3\\envs\\AI_facial_analysis_conda_venv\\lib\\site-packages\\mediapipe\\python\\solutions\\pose.py'
#         pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)  #pose: <mediapipe.python.solutions.pose.Pose object at 0x00000230E17D41F0>
   
#         mp_face_detection = solutions.face_detection #mp_face_detection: <module 'mediapipe.python.solutions.face_detection' from 'C:\\Users\\ens\\anaconda3\\envs\\AI_facial_analysis_conda_venv\\lib\\site-packages\\mediapipe\\python\\solutions\\face_detection.py'>
#         face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) #face_detection: <mediapipe.python.solutions.face_detection.FaceDetection object at 0x00000230E17D4310>


#         processed_frame_count=0
#         while video.isOpened():
#             ret, frame = video.read()
#             if not ret:
#                 break
#             processed_frame_count += 1
#             print('processed_frame_count:',processed_frame_count)
#             self.frame_count += 1 #frame is nothing but an image

#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             face_results = face_detection.process(image)

#             if face_results.detections:
                
#                 for detection in face_results.detections:
#                     self.face_confidences.append(detection.score) 
#             try:
#                 result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)

#                 if isinstance(result, list):
#                     result = result[0]

#                 for e, conf in result["emotion"].items():

#                     if e in self.emotion_confidences:
#                         self.emotion_confidences[e].append(conf) #appending the emotion values respect to their key for all frames

#             except Exception as e:
#                 print(f"Error analyzing frame: {e}")

#             pose_results = pose.process(image) #class 'mediapipe.python.solution_base.SolutionOutputs'>, if there is 55 frames,it will bring hfor each of them
#             '''each mp_pose.PoseLandmark.__ has x,y,z and visibility values'''
#             if pose_results.pose_landmarks: 
#                 landmarks = pose_results.pose_landmarks.landmark
#                 left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
#                 right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
#                 nose = landmarks[mp_pose.PoseLandmark.NOSE]

#                 if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
#                     self.eye_contact_count += 1

#                     if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
#                         self.looking_straight_count += 1

#                 if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
#                     self.smile_count += 1

#                 if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.5:
#                     self.hand_usage_count += 1

#                 if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
#                     self.arms_crossed_count += 1

#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
#                 right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
#                 if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
#                     wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
#                     if wrist_distance < 0.1:
#                         self.wrists_closed_count += 1

#                 left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
#                 right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
#                 if (left_foot.visibility > 0.5 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.5):
#                     self.weight_on_one_leg_count += 1

#                 if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
#                     self.leg_movement_count += 1

#                 if left_foot.visibility > 0.5 and right_foot.visibility > 0.5:
#                     self.weight_balanced_count += 1


#         video.release()
#         end_time = time.time()
#         total_time = end_time - start_time
#         fps = self.frame_count / total_time

#         print(f"Total frames processed: {self.frame_count}")
#         print(f"Total time taken: {total_time:.2f} seconds")
#         print(f"Frames per second (FPS): {fps:.2f}")

#     def get_results(self):
#         total_frames = self.frame_count

#         #to get facial emotion data by averaging them
#         emotion_avg_confidences = {emotion: (np.mean(confidences))/10 if confidences else 0 for emotion, confidences in self.emotion_confidences.items()}
        
#         # Pre-calculate the division factor
#         div_factor = 10 / total_frames if total_frames else 0

#         # Body language gestures
#         eye_contact_percentage = self.eye_contact_count * div_factor
#         avg_face_confidence = (np.mean(self.face_confidences) * 10) if self.face_confidences else 0
#         looking_straight_percentage = self.looking_straight_count * div_factor
#         smile_percentage = self.smile_count * div_factor
#         hand_usage_percentage = self.hand_usage_count * div_factor
#         arms_crossed_percentage = self.arms_crossed_count * div_factor
#         wrists_closed_percentage = self.wrists_closed_count * div_factor
#         weight_on_one_leg_percentage = self.weight_on_one_leg_count * div_factor
#         leg_movement_percentage = self.leg_movement_count * div_factor
#         weight_balanced_percentage = self.weight_balanced_count * div_factor

#         # Arranging the values together, all values are out of 10
#         gestures_analysis_data = {
#             "happy": round(emotion_avg_confidences['happy'], 2),
#             "nautral": round(emotion_avg_confidences['neutral'], 2),
#             "surprise": round(emotion_avg_confidences['surprise'], 2),
#             "angry": round(emotion_avg_confidences['angry'], 2),
#             "fear": round(emotion_avg_confidences['fear'], 2),
#             "disgust": round(emotion_avg_confidences['disgust'], 2),
#             "sad": round(emotion_avg_confidences['sad'], 2),
#             "faceConfidence": round(avg_face_confidence, 2),
#             "lookingStraight": round(looking_straight_percentage, 2),
#             "smileCount": round(smile_percentage, 2),
#             "handUsage": round(hand_usage_percentage, 2),
#             "armsCrossed": round(arms_crossed_percentage, 2),
#             "wristsClosed": round(wrists_closed_percentage, 2),
#             "weightOnOneLeg": round(weight_on_one_leg_percentage, 2),
#             "legMovement": round(leg_movement_percentage, 2),
#             "weightBalancedOnBothLegs": round(weight_balanced_percentage, 2),
#             "eyeContact": round(eye_contact_percentage, 2)
#         }

#         return gestures_analysis_data
