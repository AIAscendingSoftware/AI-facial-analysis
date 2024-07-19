import json
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
from api import post_final_data
def find_average(combined_dict):

    keys_to_ignore = {"id", "userId", "videoId", "voiceGraphBase64"}
    keys = [key for key in combined_dict[0].keys() if key not in keys_to_ignore]
    
    sums = {key: 0 for key in keys}
    count = len(combined_dict)
    
    for obj in combined_dict:
        for key in keys:
            sums[key] += obj[key]
    
    averages = {key: round(sums[key] / count, 2) for key in keys}

    average_dict = {
        "userId": combined_dict[0]["userId"],
        **averages,
        "voiceGraphBase64": "iVBORw0KGgoAAAANSUhEUgAADhAA"
    }
    
    return average_dict

final_out= find_average(data)
# final_out=(json.dumps(find_average(data), indent=4))
# final_out=dict(final_out)
post_final_data(final_out)
print(final_out, type(final_out), len(final_out))

