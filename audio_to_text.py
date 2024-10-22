# import speech_recognition as sr
# from pydub import AudioSegment
# from pydub.silence import split_on_silence
# from io import BytesIO
# import logging

# class audioToText:
#     def __init__(self,audio_path):
#         self.audio_path=audio_path

#     def transcribe_audio(self):
#         recognizer = sr.Recognizer()
#         sound = AudioSegment.from_file(self.audio_path, format="wav")
    
#         chunks = split_on_silence(
#             sound,
#             min_silence_len=500,
#             silence_thresh=sound.dBFS - 14,
#             keep_silence=500,
#         )
#         logging.info(f"Total chunks created: {len(chunks)}")
#         print( chunks,'Total chunks created:', len(chunks))
    
    
#         full_text = ""
#         for audio_chunk in chunks:
#             chunk_buffer = BytesIO()
#             audio_chunk.export(chunk_buffer, format="wav")
#             chunk_buffer.seek(0)
    
#             with sr.AudioFile(chunk_buffer) as source:
#                 audio_data = recognizer.record(source)
#                 # print(audio_data)
#                 try:
#                     text = recognizer.recognize_google(audio_data)
#                     # print(text)
#                 except sr.UnknownValueError:
#                     text = ""
#                 full_text += f"{text} "
#         if len(full_text.strip()) ==0:
#             return None
#         else:
#             return full_text.strip()


#introduced parallel processing to speed-up the processing time
import concurrent.futures
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from io import BytesIO
import logging

class audioToText:
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def transcribe_chunk(self, audio_chunk):
        recognizer = sr.Recognizer()
        chunk_buffer = BytesIO()
        audio_chunk.export(chunk_buffer, format="wav")
        chunk_buffer.seek(0)

        with sr.AudioFile(chunk_buffer) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = ""
        return text

    def transcribe_audio(self):
        sound = AudioSegment.from_file(self.audio_path, format="wav")

        # Split audio into chunks based on silence
        chunks = split_on_silence(
            sound,
            min_silence_len=500,
            silence_thresh=sound.dBFS - 14,
            keep_silence=500,
        )
        logging.info(f"Total chunks created: {len(chunks)}")
        print(f"Total chunks created: {len(chunks)}")

        # Process the chunks in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.transcribe_chunk, chunks))

        full_text = " ".join(results).strip()
        return full_text if full_text else None