import subprocess
import json
import os

class VideoToAudio:
    def __init__(self, video_path, audio_output_path):
        self.video_path = video_path
        self.audio_output_path = audio_output_path

    def has_audio_stream(self):
        '''In this method, we return Fasle when we get any error while processsing,
        because of this method is completely for checking whether the video has audio or not'''
        command = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'json', self.video_path]
        print("has_audio_stream command:",command )
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print('result = subprocess.run(command, capture_output=True, text=True, check=True):',result )
        except:
            return False
        print("has_audio_stream result:",result)
        streams = json.loads(result.stdout).get('streams', [])
        print("any(stream.get('codec_type') == 'audio' for stream in streams):", any(stream.get('codec_type') == 'audio' for stream in streams))
        return any(stream.get('codec_type') == 'audio' for stream in streams)
        '''it returns False when there is no audio, it returns True when there is proper audio in the video''' 

    def video_to_audio_ffmpeg(self):
        if not self.has_audio_stream(): #if not False: is also if True:
            print("No audio stream found in the video.")
            return None
        command = ['ffmpeg','-y', '-i', self.video_path, '-q:a', '0', '-map', 'a', self.audio_output_path]
        subprocess.run(command, check=True)
        print(f"Audio has been successfully extracted and saved to {self.audio_output_path}.")
        return self.audio_output_path
