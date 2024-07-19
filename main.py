from video_to_text import VideoToText
from getting_gestures_score import GestureAnalyzer
from video_to_audio_analyse import SpeechAnalyzer
from convert_video_to_base64 import video_to_base64, base64_to_video, converting_image_base64_into_image
from api import post_data, get_details,post_final_data
import os,json
from handling_db import insert_video_scores



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

def main(video_path, videoI_userId):
    # vedio_details={"userId":data['userId'],"videoId":data['videoId'] } #we can add if java backend need any data
    vedio_details=videoI_userId
    # print(vedio_details)
    # Video to Text
    video_to_text = VideoToText(video_path)
    transcribed_text = video_to_text.get_transcribed_text()
    print("Transcribed Text:", transcribed_text)

    # Gesture Analysis
    gesture_analyzer = GestureAnalyzer(video_path)
    gesture_analyzer.analyze_gestures()
    gesture_results = gesture_analyzer.get_results()
    # print("\nGesture Analysis Results:")
    print(gesture_results)

    # Speech Analysis
    speech_analyzer = SpeechAnalyzer(video_path)
    speech_scores = speech_analyzer.analyze(transcribed_text)
    print('speech_scores:',speech_scores, type(speech_scores))
    
    
    combined_dict = {**gesture_results, **speech_scores, **vedio_details}

    fcialScore=(combined_dict['happy']+combined_dict['neutral']+combined_dict['surprise']+combined_dict['angry']+combined_dict['fear']+combined_dict['disgust']+combined_dict['sad']+combined_dict['faceConfidence'])/8
    communicationScore=(combined_dict['fluency']*100 + combined_dict['grammar']*100 +combined_dict['pronunciation'])/3
    speechScore=(combined_dict['tone']*100 + combined_dict['voiceConfidence']*100)/2
    bodyLanguageScore=(combined_dict['lookingStraight']+combined_dict['smileCount']+combined_dict['handUsage']+combined_dict['armsCrossed']+combined_dict['wristsClosed']+combined_dict['weightOnOneLeg']+combined_dict['legMovement']+combined_dict['weightBalancedOnBothLegs']+combined_dict['eyeContact'])/9
    overAllScroe=(fcialScore+communicationScore+speechScore+bodyLanguageScore)/4
    wanted_data={"overAllScroe": float(f"{overAllScroe:.2f}"), "fcialScore": float(f"{fcialScore:.2f}"),"communicationScore": float(f"{communicationScore:.2f}"),"bodyLanguageScore": float(f"{bodyLanguageScore:.2f}"), "speechScore": float(f"{speechScore:.2f}")}
    
    combined_dict={**combined_dict, **wanted_data }
    
    # print(combined_dict, len(combined_dict), type(combined_dict))
    insert_data_on_insert_video_scores=(combined_dict['angry'], combined_dict['armsCrossed'], combined_dict['bodyLanguageScore'], combined_dict['communicationScore'], combined_dict['disgust'], combined_dict['eyeContact'], combined_dict['faceConfidence'], combined_dict['fcialScore'], combined_dict['fear'], combined_dict['fluency'], combined_dict['grammar'], combined_dict['handUsage'], combined_dict['happy'], combined_dict['legMovement'], combined_dict['lookingStraight'], combined_dict['neutral'], combined_dict['overAllScroe'], combined_dict['pronunciation'], combined_dict['sad'], combined_dict['smileCount'], combined_dict['speechRate'], combined_dict['speechScore'], combined_dict['surprise'], combined_dict['tone'], combined_dict['userId'], combined_dict['videoId'], combined_dict['voiceConfidence'], combined_dict['voiceGraphBase64'], combined_dict['weightBalancedOnBothLegs'], combined_dict['weightOnOneLeg'], combined_dict['wristsClosed'])
  
    insert_video_scores_=insert_video_scores(insert_data_on_insert_video_scores)
    print(insert_video_scores_)
    print('userI for get_details api:',combined_dict['userId'], type(combined_dict['userId']))
    result = get_details(combined_dict['userId'])
    print(result, type(result), len(result), 'final result data')

    # final_out=json.dumps(result(combined_dict), indent=4)
    # print(final_out, len(final_out), type(final_out), 'final ou data')
    final_out = find_average(result)

    #to post final score
    post_final_data(final_out)


    # #To show the imaghe from image base64, enable if wa want the see, otherwise no need to enalbe
    # converting_image_base64_into_image(combined_dict["voiceGraphBase64"])

    # # print(combined_dict, len(combined_dict),type(combined_dict))
    # response_from_post=post_data(combined_dict)
    # print(response_from_post)



# '''triggering main using video path'''
# if __name__ == "__main__":
#     video_path = r"C:\Users\prani\OneDrive\Pictures\Camera Roll\WIN_20240716_12_38_55_Pro.mp4"
#     # output_path = "temporary_video.mp4"
#     # Convert video to Base64
#     base64_string = video_to_base64(video_path)
    
#     output_path = "temporary_video.mp4"
#     # Convert Base64 back to video
#     decoded_video_path=base64_to_video(base64_string, output_path)
    
#     if decoded_video_path:
#         data={"videoId": 1,"userId": 1}

#         main(decoded_video_path,data)
        
#         if os.path.exists(decoded_video_path):
#             os.remove(decoded_video_path)
#             print(f"Removed temporary video file: {decoded_video_path}")
#         else:
#             print(f"Temporary video file not found: {decoded_video_path}")
#     else:
#         print("Error decoding video to Base64.")
  


