
# # data={"videoBase64": 'urlToupload',
# #  "file": 'fileToupload'}
# # # print(data['videoBase64'])

# # baseUrl='data:video/webm;base64,GkXfo6NChoEBQveBAULygQRC84EIQoKIbWF0cm9za2FCh4EEQoWBAhhTgGcB/////////xVJqWaZKtexgw9CQE2AhkNocm9tZVdBhkNo'
# # # Extracting the part after the comma
# # data_after_comma = baseUrl.split(',', 1)[1]

# # # print(data_after_comma)
# # data = {
# #     'Grammar Score': 1.0,
# #     'Fluency Score': 0.0,
# #     'Tone Score': 0.3076171875,
# #     'Confidence Score': 0.114430021494627,
# #     'Speech Rate': 72.28915662650603
# # }

# # a = {
# #     'happy': '0.00%',
# #     'neutral': '100.00%',
# #     'surprise': '0.00%',
# #     'angry': '0.00%',
# #     'fear': '0.00%',
# #     'disgust': '0.00%',
# #     'sad': '0.00%',
# #     'Average Face Detection Confidence': '0.92%',
# #     'Looking Straight': '100.00%',
# #     'Smile Count': '7.27%',
# #     'Hand Usage': '34.55%',
# #     'Arms Crossed': '96.36%',
# #     'Wrists Closed': '0.00%',
# #     'Weight on One Leg': '0.00%',
# #     'Leg Movement': '47.27%',
# #     'Weight Balanced on Both Legs': '0.00%',
# #     'Eye Contact Percentage': '100.00%'
# # }

# # # Combine both dictionaries into one
# # combined_dict = {**data, **a}

# # # print(combined_dict)
# # wanted_data={"oveAllScroe":float(90), "fcialScore":float(86),"communicationScore":float(95),"bodyLanguageScore":float(78), "speechScore":float(89)}
# # # print(wanted_data)
# # data_={'happy': '0.00%', 'neutral': '100.00%',
# #         'surprise': '0.00%', 'angry': '0.00%',
# #         'fear': '0.00%', 'disgust': '0.00%', 
# #         'sad': '0.00%', 'faceConfidence': '0.92%',
# #         'lookingStraight': '100.00%', 'smileCount': '7.27%',
# #         'handUsage': '34.55%', 'armsCrossed': '96.36%', 'wristsClosed': '0.00%',
# #         'weightOnOneLeg': '0.00%', 'legMovement': '47.27%', 'weightBalancedOnBothLegs': '0.00%',
# #         'eyeContact': '100.00%', 'grammar': '1.0', 'fluency': '0.0', 'tone': '0.3076171875',
# #         'voiceConfidence': '0.114430021494627', 'speechRate': '72.28915662650603',
# #         'pronunciation': '89', 'userId': 1, 'videoId': 7, 'oveAllScroe': 90.0,
# #         'fcialScore': 86.0, 'communicationScore': 95.0, 'bodyLanguageScore': 78.0,
# #         'speechScore': 89.0,"voiceGraphBase64": "voice_graph_base64"}

# # import requests
# # def post_compreshed_data(postable_data):
# #     # The URL for the API endpoint
# #     url = "http://192.168.29.223:8080/api/proCommunication/postvideo"

# #     # The JSON data to be posted
# #     data = postable_data

# #     # Set the headers for the request
# #     headers = {
# #         "Content-Type": "application/json"
# #     }

# #     # Post the JSON data to the URL
# #     response = requests.post(url, json=data, headers=headers)

# #     # Print the response from the server
# #     print(response.status_code)
# #     print(response.json())


# # postable_data = {
# #         "baseUrl": "compressed_base64_string",
# #         "userId": 1,
# #         "videoName":"rty",
# #         "videoType":"tyuy",
# #         "dateAndTime":"yt",
# #         "byteSize":"rt",
# #         "videoCategory":"rth"
       
# #     }
# # post_compreshed_data(postable_data)

# combined_dict={'happy': 0.0, 'neutral': 100.0, 'surprise': 0.0, 'angry': 0.0, 'fear': 0.0, 'disgust': 0.0,
#                 'sad': 0.0, 'faceConfidence': 0.9182794072411277, 'lookingStraight': 100.0,
#                   'smileCount': 7.2727272727272725, 'handUsage': 34.54545454545455,
#                     'armsCrossed': 96.36363636363636, 'wristsClosed': 0.0, 'weightOnOneLeg': 0.0,
#                       'legMovement': 47.27272727272727, 'weightBalancedOnBothLegs': 0.0, 'eyeContact': 100.0,
#                  'grammar': 1.0, 'fluency': 0.0, 'tone': 0.3076171875, 'voiceConfidence': 0.114430021494627,
#                    'speechRate': 72.28915662650603, 'voiceGraphBase64': 'voice_graph_base64',
#                      'pronunciation': 0.5, 'userId': 1, 'videoId': 1}
# fcialScore=(combined_dict['happy']+combined_dict['neutral']+combined_dict['surprise']+combined_dict['angry']+combined_dict['fear']+combined_dict['disgust']+combined_dict['sad']+combined_dict['faceConfidence'])/8

# # communicationScore=(combined_dict['fluency']*100 + combined_dict['grammar']*100 +combined_dict['pronunciation'])/3

# # speechScore=(combined_dict['tone']*100 + combined_dict['voiceConfidence']*100)/2

# # bodyLanguageScore=(combined_dict['lookingStraight']+combined_dict['smileCount']+combined_dict['handUsage']+combined_dict['armsCrossed']+combined_dict['wristsClosed']+combined_dict['weightOnOneLeg']+combined_dict['legMovement']+combined_dict['weightBalancedOnBothLegs']+combined_dict['eyeContact'])/9


# # overAllScroe=(fcialScore+communicationScore+speechScore+bodyLanguageScore)/4
# # a = 4
# # data={"seaf":float(f"{a:.2f}")}

# # print(data, type(data))
# import requests

# # URL to fetch data from
# url = "http://192.168.29.223:8080/api/proCommunication/getdetails/1"

# # Sending a GET request to the URL
# response = requests.get(url)

# # Checking if the request was successful
# if response.status_code == 200:
#     # Parsing the response JSON data
#     data = response.json()
#     print("Data fetched successfully:")
#     print(data)
# else:
#     print(f"Failed to fetch data. Status code: {response.status_code}")


data=[
    {
        "id": 1,
        "userId": 1,
        "videoId": 1,
        "overAllScroe": 27.51135705097983,
        "fcialScore": 12.614784925905141,
        "happy": 0.0,
        "nautral": 0.0,
        "surprise": 0.0,
        "angry": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "sad": 0.0,
        "faceConfidence": 0.9182794072411277,
        "communicationScore": 33.5,
        "grammar": 1.0,
        "fluency": 0.0,
        "pronunciation": 0.5,
        "speechScore": 21.10236044973135,
        "tone": 0.3076171875,
        "voiceConfidence": 0.114430021494627,
        "speechRate": 72.28915662650603,
        "bodyLanguageScore": 42.82828282828282,
        "lookingStraight": 100.0,
        "smileCount": 7.2727272727272725,
        "handUsage": 34.54545454545455,
        "armsCrossed": 96.36363636363636,
        "wristsClosed": 0.0,
        "weightOnOneLeg": 0.0,
        "legMovement": 47.27272727272727,
        "weightBalancedOnBothLegs": 0.0,
        "eyeContact": 100.0,
        "voiceGraphBase64": "voice_graph_base64"
    },
    {
        "id": 2,
        "userId": 1,
        "videoId": 2,
        "overAllScroe": 27.51135705097983,
        "fcialScore": 12.614784925905141,
        "happy": 0.0,
        "nautral": 0.0,
        "surprise": 0.0,
        "angry": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "sad": 0.0,
        "faceConfidence": 0.9182794072411277,
        "communicationScore": 33.5,
        "grammar": 1.0,
        "fluency": 0.0,
        "pronunciation": 0.5,
        "speechScore": 21.10236044973135,
        "tone": 0.3076171875,
        "voiceConfidence": 0.114430021494627,
        "speechRate": 72.28915662650603,
        "bodyLanguageScore": 42.82828282828282,
        "lookingStraight": 100.0,
        "smileCount": 7.2727272727272725,
        "handUsage": 34.54545454545455,
        "armsCrossed": 96.36363636363636,
        "wristsClosed": 0.0,
        "weightOnOneLeg": 0.0,
        "legMovement": 47.27272727272727,
        "weightBalancedOnBothLegs": 0.0,
        "eyeContact": 100.0,
        "voiceGraphBase64": "iVBORw0KGgoAAAANSUhEUgAADhAA"
    }
]


insert=(data['data'], data["data"])
print(insert)
