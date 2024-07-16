from video_to_text import VideoToText
from getting_gestures_score import GestureAnalyzer
from video_to_audio_analyse import SpeechAnalyzer

def main(video_path):
    # Video to Text
    video_to_text = VideoToText(video_path)
    transcribed_text = video_to_text.get_transcribed_text()
    print("Transcribed Text:", transcribed_text)

    # Gesture Analysis
    gesture_analyzer = GestureAnalyzer(video_path)
    gesture_analyzer.analyze_gestures()
    gesture_results = gesture_analyzer.get_results()
    print("\nGesture Analysis Results:")
    print(gesture_results)

    # Speech Analysis
    speech_analyzer = SpeechAnalyzer(video_path)
    speech_scores = speech_analyzer.analyze(transcribed_text)
    print(speech_scores)
    # if speech_scores:
    #     print("\nSpeech Analysis Scores:")
    #     for key, value in speech_scores.items():
    #         print(f"{key}: {value:.2f}")
    # else:
    #     print("Speech analysis could not be completed.")

    print("\nSpeech level graph has been saved as 'speech_level_graph.png'")

if __name__ == "__main__":
    video_file = r"C:\Users\prani\OneDrive\Pictures\Camera Roll\WIN_20240716_12_58_11_Pro.mp4"
    main(video_file)


