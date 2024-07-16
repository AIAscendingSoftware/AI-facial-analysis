from video_to_text import VideoToText
from getting_gestures_score import GestureAnalyzer

def main(video_path):
    # Video to Text
    video_to_text = VideoToText(video_path)
    transcribed_text = video_to_text.get_transcribed_text()
    print("Transcribed Text:", transcribed_text)

    # Gesture Analysis
    gesture_analyzer = GestureAnalyzer(video_path)
    gesture_analyzer.analyze_gestures()
    results = gesture_analyzer.get_results()
    print("Emotion Percentages and Additional Data:")
    print(results)

