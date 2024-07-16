import librosa
import numpy as np
import moviepy.editor as mp
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import tempfile
import os
import spacy

class SpeechAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.nlp = spacy.load("en_core_web_sm")
        self.max_grammar_mistakes = 10
        self.max_tone = 300
        self.max_confidence = 0.1
        self.voice = None
        self.sp = None
        self.speech_rate = 0

    def extract_audio(self):
        with mp.VideoFileClip(self.video_path) as video:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                video.audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le')
                return temp_audio_file.name

    def extract_voice(self, audio_path):
        try:
            y, sp = librosa.load(audio_path, sr=None)
            S = librosa.feature.melspectrogram(y=y, sr=sp)
            S_db = librosa.power_to_db(S, ref=np.max)
            mean_energy = np.mean(S_db, axis=0)
            smoothed_energy = medfilt(mean_energy, kernel_size=11)
            threshold = np.mean(smoothed_energy) - 1.0 * np.std(smoothed_energy)
            voice_segments = librosa.effects.split(y, top_db=threshold)
            self.voice = np.concatenate([y[start:end] for start, end in voice_segments]) if voice_segments else y
            self.sp = sp
        except Exception as e:
            print(f"Error in extract_voice: {e}")
            self.voice = None
            self.sp = None

    def analyze_audio(self, audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        return tempo, rmse.mean()

    def calculate_speech_rate(self, text):
        if self.voice is None or self.sp is None:
            print("Voice data is not available. Speech rate cannot be calculated.")
            self.speech_rate = 0
        else:
            words = text.split()
            audio_duration = len(self.voice) / self.sp if self.sp != 0 else 0
            self.speech_rate = len(words) / (audio_duration / 60) if audio_duration > 0 else 0

    def analyze_text(self, text):
        doc = self.nlp(text)
        grammar_mistakes = len([token for token in doc if token.dep_ == 'dep'])
        named_entities = len(doc.ents)
        noun_chunks = len(list(doc.noun_chunks))
        fluency = (named_entities + noun_chunks) / len(doc) if len(doc) > 0 else 0
        return grammar_mistakes, fluency

    def generate_speech_level_graph(self, audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        energy = np.abs(y)**2
        energy_norm = energy / energy.max()
        time = np.arange(0, len(y)) / sr

        plt.figure(figsize=(12, 6))
        plt.plot(time, energy_norm)
        plt.xlabel('Time (s)')
        plt.ylabel('Speech Level')
        plt.title('Speech Level Over Time')
        plt.savefig('speech_level_graph.png', dpi=300)
        plt.close()

    def analyze(self, text):
        try:
            temp_audio_path = self.extract_audio()
            self.extract_voice(temp_audio_path)
            self.calculate_speech_rate(text)

            tone, confidence = self.analyze_audio(temp_audio_path)
            grammar_mistakes, fluency = self.analyze_text(text)
            
            scores = {
                "Grammar Score": 1 - (float(grammar_mistakes) / self.max_grammar_mistakes),
                "Fluency Score": float(fluency),
                "Tone Score": float(tone) / self.max_tone,
                "Confidence Score": float(confidence) / self.max_confidence,
                "Speech Rate": float(self.speech_rate)
            }
            
            self.generate_speech_level_graph(temp_audio_path)
            os.unlink(temp_audio_path)
            return scores
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None

# import speech_recognition as sr
# import librosa
# import numpy as np
# import moviepy.editor as mp
# import matplotlib.pyplot as plt
# from scipy.signal import medfilt
# import spacy
# import tempfile
# import os

# class SpeechAnalyzer:
#     def __init__(self, video_path):
#         self.video_path = video_path
#         self.nlp = spacy.load("en_core_web_sm")
#         self.max_grammar_mistakes = 10
#         self.max_tone = 300
#         self.max_confidence = 0.1
#         self.text = ""
#         self.voice = None
#         self.sp = None
#         self.speech_rate = 0

#     def extract_audio(self):
#         video = mp.VideoFileClip(self.video_path)
#         audio = video.audio
#         temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#         audio.write_audiofile(temp_audio_file.name, codec='pcm_s16le')
#         return temp_audio_file.name

#     def extract_voice(self, audio_path):
#         try:
#             y, sp = librosa.load(audio_path, sr=None)
            
#             S = librosa.feature.melspectrogram(y=y, sr=sp)
#             S_db = librosa.power_to_db(S, ref=np.max)
            
#             mean_energy = np.mean(S_db, axis=0)
#             smoothed_energy = medfilt(mean_energy, kernel_size=11)
            
#             threshold = np.mean(smoothed_energy) - 1.0 * np.std(smoothed_energy)
            
#             voice_segments = librosa.effects.split(y, top_db=threshold)
            
#             if len(voice_segments) == 0:
#                 self.voice = y
#                 self.sp = sp
#             else:
#                 self.voice = np.concatenate([y[start:end] for start, end in voice_segments])
#                 self.sp = sp
#         except Exception as e:
#             print(f"Error in extract_voice: {e}")
#             self.voice = None
#             self.sp = None

#     def transcribe_audio(self, audio_path):
#         try:
#             recognizer = sr.Recognizer()
#             with sr.AudioFile(audio_path) as source:
#                 audio_data = recognizer.record(source)
#             self.text = recognizer.recognize_google(audio_data)
#         except Exception as e:
#             print(f"Error in transcribe_audio: {e}")
#             self.text = ""

#     def analyze_text(self):
#         doc = self.nlp(self.text)
        
#         grammar_mistakes = len([token for token in doc if token.dep_ == 'dep'])
        
#         named_entities = len(doc.ents)
#         noun_chunks = len(list(doc.noun_chunks))
#         fluency = (named_entities + noun_chunks) / len(doc) if len(doc) > 0 else 0
        
#         return grammar_mistakes, fluency

#     def analyze_audio(self, audio_path):
#         y, sr = librosa.load(audio_path, sr=None)
#         tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
#         rmse = librosa.feature.rms(y=y)
#         tone = tempo
#         confidence = rmse.mean()
#         return tone, confidence

#     def calculate_speech_rate(self):
#         if self.voice is None or self.sp is None:
#             print("Voice data is not available. Speech rate cannot be calculated.")
#             self.speech_rate = 0
#         else:
#             words = self.text.split()
#             audio_duration = len(self.voice) / self.sp if self.sp != 0 else 0
#             self.speech_rate = len(words) / (audio_duration / 60) if audio_duration > 0 else 0

#     def combine_scores(self, grammar_mistakes, fluency, tone, confidence):
#         grammar_score = 1 - grammar_mistakes / self.max_grammar_mistakes
#         fluency_score = fluency  # Already normalized
#         tone_score = tone / self.max_tone
#         confidence_score = confidence / self.max_confidence

#         return {
#             "Grammar Score": grammar_score,
#             "Fluency Score": fluency_score,
#             "Tone Score": tone_score,
#             "Confidence Score": confidence_score,
#             "Speech Rate": self.speech_rate
#         }

#     def generate_speech_level_graph(self, audio_path):
#         y, sr = librosa.load(audio_path, sr=None)
#         energy = np.abs(y)**2
#         energy_norm = energy / energy.max()
#         time = np.arange(0, len(y)) / sr

#         plt.figure(figsize=(12, 6))
#         plt.plot(time, energy_norm)
#         plt.xlabel('Time (s)')
#         plt.ylabel('Speech Level')
#         plt.title('Speech Level Over Time')
#         plt.savefig('speech_level_graph.png', dpi=300)

#     def analyze(self):
#         try:
#             temp_audio_path = self.extract_audio()
#             self.extract_voice(temp_audio_path)
#             self.transcribe_audio(temp_audio_path)
#             self.calculate_speech_rate()

#             if self.text:
#                 grammar_mistakes, fluency = self.analyze_text()
#                 tone, confidence = self.analyze_audio(temp_audio_path)
#                 scores = self.combine_scores(grammar_mistakes, fluency, tone, confidence)
#                 self.generate_speech_level_graph(temp_audio_path)
#                 os.unlink(temp_audio_path)  # Delete the temporary file
#                 return self.text, scores
#             else:
#                 os.unlink(temp_audio_path)  # Delete the temporary file
#                 return "No text could be extracted from the audio.", None
#         except Exception as e:
#             print(f"Error during analysis: {e}")
#             return "An error occurred during analysis.", None


