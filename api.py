import requests
import json

url = 'http://192.168.29.216:5000/post_video'  # URL of your Flask API endpoint

# Example data to send
data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'john.doe@example.com'
}

# Convert data to JSON format
json_data = json.dumps(data)

# Set headers
headers = {'Content-Type': 'application/json'}

# Send POST request
response = requests.post(url, data=json_data, headers=headers)

# Print response
if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Failed:', response.status_code, response.text)