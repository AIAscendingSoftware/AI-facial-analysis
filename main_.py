


from getting_gestures_score import GestureAnalyzer
from video_to_audio_analyse import SpeechAnalyzer
from convert_video_to_base64 import video_to_base64, base64_to_video, converting_image_base64_into_image
from api import APIs
import time
from converting_video_to_audio import VideoToAudio
from audio_to_text import audioToText
API_object=APIs()


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
    print('you are in main with:',video_path, videoI_userId)
    start_time = time.time()
    # vedio_details={"userId":data['userId'],"videoId":data['videoId'] } #we can add if java backend need any data
    vedio_details=videoI_userId
    # print(vedio_details)
    
    #converting video to audio an save the audio
    audio_output_path="extracted_audio.wav"
    video_to_audio_object = VideoToAudio(video_path, audio_output_path)
    result = video_to_audio_object.video_to_audio_ffmpeg()
    if result is None:
        return "There is no audio to extract, so kindly check the whether the video has english audio or not."
    else:
        print(f"Audio file created at: {result}")

    #converting audio to text
    audioToText_object=audioToText(audio_output_path)
    transcribed_text=audioToText_object.transcribe_audio()
    print("Transcribed Text:", transcribed_text)
    if transcribed_text is None: 
        return "There is no audio to extract, so kindly check the whether the video has english audio or not."

    # # Gesture Analysis
    gesture_analyzer = GestureAnalyzer(video_path)
    gesture_analyzer.analyze_gestures()
    gesture_results = gesture_analyzer.get_results()
    print("Gesture Analysis Results:")
    print(gesture_results)

    # Speech Analysis
    speech_analyzer = SpeechAnalyzer()
    print("you are in speech_analyzer and going to get speech_scores ")
    speech_scores = speech_analyzer.analyze(transcribed_text, audio_output_path)
    print('speech_scores:',speech_scores, type(speech_scores))

    # #to combine necessary values
    combined_dict = {**gesture_results, **speech_scores, **vedio_details}
    fcialScore=(combined_dict['happy']+combined_dict['nautral']+combined_dict['surprise']+combined_dict['angry']+combined_dict['fear']+combined_dict['disgust']+combined_dict['sad']+combined_dict['faceConfidence'])/8
    communicationScore=(combined_dict['fluency']*100 + combined_dict['grammar']*100 +combined_dict['pronunciation']*100)/3
    speechScore=(combined_dict['tone']*100 + combined_dict['voiceConfidence']*100)/2
    bodyLanguageScore=(combined_dict['lookingStraight']+combined_dict['smileCount']+combined_dict['handUsage']+combined_dict['armsCrossed']+combined_dict['wristsClosed']+combined_dict['weightOnOneLeg']+combined_dict['legMovement']+combined_dict['weightBalancedOnBothLegs']+combined_dict['eyeContact'])/9
    overAllScroe=(fcialScore+communicationScore+speechScore+bodyLanguageScore)/4
    wanted_data={"oveAllScroe": float(f"{overAllScroe:.2f}"), "fcialScore": float(f"{fcialScore:.2f}"),"communicationScore": float(f"{communicationScore:.2f}"),"bodyLanguageScore": float(f"{bodyLanguageScore:.2f}"), "speechScore": float(f"{speechScore:.2f}")}
    print('wanted_data:',wanted_data)   
    print(combined_dict, len(combined_dict), type(combined_dict))

    one_video_data={
    "userId": vedio_details["userId"],
    "videoId":vedio_details["videoId"],
    "overAllScroe": round(wanted_data["oveAllScroe"],2),
    "fcialScore": round(wanted_data["fcialScore"],2),
    "happy": round(combined_dict['happy']/10,2),
    "nautral": round(combined_dict["nautral"]/10,2),
    "surprise": round(combined_dict['surprise']/10,2),
    "angry": round(combined_dict['angry']/10,2),
    "disgust": round(combined_dict['disgust']/10,2),
    "fear": round(combined_dict['fear']/10,2),
    "sad": round(combined_dict['sad']/10,2),
    "faceConfidence": round(combined_dict["faceConfidence"]/10,2),
    "communicationScore": round(wanted_data["communicationScore"],2),
    "grammar": round(combined_dict["grammar"]*10,2),
    "fluency": round(combined_dict["fluency"]*10,2),
    "pronunciation": round(combined_dict["pronunciation"]*10,2),
    "speechScore": round(wanted_data["speechScore"],2),
    "tone": round(combined_dict["tone"]*10,2),
    "voiceConfidence": round(combined_dict["voiceConfidence"]*10,2),
    "speechRate": round(combined_dict["speechRate"],2),
    "bodyLanguageScore": round(wanted_data["bodyLanguageScore"],2),
    "lookingStraight": round(combined_dict["lookingStraight"]/10,2),
    "smileCount": round(combined_dict["smileCount"]/10,2),
    "handUsage": round(combined_dict["handUsage"]/10,2),
    "armsCrossed": round(combined_dict["armsCrossed"]/10,2),
    "wristsClosed": round(combined_dict["wristsClosed"]/10,2),
    "weightOnOneLeg": round(combined_dict["weightOnOneLeg"]/10,2),
    "legMovement": round(combined_dict["legMovement"]/10,2),
    "weightBalancedOnBothLegs": round(combined_dict["weightBalancedOnBothLegs"]/10,2),
    "eyeContact": round(combined_dict["eyeContact"]/10,2),
    "voiceGraphBase64": combined_dict["voiceGraphBase64"]
    }
    print("one_video_data:",one_video_data, type(one_video_data), len(one_video_data))
    post_video_result=API_object.post_one_video_result(one_video_data)
    print('post_video_result:',post_video_result)
    # print(vedio_details['userId'], type(vedio_details['userId']))
    result = API_object.get_details(vedio_details['userId'])
    print(result, type(result), len(result), 'final result data')
    # final_out=json.dumps(result(combined_dict), indent=4)
    # print(final_out, len(final_out), type(final_out), 'final ou data')
    final_out = find_average(result)
    print('final_out:',final_out)
    #to post final score
    API_object.post_final_data(final_out)
    end_time = time.time()
    # # Calculate the time taken in seconds
    time_taken = end_time - start_time
    # # Convert seconds to minutes
    time_taken_minutes = time_taken / 60
    print(f"Time taken: {time_taken_minutes:.2f} minutes, start tiume: {start_time}, end time:{end_time}")
    
    return 'data processed successfuly finished'