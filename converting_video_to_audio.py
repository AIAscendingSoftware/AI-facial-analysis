import subprocess

class videoToAudio:
    def __init__(self,video_path,audio_output_path):
        self.video_path=video_path
        self.audio_output_path=audio_output_path
        
    def video_to_audio_ffmpeg(self):
        command = ['ffmpeg', '-i', self.video_path, '-q:a', '0', '-map', 'a', self.audio_output_path]
        subprocess.run(command, check=True)


