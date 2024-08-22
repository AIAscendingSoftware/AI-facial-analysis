from flask import Blueprint, request, jsonify
from app.config import Config
from app.utils.handling_files import remove_file
from app.utils.initiating_process import process_video
import time


main_bp = Blueprint('main', __name__)






@main_bp.route('/post_video', methods=['POST'])
def receive_data():
    start_time = time.time()
    print('process is started:',start_time)
    data = request.get_json()
    # print(data,'data by trigger')
    try:
        # video_base64 = data['baseUrl']  # for development and testing
        video_base64=data["videoBytes"]

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


