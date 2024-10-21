import cv2
import numpy as np
import mediapipe as mp
from app.static.statistics import emotionalsavg
from app.utils.video_analysis.emotion_analysis import EmotionAnalyzer
from app.utils.video_analysis.face_detection import FaceDetector
from app.utils.video_analysis.pose_estimation import PoseEstimator


class GestureAnalyzer:
    def __init__(self, video_path, target_fps=15): #target_fps=15
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
        #create necessary objects
        self.face_detector = FaceDetector()
        self.emotion_analyzer = EmotionAnalyzer()
        self.pose_estimator = PoseEstimator()

    def analyze_gestures(self):
        video = cv2.VideoCapture(self.video_path)
        original_fps = video.get(cv2.CAP_PROP_FPS)
        frame_interval = max(1, int(original_fps / self.target_fps)) if int(original_fps) > 15 else 1
        processed_frame_count = 0
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        print("total_frames:",total_frames)

        while video.isOpened(): #video analysis has started
            ret, frame = video.read()
            if not ret:
                break
            
            self.frame_count += 1
            if self.frame_count % frame_interval == 0:
                processed_frame_count += 1
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                '''BGR: OpenCV uses BGR format as its default color space. 
                Most pre-trained face detection models provided by 
                OpenCV (such as Haar cascades and DNN models) expect
                the image to be in BGR format for accurate detection.
                '''
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Face detection
                face_results = self.face_detector.detect_faces(image) 
                '''None or empty list: No faces were detected in the frame.'''
                if face_results:
                    '''moving to further analysis if face is detected'''
                    '''face_results: [label_id: 0score: 0.811774731
                        location_data {
                          format: RELATIVE_BOUNDING_BOX
                          relative_bounding_box {
                            xmin: 0.43934235
                            ymin: 0.267300308
                            width: 0.29065153
                            height: 0.516717315
                          }
                          relative_keypoints {
                            x: 0.522203267
                            y: 0.432177067
                          }
                          relative_keypoints {
                            x: 0.642713249
                            y: 0.443909585
                          }
                          relative_keypoints {
                            x: 0.581252396
                            y: 0.564728
                          }
                          relative_keypoints {
                            x: 0.576596856
                            y: 0.659892619
                          }
                          relative_keypoints {
                            x: 0.456542581
                            y: 0.463175416
                          }
                          relative_keypoints {
                            x: 0.702619195
                            y: 0.485643089
                          }
                        }
                        ]
                    '''
                    for detection in face_results:
                        self.face_confidences.append(detection.score)
                        self.face_detector.draw_detection(image_bgr, detection)
                
                    # Emotion analysis
                    try:
                        result = self.emotion_analyzer.analyze_emotion(frame)
                        emotion = max(result["emotion"], key=result["emotion"].get)
                        cv2.putText(image_bgr, f"Emotion: {emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        for e, conf in result["emotion"].items():
                            if e in self.emotion_confidences:       
                                self.emotion_confidences[e].append(conf)
                    except Exception as e:
                        print(f"Error analyzing frame: {e}")


                    # Pose estimation
                    pose_results = self.pose_estimator.estimate_pose(image) #<class 'mediapipe.python.solution_base.SolutionOutputs'>  
                    # print('pose_results:',pose_results)
                    if pose_results.pose_landmarks:
                    
                        self.pose_estimator.draw_landmarks(image_bgr, pose_results) #mp_drawing.draw_landmarks(image_bgr, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        landmarks = pose_results.pose_landmarks.landmark
                        self._analyze_pose_landmarks(landmarks,image_bgr)

                    cv2.imshow('Frame', image_bgr)
    
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()
    
    def _analyze_pose_landmarks(self, landmarks,image_bgr):
        #passed Hand usage is passed
        if landmarks[self.pose_estimator.mp_pose.PoseLandmark.LEFT_WRIST].visibility > 0.7 or landmarks[self.pose_estimator.mp_pose.PoseLandmark.RIGHT_WRIST].visibility > 0.7:
            self.hand_usage_count += 1
            cv2.putText(image_bgr, "Hand usage", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # weight_on_one_leg_count is passed
        left_foot = landmarks[self.pose_estimator.mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot = landmarks[self.pose_estimator.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        if (left_foot.visibility > 0.9 and right_foot.visibility < 0.5) or (left_foot.visibility < 0.5 and right_foot.visibility > 0.9):
            self.weight_on_one_leg_count += 1
            cv2.putText(image_bgr, "Weight on one leg", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        #weight balanced on both leg is passed
        if left_foot.visibility > 0.9 and right_foot.visibility > 0.9:
            self.weight_balanced_count += 1
            cv2.putText(image_bgr, "Weight balanced", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # # wrists_closed is secondary
        # left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        # right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        # if left_wrist.visibility > 0.8 and right_wrist.visibility > 0.8:
        #     wrist_distance = np.sqrt((left_wrist.x - right_wrist.x) ** 2 + (left_wrist.y - right_wrist.y) ** 2)
            
        #     if wrist_distance < 0.1:
        #         print('(left_wrist.x - right_wrist.x) ** 2:',(left_wrist.x - right_wrist.x) ** 2)
        #         print('(left_wrist.y - right_wrist.y) ** 2:', (left_wrist.y - right_wrist.y) ** 2)
        #         print('left_wrist.visibility:',left_wrist.visibility)
        #         print('right_wrist.visibility:',right_wrist.visibility)
        #         print('wrist_distance:',wrist_distance)
        #         self.wrists_closed_count += 1
        #         print('self.wrists_closed_count :', self.wrists_closed_count )
        #         cv2.putText(image_bgr, "Wrists closed", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        #arms_crossed is failed
        # if landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:
        #     print('landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x:',landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x)
        #     print('landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x:', landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x)
        #     print(landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x > landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x)
        #     self.arms_crossed_count += 1
        #     print('self.arms_crossed_count:', self.arms_crossed_count)
        #     cv2.putText(image_bgr, "Arms crossed", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        #eye_contact and looking_straight are failed
        # if left_eye.visibility > 0.5 and right_eye.visibility > 0.5:
        #     self.eye_contact_count += 1
        #     if abs(left_eye.y - right_eye.y) < 0.02 and abs(nose.x - (left_eye.x + right_eye.x) / 2) < 0.02:
        #         self.looking_straight_count += 1
        #         cv2.putText(image_bgr, "Looking straight", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        #smile_count is failed
        # if landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:
        #     print('landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y:',landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y)
        #     print('landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y:',landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y)
        #     print(landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y < landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y)
        #     self.smile_count += 1
        #     print('self.smile_count:',self.smile_count)
        #     cv2.putText(image_bgr, "Smiling", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        # if abs(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y - landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y) > 0.02:
        #     self.leg_movement_count += 1
        #     print('self.leg_movement_count:',self.leg_movement_count)
        #     cv2.putText(image_bgr, "Leg movement", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2

    def get_results(self):
        total_frames = self.frame_count
        emotion_avg_confidences = emotionalsavg(self.emotion_confidences)
        print('emotion_avg_confidences:',emotion_avg_confidences)
        positiveFaceConfidence=(emotion_avg_confidences['happy']+emotion_avg_confidences['surprise']+emotion_avg_confidences['neutral'])/3
        negaticeFaceConfidence=(emotion_avg_confidences['angry']+emotion_avg_confidences['fear']+emotion_avg_confidences['disgust']+emotion_avg_confidences['sad'])/4
        print('positiveFaceConfidence:',positiveFaceConfidence)
        print('negaticeFaceConfidence:',negaticeFaceConfidence)

        # Pre-calculate the division factor
        div_factor = 10 / total_frames if total_frames else 0
        print( round(self.hand_usage_count * div_factor, 2))
        print(round(self.weight_on_one_leg_count * div_factor, 2))
        print(round(self.weight_balanced_count * div_factor, 2))
        print(round((np.mean(self.face_confidences) * 10) if self.face_confidences else 0, 2))
        # Body language gestures
        gestures_analysis_data = {
            "happy": emotion_avg_confidences['happy'],
            "nautral": emotion_avg_confidences['neutral'],
            "surprise": emotion_avg_confidences['surprise'],
            "angry": emotion_avg_confidences['angry'],
            "fear": emotion_avg_confidences['fear'],
            "disgust": emotion_avg_confidences['disgust'],
            "sad": emotion_avg_confidences['sad'],
            #"faceConfidence": round((np.mean(self.face_confidences) * 10) if self.face_confidences else 0, 2), 
            "lookingStraight": round(self.looking_straight_count * div_factor, 2),
            "smileCount": round(self.smile_count * div_factor, 2),
            "handUsage": round(self.hand_usage_count * div_factor, 2),
            "armsCrossed": round(self.arms_crossed_count * div_factor, 2),
            "wristsClosed": round(self.wrists_closed_count * div_factor, 2),
            "weightOnOneLeg": round(self.weight_on_one_leg_count * div_factor, 2),
            "legMovement": round(self.leg_movement_count * div_factor, 2),
            "weightBalancedOnBothLegs": round(self.weight_balanced_count * div_factor, 2),
            "eyeContact": round(self.eye_contact_count * div_factor, 2),
            "positiveFaceConfidence": positiveFaceConfidence,
            "negaticeFaceConfidence":negaticeFaceConfidence
        }
        return gestures_analysis_data