

import librosa
import numpy as np
import moviepy.editor as mp
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import tempfile
import os
import spacy
import io
import base64
import speech_recognition as sr

def calculate_pronunciation_score(recognizer, audio_data):
    try:
        result = recognizer.recognize_google(audio_data, show_all=True)
        if not result or 'alternative' not in result:
            return 0, ""
        top_alternative = result['alternative'][0]
        transcript = top_alternative['transcript']
        confidence = top_alternative.get('confidence', 0.5)
        return confidence, transcript
    except sr.UnknownValueError:
        return 0, ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return 0, ""
    
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio_data = recognizer.record(source)
    pronunciation_score, transcript = calculate_pronunciation_score(recognizer, audio_data)
    return transcript, pronunciation_score 


class SpeechAnalyzer:
    def __init__(self):
        # print('you are in SpeechAnalyzer initilalizer')#prited
        self.nlp = spacy.load("en_core_web_sm")
        print('self.nlp:',self.nlp)
        # print('you are in SpeechAnalyzer initilalizer')
        self.max_grammar_mistakes = 10
        self.max_tone = 300
        self.max_confidence = 0.1
        self.voice = None
        self.sp = None
        self.speech_rate = 0
        print('you are in SpeechAnalyzer initilalizer')


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

    
    def analyze(self, text, audio_output_path):
        try:

            self.extract_voice(audio_output_path)
            self.calculate_speech_rate(text)

            tone, confidence = self.analyze_audio(audio_output_path)
            grammar_mistakes, fluency = self.analyze_text(text)
            


            #to get the pronunciation score
            text_, pronunciation_score = transcribe_audio(audio_output_path)
            scores = {
                "grammar":  float(f"{(1 - (float(grammar_mistakes) / self.max_grammar_mistakes)):.2f}"),
                "fluency": float(f"{fluency:.2f}"),
                "tone":  float(f"{(float(tone) / self.max_tone):.2f}"),
                "voiceConfidence": float(f"{(float(confidence) / self.max_confidence):.2f}"),
                "speechRate":  float(f"{(self.speech_rate):.2f}"),
                "voiceGraphBase64": "voice_graph_base64", #dummy baseurl
                # "voiceGraphBase64": voice_graph_base64, #real baseurl
                "pronunciation":float(f"{pronunciation_score:.2f}")
            }
            # print('speech and communication data:',scores, type(scores['fluency']),scores['fluency']+100 )
            # os.unlink(audio_output_path) #to delete the audio using it's path
            return scores
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None


