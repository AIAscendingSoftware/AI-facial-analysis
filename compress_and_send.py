import base64, requests
import io, os
import tempfile
from moviepy.editor import VideoFileClip

def post_compreshed_data(postable_data):
    url = "http://192.168.29.223:8080/api/proCommunication/postvideo"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=postable_data, headers=headers)
    print('status code:', response.status_code)
    return response.json()

def compress_base64(base64_string, data, result_queue):
    print('you are in compress_base64 function')
    video_data = base64.b64decode(base64_string)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(video_data)
        temp_file_path = temp_file.name

    output_buffer = io.BytesIO()
    with VideoFileClip(temp_file_path) as clip:
        clip_resized = clip.resize(height=360)
        clip_resized.write_videofile(temp_file_path, codec='libx264', bitrate='500k')

    with open(temp_file_path, 'rb') as temp_file:
        compressed_video_data = temp_file.read()

    compressed_base64_string = base64.b64encode(compressed_video_data).decode('utf-8')
    print('compressed_base64_string:', type(compressed_base64_string))
    os.remove(temp_file_path)
    
    postable_data = {
        "baseUrl": compressed_base64_string,
        "userId": data['userId'],
        "videoName": "rty",
        "videoType": "tyuy",
        "dateAndTime": "yt",
        "byteSize": "rt",
        "videoCategory": "rth"
    }
    
    result = post_compreshed_data(postable_data)
    print('result from post_compreshed:',result)
    result_queue.put(result)
    return result




# import base64, requests
# import io,os
# import tempfile
# from moviepy.editor import VideoFileClip
# import queue

# def post_compreshed_data(postable_data):
#     # The URL for the API endpoint
#     url = "http://192.168.29.223:8080/api/proCommunication/postvideo"

#     # The JSON data to be posted
#     data = postable_data

#     # Set the headers for the request
#     headers = {
#         "Content-Type": "application/json"
#     }

#     # Post the JSON data to the URL
#     response = requests.post(url, json=data, headers=headers)

#     # Print the response from the server
#     print('status code:',response.status_code)
#     return response.json()
  


# def compress_base64(base64_string,data):
#     print('you are in compress_base64 function ')
#     video_data = base64.b64decode(base64_string)
    
#     # Save the video data to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
#         temp_file.write(video_data)
#         temp_file_path = temp_file.name

#     # Create an output buffer to store the compressed video
#     output_buffer = io.BytesIO()

#     # Use moviepy with imageio-ffmpeg to read and compress the video from the temp file
#     with VideoFileClip(temp_file_path) as clip:
#         clip_resized = clip.resize(height=360)  # Example: resize the video to height 360 pixels
#         # Write the resized video to the output buffer
#         clip_resized.write_videofile(temp_file_path, codec='libx264', bitrate='500k')

#     # Read the compressed video data from the temporary file
#     with open(temp_file_path, 'rb') as temp_file:
#         compressed_video_data = temp_file.read()

#     compressed_base64_string = base64.b64encode(compressed_video_data).decode('utf-8')
#     print('compressed_base64_string:', type(compressed_base64_string))

#     # Clean up the temporary file
#     os.remove(temp_file_path)
#     postable_data = {
#         "baseUrl": compressed_base64_string,
#         "userId": data['userId'],
#         "videoName":"rty",
#         "videoType":"tyuy",
#         "dateAndTime":"yt",
#         "byteSize":"rt",
#         "videoCategory":"rth"
       
#     }
#     # post_compreshed_data(postable_data)
#     result=post_compreshed_data(postable_data)
#     print(result)
#     return result
#     # return video_details
#     # result_queue.put(result)
#     # return compressed_base64_string



