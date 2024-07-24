
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, os, time
from main_ import main
from convert_video_to_base64 import base64_to_video
from handling_db import insert_video_details

app = Flask(__name__)
CORS(app, resources={r"/post_video": {"origins": "*"}})

def make_video_path(base64_string, videoI_userId):
    print('you are in make_video_path function')
    print('videoId:',videoI_userId)
    output_path = "temporary_video.mp4"
    decoded_video_path = base64_to_video(base64_string, output_path)
    
    if decoded_video_path:
        main(decoded_video_path,  videoI_userId)
        if os.path.exists(decoded_video_path):
            os.remove(decoded_video_path)
            print(f"Removed temporary video file: {decoded_video_path}")
        else:
            print(f"Temporary video file not found: {decoded_video_path}")
    else:
        print("Error decoding video to Base64.")

@app.route('/post_video', methods=['POST'])

def receive_data():

    try:
        print('request data:', request)
        data = request.get_json()
        # print(data,'data from vijay')
        print("------------------------")
        base64_string = data['baseUrl']
        # base64_string = base64_string.split(',', 1)[1]

        # Insert video details and get videoId
        # video_data = (base64_string, data['size'], data['lastModifiedDate'], data['userId'], data['videoCategory'], data['name'], data['type'])
        # insert_video_and_get_id = insert_video_details(video_data)
        # print(insert_video_and_get_id)
        # videoId = insert_video_and_get_id['id']
        videoId=1
        videoI_userId = {"userId": data['userId'], "videoId": videoId}

        # Process the video
        make_video_path(base64_string, videoI_userId)

        # Prepare and send the response
        response = jsonify({'message': 'Data processed successfully', "videoId": videoId})
        return response, 200

    except Exception as e:
        response = jsonify({'message': 'Error processing request', 'error': str(e)})
        return response

if __name__ == '__main__':
    app.run(host='192.168.29.125', port=5000, debug=True)
#server host='136.185.19.60'port='5006', 





