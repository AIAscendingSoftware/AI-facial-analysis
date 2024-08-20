import subprocess
import json
import os

class VideoToAudio:
    def __init__(self, video_path, audio_output_path):
        self.video_path = video_path
        self.audio_output_path = audio_output_path

    def has_audio_stream(self):
        command = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'json', self.video_path]
        print("has_audio_stream command:",command )
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except:
            return "there is no proper video data"
        print("has_audio_stream result:",result)
        streams = json.loads(result.stdout).get('streams', [])
        return any(stream.get('codec_type') == 'audio' for stream in streams)

    def video_to_audio_ffmpeg(self):
        if not self.has_audio_stream():
            print("No audio stream found in the video.")
            return None
        command = ['ffmpeg','-y', '-i', self.video_path, '-q:a', '0', '-map', 'a', self.audio_output_path]
        subprocess.run(command, check=True)
        print(f"Audio has been successfully extracted and saved to {self.audio_output_path}.")
        return self.audio_output_path
