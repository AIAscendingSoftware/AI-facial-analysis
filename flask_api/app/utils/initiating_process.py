

from app.main_ import VideoProcessing
from app.utils.convert_video_to_base64 import base64_to_video
import os
from app.config import Config


def process_video(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:', videoI_userId)
    decoded_video_path = base64_to_video(base64_string, Config.video_path)
    print("decoded_video_path result:",decoded_video_path)
    if decoded_video_path != None:
        
        if decoded_video_path:
            processor = VideoProcessing(decoded_video_path, videoI_userId)
            result = processor.process()


        print(result, type(result), 'this error coms from the process method')
        return result
    else:
        return "Invalid Base64 string, there is improper baseurl"