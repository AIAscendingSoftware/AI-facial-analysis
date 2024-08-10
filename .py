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


