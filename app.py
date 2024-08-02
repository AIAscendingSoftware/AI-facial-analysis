
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
        print(data, 'data from vicky')
        video_base64 = data['baseUrl']
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
        app.run(debug=True,host="192.168.29.125",port=5000) #server: app.run(debug=True,host="192.168.1.29")

        # app.run(host='136.185.19.60', port=5006, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_flask_app()




'rerun app after getting error ad return the respones after completing process'
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import threading, os, time
# from main_ import main
# from convert_video_to_base64 import base64_to_video
# from handling_db import insert_video_details
# from kinds import restart_app

# app = Flask(__name__)
# CORS(app, resources={r"/post_video": {"origins": "*"}})

# def make_video_path(base64_string, videoI_userId):
#     print('you are in make_video_path function')
#     print('videoId:',videoI_userId)
#     output_path = "temporary_video.mp4"
#     decoded_video_path = base64_to_video(base64_string, output_path)
#     # print(decoded_video_path)
#     if decoded_video_path:
#         main(decoded_video_path,  videoI_userId)
#         if os.path.exists(decoded_video_path):
#             os.remove(decoded_video_path)
#             print(f"Removed temporary video file: {decoded_video_path}")
#         else:
#             print(f"Temporary video file not found: {decoded_video_path}")
#     else:
#         print("Error decoding video to Base64.")

# @app.route('/post_video', methods=['POST'])

# def receive_data():

#     try:
#         print('request data:', request)
#         data = request.get_json()
#         # print(data,'data from vicky')
#         print("------------------------")
#         base64_string = data['baseUrl']
#         # print()
#         # base64_string = base64_string.split(',', 1)[1]

#         # Insert video details and get videoId
#         # video_data = (base64_string, data['size'], data['lastModifiedDate'], data['userId'], data['videoCategory'], data['name'], data['type'])
#         # insert_video_and_get_id = insert_video_details(video_data)
#         # print(insert_video_and_get_id)
#         # videoId = insert_video_and_get_id['id']
#         # videoId=1
#         # videoI_userId = {"userId": data['userId'], 'videoId': 1} 
#         videoI_userId = {"userId": data['userId'], 'videoId': data['id']}
    
#         # Process the video
#         make_video_path(base64_string, videoI_userId)

#         # Prepare and send the response
#         response = jsonify({'message': 'Data processed and stored successfully'})

#         return response, 200

#     except Exception as e:
#         response = jsonify({'message': 'Error processing request', 'error': str(e)})

#         return response
    
# if __name__ == '__main__':
#     app.run(host='192.168.29.216', port=5000, debug=True)
# #server host='136.185.19.60'port='5006', 



# 'rerun app after completing process amd return the respones immediately'
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import threading, os, time, sys
# from main_ import main
# from convert_video_to_base64 import base64_to_video
# from handling_db import insert_video_details
# from kinds import restart_app

# app = Flask(__name__)
# CORS(app, resources={r"/post_video": {"origins": "*"}})

# process_complete = threading.Event()

# def make_video_path(base64_string, videoI_userId):
#     print('you are in make_video_path function')
#     print('videoId:', videoI_userId)
#     output_path = "temporary_video.mp4"
#     decoded_video_path = base64_to_video(base64_string, output_path)
#     if decoded_video_path:
#         main(decoded_video_path, videoI_userId)
#         if os.path.exists(decoded_video_path):
#             os.remove(decoded_video_path)
#             print(f"Removed temporary video file: {decoded_video_path}")
#         else:
#             print(f"Temporary video file not found: {decoded_video_path}")
#     else:
#         print("Error decoding video to Base64.")
    
#     print("Process complete. Signaling for restart...")
#     os._exit(0)  # Force exit the entire process

# @app.route('/post_video', methods=['POST'])
# def receive_data():
#     try:
#         print('request data:', request)
#         data = request.get_json()
#         base64_string = data['baseUrl']
#         videoI_userId = {"userId": data['userId'], 'videoId': data['id']}
        
#         # Process the video in a separate thread
#         threading.Thread(target=make_video_path, args=(base64_string, videoI_userId)).start()

#         # Prepare and send the response
#         response = jsonify({'message': 'Data processing started'})
#         return response, 202  # 202 Accepted

#     except Exception as e:
#         response = jsonify({'message': 'Error processing request', 'error': str(e)})
#         return response, 500

# def run_flask_app():
#     app.run(host='192.168.1.25', port=5000, debug=False, use_reloader=False)

# if __name__ == '__main__':
#     run_flask_app()

