from deepface import DeepFace

class EmotionAnalyzer:
    def analyze_emotion(self, frame):
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        return result
