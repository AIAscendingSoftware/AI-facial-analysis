import os
from io import BytesIO
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


class VideoToText:
    def __init__(self, video_path):
        self.video_path = video_path

    def extract_audio(self):
        print('you are in method extract_audio')
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"The file {self.video_path} does not exist!")

        video = mp.VideoFileClip(self.video_path) #print('video:', video), video: <moviepy.video.io.VideoFileClip.VideoFileClip object at 0x000001A43F5BE870>
        audio = video.audio #print('audio:', audio), audio: <moviepy.audio.io.AudioFileClip.AudioFileClip object at 0x000001A43F448CE0

        if audio is None:
            print('There is no audio in the video.')
            return None
        try:
            audio_buffer = BytesIO() #print('audio_buffer:', audio_buffer), audio_buffer: <_io.BytesIO object at 0x000001A42F7BE3E0>
            audio.write_audiofile("temp_audio.wav", codec='pcm_s16le', write_logfile=False) #print('audio:', audio), audio: <moviepy.audio.io.AudioFileClip.AudioFileClip object at 0x000001A43F448CE0>
            audio_segment = AudioSegment.from_wav("temp_audio.wav") #print('audio_segment:', audio_segment), audio_segment: <pydub.audio_segment.AudioSegment object at 0x000001A43F5BDA00
            audio_segment.export(audio_buffer, format="wav") #print('audio_segment:', audio_segment), audio_segment: <pydub.audio_segment.AudioSegment object at 0x000001A43F5BDA00>
            audio_buffer.seek(0) #print('audio_buffer:', audio_buffer), audio_buffer: <_io.BytesIO object at 0x000001A42F7BE3E0
            print('The audio is there, we are processng...',)
            os.remove("temp_audio.wav")
            return audio_buffer
        except Exception as e:
            print(f'An error occurred while processing the audio: {e}')
            return None

    

    def transcribe_audio(self, audio_buffer):
        recognizer = sr.Recognizer()
        sound = AudioSegment.from_file(audio_buffer, format="wav")

        chunks = split_on_silence(
            sound,
            min_silence_len=500,
            silence_thresh=sound.dBFS - 14,
            keep_silence=500,
        )

        full_text = ""
        for audio_chunk in chunks:
            chunk_buffer = BytesIO()
            audio_chunk.export(chunk_buffer, format="wav")
            chunk_buffer.seek(0)

            with sr.AudioFile(chunk_buffer) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    text = ""
                full_text += f"{text}"

        return full_text.strip()

    # def get_transcribed_text(self):
    #     audio_buffer = self.extract_audio()
    #     if audio_buffer is not None:
    #         transcribed_text = self.transcribe_audio(audio_buffer)
    #     return transcribed_text
    def get_transcribed_text(self):
        try:
            audio_buffer = self.extract_audio()
            
            if audio_buffer is not None:
                transcribed_text = self.transcribe_audio(audio_buffer)
                return transcribed_text
            else:
                print('No audio buffer available for transcription.')
                return None
        except Exception as e:
            print(f'An error occurred while transcribing the audio: {e}')
            return None
