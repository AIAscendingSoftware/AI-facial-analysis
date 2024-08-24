# # from convert_video_to_base64 import video_to_base64, base64_to_video
# import requests
# # from google.colab.output import eval_js

# video_path = "/content/drive/MyDrive/AI facial analysis/flask_api/3s 2mb.mp4"

# # Convert video to base64
# # base64_string = video_to_base64(video_path)

# # Convert base64 back to video (optional, for checking)
# output_path = "temporary_video.mp4"
# # video_path = base64_to_video(base64_string, output_path)
# print(video_path)

# data = {
#     'baseUrl': 'base64_string',
#     'size': 'gh',
#     'lastModifiedDate': 'gh',
#     'userId': 1,
#     'id': 1,
#     'videoCategory': 'gh',
#     'name': 'gh',
#     'type': 'gh'
# }

# def post_data(data):
#     public_url = "https://y01sc8fnlgm-496ff2e9c6d22116-5000-colab.googleusercontent.com/"  # Replace with your public URL
#     url = f'{public_url}/post_video'
    
#     response = requests.post(url, json=data)
    
#     if response.status_code == 200:
#         return response.text
#     else:
#         return f'Response Text: {response.text}, and response.status_code: {response.status_code}'

# post_video_data = post_data(data)
# print(post_video_data)
# import base64
# import re

# def is_base64(s: str) -> bool:
#     # Check if string length is a multiple of 4
#     if len(s) % 4 != 0:
#         return False
    
#     # Check if string consists of valid base64 characters
#     base64_pattern = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')
#     if not base64_pattern.match(s):
#         return False
    
#     # Try to decode the string using base64
#     try:
#         base64.b64decode(s, validate=True)
#         return True
#     except ValueError:
#         return False

# def base64_to_video(base64_string, output_path):
#     # Validate the base64 string
#     if not is_base64(base64_string):
#         return "Invalid Base64 string"

#     try:
#         # Decode the Base64 string back to bytes
#         video_bytes = base64.b64decode(base64_string)
        
#         # Write the bytes to a video file
#         with open(output_path, "wb") as video_file:
#             video_file.write(video_bytes)
        
#         return output_path

#     except Exception as e:
#         return f"Error decoding Base64 and saving video: {e}"
# data = {
#     'baseUrl': "base64_string",
#     'size': 'gh',
#     'lastModifiedDate': 'gh',
#     'userId': 1,
#     'id':1,
#     'videoCategory': 'gh',
#     'name': 'gh',
#     'type': 'gh'
# }
# base64_string = data['baseUrl']
# output_path = "output_video.mp4"

# result = base64_to_video(base64_string, output_path)
# print(result)  # Will either print the path to the saved video or an error message

'''frame_interval = max(1, int(original_fps / self.target_fps))'''
# frame_interval = max(1, int(10/ 14))
# # print('frame_interval:', frame_interval, type(frame_interval))
# a=int(30/ 15)

# print('a:',a, type(a))

# a=556%10
# print(a)

# d='ghf'+'rrr'
# print(d)

# def process_audio(audio_data):
#     if audio_data is None:
#         # raise ValueError("There is no audio to extract.")
#         raise TypeError('there is no audio to extrat')
#     # Process the audio data
#     return "Processed Audio"

# try:
#     result = process_audio(None)
# except TypeError as e:
#     print(f"Error occured as {e}")


# class necessary_paths:
#     video_path="extracted_audio.wav"
#     audio_path="extracted_audio.wav"


# audio_path=necessary_paths.audio_path
# print(audio_path)

a=15 % 1
print(a)