import requests
def post_data(data):
    # API endpoint URL
    url = 'http://192.168.29.223:8080/api/proCommunication/postDetails'

    # Making the POST request
    response = requests.post(url, json=data)

    # Checking the response
    if response.status_code == 200:
        return 'POST request successful.'
    else:
        print(response.text) 
        return f'POST request failed with status code: {response.status_code}'



def get_details(id):
    base_url = f"http://192.168.29.223:8080/api/proCommunication/getdetails/{id}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()  # Assuming the API returns JSON
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None



def post_final_data(data):
    url = "http://192.168.29.223:8080/api/proCommunication/postAllDetailsScore"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST finall request successful")
        print("Response:", response.json())
    else:
        print("POST final request failed")
        print("Status code:", response.status_code)
    print("Response:", response.text)
# data={'usderId':1, "angry":2}
# post_final_data(data)
# # Example usage
# id = 1  # This can be any value you want to pass
# result = get_details(id)

# if result:
#     print(result)
# else:
#     print("Failed to retrieve data")

# import requests
# import json

# url = 'http://192.168.29.216:5000/post_video'  # URL of your Flask API endpoint

# # Example data to send
# data = {
#     'name': 'John Doe',
#     'age': 30,
#     'email': 'john.doe@example.com'
# }

# # Convert data to JSON format
# json_data = json.dumps(data)

# # Set headers
# headers = {'Content-Type': 'application/json'}

# # Send POST request
# response = requests.post(url, data=json_data, headers=headers)

# # Print response
# if response.status_code == 200:
#     print('Success:', response.json())
# else:
#     print('Failed:', response.status_code, response.text)