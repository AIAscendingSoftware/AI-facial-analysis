from flask import Blueprint, request, jsonify
import threading, time, queue
from app.main_ import VideoProcessing
from app.utils.convert_video_to_base64 import base64_to_video

main_bp = Blueprint('main', __name__)

# Initialize the process_complete event
process_complete = threading.Event()

def process_video(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:', videoI_userId)
    output_path = "temporary_video.mp4"
    decoded_video_path = base64_to_video(base64_string, output_path)
    if decoded_video_path:
        processor = VideoProcessing(decoded_video_path, videoI_userId)
        result = processor.process()
    process_complete.set()  # Signal that the process is complete

    print("Process complete. Signaling for restart...")
    with open("restart.txt", "w") as f:
        f.write("restart")
    print(result, type(result))
    return result

@main_bp.route('/post_video', methods=['POST'])
def receive_data():
    start_time = time.time()
    print('process is started:',start_time)
    data = request.get_json()
    try:
        video_base64 = data['baseUrl']  # for development and testing
        videoI_userId = {"userId": data['userId'], 'videoId': data['id']}
        
        # Process the video in a separate thread
        process_complete.clear()
        
        def threaded_function(q, video_base64, videoI_userId):
            result = process_video(video_base64, videoI_userId)
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

    finally:
        
        end_time=time.time()
        print('process is finished and the end_time:',end_time) 
        total_time = end_time - start_time
        minutes, seconds = divmod(total_time, 60)
        # Conditional formatting for minutes
        minutes_str = f"{minutes}m" if minutes > 0 else ""
        print(f"Total time taken: {minutes_str} {seconds:.0f}sec")
