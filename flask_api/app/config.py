class Config:
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    video_path="temporary_video.mp4"
    audio_path="extracted_audio.wav"

# we can add more configuration classes if needed, e.g.:
# class ProductionConfig(Config):
#     DEBUG = False
#     HOST = "0.0.0.0"
#     PORT = 80