

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
    def __init__(self, video_path):
        # print('you are in SpeechAnalyzer initilalizer')
        self.video_path = video_path
        print('self.video_path:',self.video_path)
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
        # y, sr = librosa.load(audio_path, sr=None)
        # energy = np.abs(y)**2
        # energy_norm = energy / energy.max()
        # time = np.arange(0, len(y)) / sr

        # plt.figure(figsize=(12, 6))
        # plt.plot(time, energy_norm)
        # plt.xlabel('Time (s)')
        # plt.ylabel('Speech Level')
        # plt.title('Speech Level Over Time')

        # # Save the plot as an image file
        # plt.savefig('speech_level_graph.png', dpi=300)
        ## above old plot
        audio, sr = librosa.load(audio_path)
        energy = np.abs(audio)**2
        energy_norm = energy / energy.max()
        time = np.arange(0, len(audio)) / sr
        window_size = int(0.1 * sr)
        energy_smoothed = medfilt(energy_norm, kernel_size=window_size)
        threshold = 0.01
        voice_mask = energy_smoothed > threshold
        noise_mask = ~voice_mask
        bin_size = 0.5 
        num_bins = int(np.ceil(time[-1] / bin_size))
        bins = np.linspace(0, time[-1], num_bins + 1)
        voice_levels = np.zeros(num_bins)
        noise_levels = np.zeros(num_bins)
        for i in range(num_bins):
            bin_mask = (time >= bins[i]) & (time < bins[i+1])
            voice_data = energy_norm[bin_mask & voice_mask]
            noise_data = energy_norm[bin_mask & noise_mask]

            voice_levels[i] = np.mean(voice_data) if len(voice_data) > 0 else 0
            noise_levels[i] = np.mean(noise_data) if len(noise_data) > 0 else 0

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(bins[:-1] + bin_size/2, voice_levels, width=bin_size, align='edge', color='yellow', alpha=0.7, label='Voice')
        ax.plot(bins[:-1] + bin_size/2, noise_levels, color='red', linewidth=2, label='Noise')
        ax.set_xlabel('Time Duration (s)')
        ax.set_ylabel('Voice Level')
        ax.set_title('Voice and Noise Levels Over Time')
        ax.legend()
        ax.set_ylim(bottom=0)
        plt.tight_layout()
        ### old plot end
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        plt.close()
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return img_base64
    
    def analyze(self, text):
        try:
            temp_audio_path = self.extract_audio()
            self.extract_voice(temp_audio_path)
            self.calculate_speech_rate(text)

            tone, confidence = self.analyze_audio(temp_audio_path)
            grammar_mistakes, fluency = self.analyze_text(text)
            
            voice_graph_base64 = self.generate_speech_level_graph(temp_audio_path)

            #to get the pronunciation score
            text_, pronunciation_score = transcribe_audio(temp_audio_path)
            scores = {
                "grammar":  float(f"{(1 - (float(grammar_mistakes) / self.max_grammar_mistakes)):.2f}"),
                "fluency": float(f"{fluency:.2f}"),
                "tone":  float(f"{(float(tone) / self.max_tone):.2f}"),
                "voiceConfidence": float(f"{(float(confidence) / self.max_confidence):.2f}"),
                "speechRate":  float(f"{(self.speech_rate):.2f}"),
                # "voiceGraphBase64": "voice_graph_base64", #dummy baseurl
                "voiceGraphBase64": voice_graph_base64, #real baseurl
                "pronunciation":float(f"{pronunciation_score:.2f}")
            }
            # print('speech and communication data:',scores, type(scores['fluency']),scores['fluency']+100 )
            os.unlink(temp_audio_path)
            return scores
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None


