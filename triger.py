from convert_video_to_base64 import video_to_base64, base64_to_video
import requests

video_path=r"C:\Users\prani\OneDrive\Pictures\Camera Roll\WIN_20240716_12_38_55_Pro.mp4" #grafhic card Time taken: 0.33 minutes, local cpu Time taken: 0.77 minutes
# video_path = r"E:\AI Ascending Software\AS AI Projects\videos for AI facial anlysis\1m 3mb.mp4" #grafhic cardTime taken: 4.00 minutes,local cpu Time taken: 6.72 minutes,
# video_path=r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\3m 8mb.mp4" #Time taken: 9.27 minutes
# video_path=r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\5m 10mb.mp4" #Time taken: 15.51 minutes
# video_path=r"D:\AI Projects\AI facial analysis\videos for AI facial anlysis\10m 20mb.mp4" #Time taken: 33.22 minutes

base64_string = video_to_base64(video_path)

output_path = "temporary_video.mp4"
video_path = base64_to_video(base64_string, output_path)
print(video_path)

data = {
    'baseUrl': base64_string,
    'size': 'gh',
    'lastModifiedDate': 'gh',
    'userId': 1,
    'videoCategory': 'gh',
    'name': 'gh',
    'type': 'gh'
}

def post_data(data):
    url = 'http://192.168.43.216:5000/post_video'
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return 'POST request successful.'
    else:
        print(f'Response Text: {response.text}')
        return f'POST request failed with status code: {response.status_code}'

post_video_data = post_data(data)
print(post_video_data)