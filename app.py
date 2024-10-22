
'rerun app after completing process amd return the respones after completing process'
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading,queue, os, time, sys
from main_ import main
from convert_video_to_base64 import base64_to_video
from concurrent.futures import ThreadPoolExecutor



# Initialize the process_complete event
process_complete = threading.Event()
app = Flask(__name__)
CORS(app, resources={r"/post_video": {"origins": "*"}})

def make_video_path(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:', videoI_userId)
    output_path = "temporary_video.mp4"
    decoded_video_path = base64_to_video(base64_string, output_path)
    if decoded_video_path:
        result=main(decoded_video_path, videoI_userId)

    process_complete.set() #Signal that the process is complete

    print("Process complete. Signaling for restart...")
    with open("restart.txt", "w") as f:
        f.write("restart")
    print(result, type(result))
    return result




@app.route('/post_video', methods=['POST'])
def receive_data():
    data = request.get_json()
    try:
        # print(data, 'data from vicky')
        # print(data["videoBytes"],'videoBytes')
        video_base64=data["videoBytes"]
        # video_base64 = data['baseUrl']
        # print(data['baseUrl'],'baseUrl')
        videoI_userId = {"userId": data['userId'], 'videoId': data['id']}
        
        # Process the video in a separate thread
        process_complete.clear()
        # threading.Thread(target=make_video_path, args=(base64_string, videoI_userId)).start() #
        
        '''to get rerun data from main function'''
        def threaded_function(q, video_base64, videoI_userId):
            #to analyze the video and audio
            # analyzer = VideoAudioAnalysis(video_base64, data['id'], data['userId'])
            # format_info = analyzer.get_video_format()
            # print(format_info)
        

            result = make_video_path(video_base64, videoI_userId)
            q.put(result)

        q = queue.Queue()
        thread = threading.Thread(target=threaded_function, args=(q, video_base64, videoI_userId))
        thread.start()

        # Get the result
        result = q.get()
        print('result:',result, type(result))
        thread.join()
        # Wait for the process to complete
        process_complete.wait()
        
        # Prepare and send the response after processing is complete
        response = jsonify({'message': result})
        print('Restarting app...')
        return response, 200  # 200 OK

    except Exception as e:
        response = jsonify({'message': 'Error processing request', 'error': str(e),'result':result})
        return response, 500

def run_flask_app():
    if __name__ == '__main__':
        app.run(debug=True,host="192.168.1.7") #server: app.run(debug=True,host="192.168.1.29")

        # app.run(host='136.185.19.60', port=5006, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_flask_app()


