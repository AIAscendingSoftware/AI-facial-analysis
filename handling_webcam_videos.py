import cv2
import subprocess
import os
import shutil

def check_ffmpeg():
    return shutil.which("ffmpeg") is not None

def play_video_and_save_audio(video_path):
    # Create a VideoCapture object for video playback
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Check if FFmpeg is available
    ffmpeg_available = check_ffmpeg()

    if ffmpeg_available:
        # Generate output audio filename
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_output_path = f"{base_name}_audio.mp3"

        # Use FFmpeg to extract audio
        ffmpeg_command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",  # Disable video
            "-acodec", "libmp3lame",
            "-q:a", "2",  # Variable bit rate quality (0-9, lower is better)
            audio_output_path
        ]

        try:
            subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
            print(f"Audio saved to: {audio_output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            print(f"FFmpeg output: {e.output}")
    else:
        print("FFmpeg is not available. Audio extraction will be skipped.")
        print("To enable audio extraction, please install FFmpeg and add it to your system PATH.")

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print(f"End of video reached. Total frames processed: {frame_count}")
            break
        
        frame_count += 1
        
        # Display the frame
        cv2.imshow('Frame', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            print(f"Video playback stopped by user. Frames processed: {frame_count}")
            break

    # Release the VideoCapture object and close windows
    cap.release()
    cv2.destroyAllWindows()

# Path to your video file
video_path = r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\8e0bd41f-2151-44ea-8684-246b9e216e8d.webm"

play_video_and_save_audio(video_path)


# import cv2

# def play_video(video_path):
#     # Create a VideoCapture object
#     cap = cv2.VideoCapture(video_path)

#     # Check if the video file was successfully opened
#     if not cap.isOpened():
#         print("Error opening video file")
#         return

#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
        
#         # If frame is read correctly ret is True
#         if not ret:
#             print(f"End of video reached. Total frames processed: {frame_count}")
#             break
        
#         frame_count += 1
        
#         # Display the frame
#         cv2.imshow('Frame', frame)
        
#         # Press 'q' to exit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             print(f"Video playback stopped by user. Frames processed: {frame_count}")
#             break

#     # Release the VideoCapture object and close windows
#     cap.release()
#     cv2.destroyAllWindows()

# # Path to your video file
# video_path = r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\8e0bd41f-2151-44ea-8684-246b9e216e8d.webm"

# play_video(video_path)