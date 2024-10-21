import cv2
import numpy as np
from openpose import OpenPose

# Initialize OpenPose
params = {
    "model_folder": r"E:\AI Ascending Software\AS AI Projects\AI facial analysis\openpose",
    "hand": True,
    "body": 1
}

op = OpenPose(params)

def is_wrists_closed(keypoints):
    """
    Determines if the wrists are closed based on keypoints.
    Assumes `keypoints` contains wrist keypoints in the format:
    [x, y, confidence] for each keypoint.
    """
    # Wrist keypoints
    left_wrist = keypoints[7]  # Index may vary
    right_wrist = keypoints[4]  # Index may vary

    if left_wrist[2] > 0.5 and right_wrist[2] > 0.5:  # Check confidence
        # Define a threshold distance to determine if wrists are closed
        threshold = 50  # Adjust as needed
        distance = np.linalg.norm(np.array(left_wrist[:2]) - np.array(right_wrist[:2]))
        return distance < threshold
    return False

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect keypoints
        keypoints, _ = op.detect(frame)
        
        if keypoints is not None:
            wrists_closed = is_wrists_closed(keypoints)
            if wrists_closed:
                cv2.putText(frame, "Wrists Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('OpenPose', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Replace with the path to your video file
video_path = "E:\AI Ascending Software\AS AI Projects\AI facial analysis\videos for AI facial anlysis\3s 2mb.mp4"
process_video(video_path)
