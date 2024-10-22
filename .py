# import cv2
# from ultralytics import YOLO

# # Load the fine-tuned YOLO model
# model = YOLO(r'D:\AI Projects\AI facial analysis\yolov8x.pt')  # Path to your fine-tuned model

# # Open video feed
# video_path = r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\interview videos\TCS SQL_ PLSQL Real Interview BY TCS Team Interview Recording Simulation SQL TCS Ninja Interview.mp4"
# cap = cv2.VideoCapture(video_path)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Perform object detection using the fine-tuned model
#     results = model(frame)
    
#     # Draw results on the frame
#     annotated_frame = results[0].plot()  # Draw bounding boxes
    
#     # Display the frame
#     cv2.imshow('Live Detection', annotated_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import os

# Load YOLO model for person detection
model = YOLO(r'D:\AI Projects\AI facial analysis\yolov8x.pt')  # Path to your fine-tuned model
tracker = DeepSort(max_age=30)  # Initialize the tracker with max age for object persistence
video_path = r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\interview videos\TCS SQL_ PLSQL Real Interview BY TCS Team Interview Recording Simulation SQL TCS Ninja Interview.mp4"

# Initialize video capture
cap = cv2.VideoCapture(video_path)

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read the frame.")
        break
    
    # Run YOLO detection on the frame
    results = model(frame)

    detections = []
    
    for result in results:
        for detection in result.boxes:
            x1, y1, x2, y2 = detection.xyxy[0].tolist()  # Get bounding box coordinates
            confidence = detection.conf[0].item()         # Confidence score
            class_id = int(detection.cls[0])              # Class ID
            
            if class_id == 0:  # Person class ID in YOLO
                # Append only the bounding box to the detections
                detections.append([float(x1), float(y1), float(x2), float(y2)])

    # Use Deep SORT to track people
    if detections:
        # Update the tracker with the detections
        tracks = tracker.update_tracks(detections, frame=frame)
    else:
        tracks = tracker.update_tracks([], frame=frame)  # Pass empty list if no detections

    # Draw bounding boxes and track each person
    for track in tracks:
        if not track.is_confirmed():
            continue
        
        track_id = track.track_id
        bbox = track.to_tlbr()  # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, bbox)

        # Create directory for saving person frames
        person_dir = f"person_{track_id}"
        os.makedirs(person_dir, exist_ok=True)

        # Extract individual person frame (cropping to the bounding box)
        person_frame = frame[y1:y2, x1:x2]
        
        # Save person frame to separate directories by track_id
        person_video_path = os.path.join(person_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(person_video_path, person_frame)
    
    frame_count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()
