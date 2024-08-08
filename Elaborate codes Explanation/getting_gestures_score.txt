

import cv2, time
import numpy as np
from deepface import DeepFace
from mediapipe import solutions
import datetime




class GestureAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.frame_count = 0
        self.emotion_counts = {"happy": 0, "neutral": 0, "surprise": 0, "angry": 0, "fear": 0, "disgust": 0, "sad": 0}
        self.emotion_confidences = {emotion: [] for emotion in self.emotion_counts}
        """self.emotion_confidences = {'happy': [], 'neutral': [], 'surprise': [], 'angry': [], 'fear': [], 'disgust': [], 'sad': []}"""
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
        start_time = time.time()
        video = cv2.VideoCapture(self.video_path) #video: < cv2.VideoCapture 00000230E16ADD90>

        mp_pose = solutions.pose #mp_pose: <module 'mediapipe.python.solutions.pose' from 'C:\\Users\\ens\\anaconda3\\envs\\AI_facial_analysis_conda_venv\\lib\\site-packages\\mediapipe\\python\\solutions\\pose.py'
        pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)  #pose: <mediapipe.python.solutions.pose.Pose object at 0x00000230E17D41F0>
   
        mp_face_detection = solutions.face_detection #mp_face_detection: <module 'mediapipe.python.solutions.face_detection' from 'C:\\Users\\ens\\anaconda3\\envs\\AI_facial_analysis_conda_venv\\lib\\site-packages\\mediapipe\\python\\solutions\\face_detection.py'>
        face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) #face_detection: <mediapipe.python.solutions.face_detection.FaceDetection object at 0x00000230E17D4310>



        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            self.frame_count += 1 #frame is nothing but an image

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_results = face_detection.process(image)

            if face_results.detections:
                
                for detection in face_results.detections:
                    #print('face_results.detections:', face_results.detections, 'detection.score:',detection.score)
                    '''print('face_results.detections:', face_results.detections, 'detection.score:',detection.score)
                    face_results.detections: [label_id: 0
                    score: 0.9433943629264832
                    location_data {
                      format: RELATIVE_BOUNDING_BOX
                      relative_bounding_box {
                        xmin: 0.48066356778144836
                        ymin: 0.2638506293296814
                        width: 0.2872790992259979
                        height: 0.5106983184814453
                      }
                      relative_keypoints {
                        x: 0.570661187171936
                        y: 0.43193602561950684
                      }
                      relative_keypoints {
                        x: 0.6749114394187927
                        y: 0.4601208567619324
                      }
                      relative_keypoints {
                        x: 0.6266758441925049
                        y: 0.5856029987335205
                      }
                      relative_keypoints {
                        x: 0.6149242520332336
                        y: 0.6612463593482971
                      }
                      relative_keypoints {
                        x: 0.491730272769928
                        y: 0.42612528800964355
                      }
                      relative_keypoints {
                        x: 0.7110611796379089
                        y: 0.4770684838294983
                      }
                    }
                    ] detection.score: [0.9433943629264832]
                    
                    Keypoint 1: Right Eye
                    Position: Near the center of the right eye.
                    Purpose: Helps in tracking eye movement and orientation.

                    Keypoint 2: Left Eye
                    Position: Near the center of the left eye.
                    Purpose: Similarly, helps in tracking eye movement and orientation.
                    
                    Keypoint 3: Nose Tip
                    Position: At the tip of the nose.
                    Purpose: Important for recognizing facial expressions and orientation.
                    
                    Keypoint 4: Right Mouth Corner
                    Position: At the corner of the right side of the mouth.
                    Purpose: Used for analyzing mouth movement and expressions.
                    
                    Keypoint 5: Left Mouth Corner
                    Position: At the corner of the left side of the mouth.
                    Purpose: Similarly helps in analyzing mouth movement and expressions.
                    
                    Keypoint 6: Chin
                    Position: Near the bottom of the chin.
                    Purpose: Helps in determining the overall face orientation and size.
                    '''

                    self.face_confidences.append(detection.score) 
                    '''detection.score, score: This is the confidence score for the detection. It ranges from 0 to 1, 
                    where 1 means the model is very confident that it has detected a face.'''


            try:
                result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                '''print(result)
                [{'emotion': {'angry': 0.015672415611334145, 'disgust': 6.055988501472986e-11, 'fear': 0.03761950065381825,
                'happy': 0.0005140727807884105, 'sad': 3.1068623065948486,
                'surprise': 5.844592578796437e-05, 'neutral': 96.83927297592163}, 'dominant_emotion': 'neutral',
                'region': {'x': 587, 'y': 101, 'w': 362, 'h': 362, 'left_eye': None, 'right_eye': None},
                'face_confidence': 0.96}]
                '''
                if isinstance(result, list):
                    result = result[0]
                    '''print(result)
                    {'emotion': {'angry': 0.015672415611334145, 'disgust': 6.055988501472986e-11, 'fear': 0.03761950065381825,
                    'happy': 0.0005140727807884105, 'sad': 3.1068623065948486, 'surprise': 5.844592578796437e-05, 'neutral': 96.83927297592163},
                    'dominant_emotion': 'neutral', 'region': {'x': 587, 'y': 101, 'w': 362, 'h': 362, 'left_eye': None, 'right_eye': None},
                    'face_confidence': 0.96}
                    '''
                
                for e, conf in result["emotion"].items():
                    '''print('e:', e,'conf:', conf)
                    e: angry conf: 0.5184038076549768
                    e: disgust conf: 7.854832236031672e-10
                    e: fear conf: 0.14429744333028793
                    e: happy conf: 0.00040638224163558334
                    e: sad conf: 0.9230316616594791
                    e: surprise conf: 7.798405476933112e-06
                    e: neutral conf: 98.4138548374176
                    '''
                    
                    if e in self.emotion_confidences:
                        self.emotion_confidences[e].append(conf) #appending the emotion values respect to their key for all frames

            except Exception as e:
                print(f"Error analyzing frame: {e}")

            pose_results = pose.process(image) #class 'mediapipe.python.solution_base.SolutionOutputs'>, if there is 55 frames,it will bring hfor each of them
            # print(pose_results)
            '''each mp_pose.PoseLandmark.__ has x,y,z and visibility values'''
            if pose_results.pose_landmarks: 
                '''print('pose_results.pose_landmarks:', pose_results.pose_landmarks)
                landmark {
                              x: 0.41657447814941406
                              y: 3.3906056880950928
                              z: 0.1598949134349823
                              visibility: 0.00010529020801186562
                            }
                '''
                
                landmarks = pose_results.pose_landmarks.landmark
                '''print(landmarks )
                              {
                              x: 0.41657447814941406
                              y: 3.3906056880950928
                              z: 0.1598949134349823
                              visibility: 0.00010529020801186562
                            }'''
                left_eye = landmarks[mp_pose.PoseLandmark.LEFT_EYE]
                '''print('left_eye:', left_eye)
                left_eye: x: 0.632472574710846
                y: 0.47062212228775024
                z: -1.233600378036499
                visibility: 0.9993627667427063'''
                right_eye = landmarks[mp_pose.PoseLandmark.RIGHT_EYE]
                '''print('right_eye:',right_eye)
                right_eye: x: 0.5287317037582397
                y: 0.45476844906806946
                z: -1.2204415798187256
                visibility: 0.9995083212852478'''
                nose = landmarks[mp_pose.PoseLandmark.NOSE]
                '''print('nose:',nose)
                nose: x: 0.5769361257553101
                y: 0.5567067265510559
                z: -1.2437708377838135
                visibility: 0.9996457099914551'''

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

        '''print('self.emotion_confidences :', self.emotion_confidences )
        self.emotion_confidences : 
        {'happy': [0.0005140727807884105, 0.0005387587728438075, 0.00032189204830501694, 0.00030856637770030476, 0.00022086014723754488, 4.024409134893792e-05,
        1.9048952707082358e-05, 1.2580991892718885e-05, 6.729971794710889e-05, 2.9176734983593633e-05, 1.4125492373958213e-05, 4.1675284023767745e-05, 0.00011729626714963494, 0.0003591201902963803,
        0.00011353628440831732, 8.912308544495318e-05, 6.382914534697193e-05, 7.894881832726242e-05, 8.803033892945678e-05, 0.00039009055399219505, 9.485399342916145e-05, 8.766771862539534e-05,
        9.807047847711772e-05, 0.0014508383173961192, 0.00305951944028493, 0.00036149801871943055, 5.7616941854561355e-05, 0.00011027312893929775, 0.00012920045264763758, 0.0010811609172378667,
        1.2571925289805774e-05, 9.393480837616153e-06, 0.0007254502224111897, 0.003084521449636668, 0.00036106892155109957,
        0.0019568701902657674, 0.000263610302023121, 0.0013425011275103316, 0.014161640137899667, 0.0005687648354069097, 0.00154346444210431, 0.023181387149830143, 0.012896764383185655,
        0.0012128084027015365, 0.00016574322067949444, 0.00040638224163558334, 0.006064765329938382, 0.0011907852240256034, 0.0052410808284922075, 0.00037720085401815595, 0.0002477331463524024,
        0.00027884613105114104, 7.33015029289957e-05, 5.337700418182913e-05, 7.596109412588703e-05], 
        'neutral': [96.83927297592163, 98.2753216192318, 96.7265248298645, 99.78962539372596, 99.8664140701294,
        99.8119234926655, 99.87251757815585, 99.59510564804077, 99.86869694367684, 99.99150037765503, 99.86979364572726, 99.46172833442688, 99.35221083733906, 94.33326125144958, 97.53123492374837,
        97.59650826454163, 94.30990815162659, 98.56640100479126, 98.58706593513489, 98.5937774181366, 99.86994861781291, 99.50317150316579, 98.33713163954805, 94.16512846946716, 95.40101289749146,
        94.81896162033081, 99.65451953736064, 99.52026605606079, 98.67890477180481, 93.26180219650269, 99.88858105080354, 99.06287789344788, 98.926979431274, 99.82343912124634, 98.53949564224534,
        97.79239879801266, 98.78517978103041, 88.67796063423157, 79.90659475326538, 94.81503963470459, 86.84154670486133, 87.88524197848093, 91.19231700897217, 94.88260210959886, 97.54774555848512,
        98.4138548374176, 96.42248749732971, 97.14482426643372, 97.79889013780473, 98.98321628570557, 99.2171049118042, 98.73504057704919, 99.52761528060527, 99.69295862997072, 99.73506927490234], 
        'surprise': [5.844592578796437e-05, 4.6550306297577545e-05, 0.0010384957931819372, 6.57574997235165e-05, 7.0980888722260715e-06, 4.967988983214242e-07, 1.40994035968189e-07,
        4.4129011556037767e-07, 9.000005000849655e-07, 2.445335267609039e-07, 5.9494290820611326e-08, 3.887420607640024e-07, 9.65026521339081e-07, 1.4066922915390023e-05, 1.3345284691700414e-06, 
        5.523111745731057e-07, 7.931439505171056e-07, 7.132749946237027e-07, 6.117627293633632e-07, 1.9545726814840236e-06, 1.3856629559241423e-06, 1.5821779332402674e-06, 4.025554529852108e-06,
        9.743101827552891e-05, 0.00013318315268406877, 4.8418549170037295e-06, 9.92021990396691e-07, 1.2644430391617334e-06, 5.627287436027473e-06, 0.0001372261635879113, 2.732801880975391e-07,
        3.628648492792763e-08, 3.989639431729284e-06, 4.754102462811716e-05, 2.416685585549373e-06, 3.299663743516033e-05, 6.393472443962865e-06, 0.00026306074687454384, 0.0013224866052041762,
        4.346320849890617e-05, 6.436562600198674e-05, 0.0033979560818701883, 0.0009846270586422179, 5.4967744331650295e-05, 7.458476592363442e-06, 7.798405476933112e-06, 7.235665577809414e-06,
        1.0775271164220612e-05, 1.3027766822164764e-05, 1.2467819487937959e-05, 8.46311749569395e-06, 9.331979409206537e-06, 3.4752458983609496e-06, 1.1105800287762618e-06,
        2.3722348529986448e-06], 
        'angry': [0.015672415611334145, 0.023315301157701085, 0.2553233178332448, 0.006719406192462888, 0.0021211380953900516, 0.004617274228255777, 0.0029911647252710933,
          0.03928685327991843, 0.009936801777770158, 0.000886647558218101, 0.01290412114547915, 0.04391729016788304, 0.061783123148381934, 1.4407477341592312, 0.4119023706051553, 0.21013650111854076,
            1.2487844564020634, 0.037892741966061294, 0.016837063594721258, 0.05979766137897968, 0.006688492829504926, 0.1326470361288445, 0.6794517799140084, 1.9255831837654114, 0.3858944168314338,
              0.5320870317518711, 0.07730331150573859, 0.07054193993099034, 0.6746701896190643, 4.240614175796509, 0.06053266558034234, 0.5127329844981432, 0.4871299375289753, 0.018288721912540495,
                0.4823510891376627, 0.9159499393969738, 0.6387137722947461, 4.835695028305054, 4.30595837533474, 2.339896559715271, 6.790285962241051, 0.8883017644764044, 0.9852654300630093, 1.2801689432360002, 
                0.6018519760282025, 0.5184038076549768, 0.27789995074272156, 0.5936435423791409, 0.24956142814470195, 0.3272846108302474, 0.1788580440916121, 0.32381118140385373, 0.16506986977948962,
                  0.10793037822927497, 0.08299738401547074],
        'fear': [0.03761950065381825, 0.027398225388942682, 0.3737109014764428, 0.006974042896263996, 0.0035023655073018745, 0.002601937349500591,
                    0.0008818018230065393, 0.006078217484173365, 0.005117564550555998, 0.0006137435775599442, 0.005117591295298974, 0.07931465515866876, 0.14827885294361676, 2.148721367120743, 0.6663498797386741,
                      0.758130569010973, 0.9480990469455719, 0.9905441664159298, 0.9036160074174404, 0.6018288899213076, 0.041957789971771235, 0.037569618030534026, 0.09095754318058748, 0.9083674289286137,
                        1.7035912722349167, 2.6945888996124268, 0.04474874852590254, 0.06990718538872898, 0.10603897972032428, 0.39576850831508636, 0.00048551627183988894, 0.0034547185350675136, 0.003246516984720552,
                          0.022458043531514704, 0.011669089208689129, 0.05010392349832794, 0.01618207412367011, 0.6331589072942734, 3.510560467839241, 0.19205427961423993, 0.55255800053823, 3.816322092194682,
                            2.094879373908043, 0.7032403349738914, 0.15563774850295475, 0.14429744333028793, 0.26876586489379406, 0.3502481849864125, 0.19903345920491705, 0.05717778694815934, 0.06005188333801925,
                              0.07688686266400067, 0.02552997182022612, 0.006488424650841993, 0.020527812012005597],
        'disgust': [6.055988501472986e-11, 6.456049188010018e-11, 4.120492141934662e-09,
                                1.5868944678171736e-12, 3.889209799075007e-13, 1.1649714921251237e-13, 5.248897786173281e-14, 1.2978736873203375e-12, 1.808905982342468e-13, 3.067675402269258e-15,
                                  2.7899022308157745e-13, 2.315019378452965e-11, 2.048153936819059e-10, 3.5963287903229e-08, 4.430651860107405e-09, 1.3062572724875654e-09, 8.935374662399909e-09,
                                    1.98233421865035e-10, 1.1047480204945392e-10, 2.0990115895402894e-09, 1.6414581990085203e-11, 8.202959902130366e-10, 2.5321544982404127e-09, 3.276356075332387e-07,
                                      2.605133331279319e-08, 1.3488586636523081e-08, 8.318014741931519e-11, 3.958092100603272e-10, 5.11483980170091e-09, 2.606819426986817e-07, 5.300150063971998e-13, 
                                      2.0170173650334473e-12, 8.592249693068447e-11, 4.686622184085776e-11, 2.3733167547663234e-10, 3.354820094070879e-09, 1.4730691503648227e-09, 4.707557454963762e-07,
                                        2.04372252454732e-06, 4.0191083794383076e-08, 1.258012435932963e-07, 4.4985085007185744e-07, 2.1635417901677556e-07, 2.6236348852230466e-08, 1.3283724738982252e-09,
                                          7.854832236031672e-10, 2.179365715671011e-08, 7.158507814297721e-09, 1.0754910956478879e-08, 3.19361377620897e-10, 7.21772034500967e-11, 5.06134657134677e-10, 
                                          3.7490726735193233e-11, 7.709533047040243e-12, 7.387060391552194e-12], 
        'sad': [3.1068623065948486, 1.6733798264491455, 2.6430796831846237, 0.1963055343959054,
                                            0.1277369214221835, 0.1808171384709858, 0.12359035472365348, 0.3595152869820595, 0.11617664492632211, 0.0069673820689786226, 0.11217258375049137, 0.4150018561631441,
                                              0.437605189146973, 2.0768987014889717, 1.390400042730575, 1.4351407997310162, 3.4931443631649017, 0.40508625097572803, 0.49239196814596653, 0.7442024536430836, 
                                              0.08131139232211664, 0.32651713882182376, 0.892357953927395, 2.9993759468197823, 2.5063110515475273, 1.9539950415492058, 0.22336937421526756, 0.3391721984371543, 0
                                              .5402567330747843, 2.100597508251667, 0.05038278158847611, 0.4209246952086687, 0.581910065855376, 0.13268461916595697, 0.9661163914362918, 1.239555589232182, 
                                              0.559651838445773, 5.8515846729278564, 12.261398881673813, 2.652396075427532, 5.814002800822425, 7.383555613968111, 5.713653564453125, 3.132715075288406, 
                                              1.6945920032019617, 0.9230316616594791, 3.0247755348682404, 1.910082995891571, 1.747256309121095, 0.631934218108654, 0.5437304265797138, 0.8639713650677961, 
                                              0.28170593365019164, 0.1925648542602534, 0.1613242900930345]}'''
        video.release()
        end_time = time.time()
        total_time = end_time - start_time
        fps = self.frame_count / total_time

        print(f"Total frames processed: {self.frame_count}")
        print(f"Total time taken: {total_time:.2f} seconds")
        print(f"Frames per second (FPS): {fps:.2f}")


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

        # Arranging the values together, all values out of 10
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
