from flask import Blueprint, request, jsonify
import threading
import queue
from app.main_ import main
from app.utils.convert_video_to_base64 import base64_to_video

main_bp = Blueprint('main', __name__)

# Initialize the process_complete event
process_complete = threading.Event()

def make_video_path(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:', videoI_userId)
    output_path = "temporary_video.mp4"
    decoded_video_path = base64_to_video(base64_string, output_path)
    if decoded_video_path:
        result = main(decoded_video_path, videoI_userId)

    process_complete.set()  # Signal that the process is complete

    print("Process complete. Signaling for restart...")
    with open("restart.txt", "w") as f:
        f.write("restart")
    print(result, type(result))
    return result

@main_bp.route('/post_video', methods=['POST'])
def receive_data():
    data = request.get_json()
    try:
        video_base64 = data['baseUrl']  # for development and testing
        videoI_userId = {"userId": data['userId'], 'videoId': data['id']}
        
        # Process the video in a separate thread
        process_complete.clear()
        
        def threaded_function(q, video_base64, videoI_userId):
            result = make_video_path(video_base64, videoI_userId)
            q.put(result)

        q = queue.Queue()
        thread = threading.Thread(target=threaded_function, args=(q, video_base64, videoI_userId))
        thread.start()

        # Get the result
        result = q.get()
        print('result:', result, type(result))
        thread.join()
        # Wait for the process to complete
        process_complete.wait()
        
        # Prepare and send the response after processing is complete
        response = jsonify({'message': result})
        print('Restarting app...')
        return response, 200  # 200 OK

    except Exception as e:
        response = jsonify({'message': 'Error processing request', 'error': str(e), 'result': result})
        return response, 500