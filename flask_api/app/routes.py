from flask import Blueprint, request, jsonify
from app.config import Config
from app.utils.handling_files import remove_file
from app.utils.initiating_process import process_video
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/post_video', methods=['POST'])
def receive_data():
    start_time = time.time()
    print('Process started:', start_time)
    data = request.get_json()

    try:
        video_base64 = data["videoBytes"]
        video_user_id = {"userId": data['userId'], 'videoId': data['id']}

        result = process_video(video_base64, video_user_id)
        print('Result from .route/post_video:', result)

        # Check the result for success or error
        if result == 'Data processed successfully completed!':
            # Prepare and send a success response
            response = jsonify({'message': 1, 'text':result })
            return response, 200  # 200 OK
        else:
            # Prepare and send an error response
            response = jsonify({'message': 2, 'text':result })
            return response, 200  # 200 OK

    except Exception as e:
        # Handle exceptions and prepare the error response
        response = jsonify({
            'message': 'Error processing request',
            'error': str(e)
        })
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


