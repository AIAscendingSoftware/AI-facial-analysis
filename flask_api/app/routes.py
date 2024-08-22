from flask import Blueprint, request, jsonify
import threading, time, queue
from app.main_ import VideoProcessing
from app.utils.convert_video_to_base64 import base64_to_video
import os
from app.config import Config



main_bp = Blueprint('main', __name__)

# Initialize the process_complete event
process_complete = threading.Event()



def process_video(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:', videoI_userId)
    decoded_video_path = base64_to_video(base64_string, Config.video_path)
    print("decoded_video_path result:",decoded_video_path)
    if decoded_video_path != None:
        
        if decoded_video_path:
            processor = VideoProcessing(decoded_video_path, videoI_userId)
            result = processor.process()

        process_complete.set()  # Signal that the process is complete

        print(result, type(result), 'this error coms from the process method')
        return result
    else:
        return "Invalid Base64 string, there is improper baseurl"

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been removed")
    else:
        print(f"{file_path} doesn't exit.")


@main_bp.route('/post_video', methods=['POST'])
def receive_data():
    start_time = time.time()
    print('process is started:',start_time)
    data = request.get_json()
    print(data,'data by trigger')
    try:
        video_base64 = data['baseUrl']  # for development and testing

        videoI_userId = {"userId": data['userId'], 'videoId': data['id']}

        result = process_video(video_base64, videoI_userId)
        print('result from .route/post_video:', result)
        # Prepare and send the response after processing is complete
        response = jsonify({'message': result})
        print('Restarting app...')
        return response, 200  # 200 OK

    except Exception as e:
        response = jsonify({'message': 'Error processing request', 'error': str(e), 'result': result})
        return response, 500

    finally:
        end_time=time.time()
        print('process is finished and the end_time:',end_time) 
        total_time = end_time - start_time
        minutes, seconds = divmod(total_time, 60)
        # Conditional formatting for minutes
        minutes_str = f"{minutes}m" if minutes > 0 else ""
        print(f"Total time taken: {minutes_str} {seconds:.0f}sec")

        #to remove the vidoe and audio file
        # remove_file(Config.video_path) #to remoe the video file
        # remove_file(Config.audio_path) #to remove the audio file


