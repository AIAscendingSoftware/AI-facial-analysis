

import cv2
import numpy as np


def video_to_binary(video_path):
    with open(video_path, 'rb') as video_file:
        binary_data = video_file.read()
    return binary_data

def save_binary_data(binary_data, output_path):
    with open(output_path, 'wb') as binary_file:
        binary_file.write(binary_data)

def binary_to_video(binary_data):
    video_data = np.frombuffer(binary_data, dtype=np.uint8)
    video_file = 'temp_video.mp4'
    with open(video_file, 'wb') as video:
        video.write(video_data)
    
    cap = cv2.VideoCapture(video_file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# Convert video to binary
binary_data = video_to_binary(r'D:\AI Projects\AI facial analysis\videos for AI facial anlysis\8e0bd41f-2151-44ea-8684-246b9e216e8d.webm')
print(binary_data)
# Save binary data to a file (optional)
save_binary_data(binary_data, 'video_binary.bin')

# Read binary data and play the video
with open('video_binary.bin', 'rb') as binary_file:
    binary_data = binary_file.read()

binary_to_video(binary_data)
