from app.utils.getting_gestures_score import GestureAnalyzer
from app.utils.video_to_audio_analyse import SpeechAnalyzer
from api import APIs
from app.utils.converting_video_to_audio import VideoToAudio
from app.utils.audio_to_text import audioToText
from app.config import Config
from app.static.statistics import find_average


class VideoProcessing:
    def __init__(self, video_path, videoI_userId):
        self.video_path = video_path
        self.videoI_userId = videoI_userId
        self.api_object = APIs()
        self.audio_output_path = Config.audio_path
    
    def convert_video_to_audio(self):
        video_to_audio_object = VideoToAudio(self.video_path, self.audio_output_path)
        result = video_to_audio_object.video_to_audio_ffmpeg()
        print("result from convert_video_to_audio method:", result)
        if result is None:
            raise ValueError("There is no audio to extract. Please check if the video has human voices in English or not")
            # return "There is no audio to extract. Please check if the video has English audio."
        print(f"Audio file created at: {result}")

    def convert_audio_to_text(self):
        audioToText_object = audioToText(self.audio_output_path)
        transcribed_text = audioToText_object.transcribe_audio()
        if transcribed_text is None:
            raise ValueError("There are no human voices in the video")
        print("Transcribed Text:", transcribed_text)
        return transcribed_text

    def analyze_gestures(self):
        gesture_analyzer = GestureAnalyzer(self.video_path)
        gesture_analyzer.analyze_gestures()
        return gesture_analyzer.get_results()

    def analyze_speech(self, transcribed_text):
        speech_analyzer = SpeechAnalyzer()
        print("Analyzing speech...")
        return speech_analyzer.analyze(transcribed_text, self.audio_output_path)

    def combine_results(self, gesture_results, speech_scores):
        combined_dict = {**gesture_results, **speech_scores, **self.videoI_userId}
        fcialScore = (combined_dict['happy'] + combined_dict['nautral'] + combined_dict['surprise'] +
                      combined_dict['angry'] + combined_dict['fear'] + combined_dict['disgust'] +
                      combined_dict['sad'] + combined_dict['faceConfidence']) / 8
        communicationScore = (combined_dict['fluency'] * 100 + combined_dict['grammar'] * 100 +
                              combined_dict['pronunciation'] * 100) / 3
        speechScore = (combined_dict['tone'] * 100 + combined_dict['voiceConfidence'] * 100) / 2
        bodyLanguageScore = (combined_dict['lookingStraight'] + combined_dict['smileCount'] +
                             combined_dict['handUsage'] + combined_dict['armsCrossed'] +
                             combined_dict['wristsClosed'] + combined_dict['weightOnOneLeg'] +
                             combined_dict['legMovement'] + combined_dict['weightBalancedOnBothLegs'] +
                             combined_dict['eyeContact']) / 9
        overAllScore = (fcialScore + communicationScore + speechScore + bodyLanguageScore) / 4
        
        wanted_data = {
            "overAllScore": overAllScore,
            "fcialScore": fcialScore,
            "communicationScore": communicationScore,
            "bodyLanguageScore": bodyLanguageScore,
            "speechScore": speechScore
        }
        print('wanted_data:',wanted_data)
        one_video_data = {
            "userId": self.videoI_userId["userId"],
            "videoId": self.videoI_userId["videoId"],
            "overAllScore": round(overAllScore, 2),
            "fcialScore": round(fcialScore*10, 2),
            "happy": combined_dict['happy'],
            "nautral": combined_dict["nautral"],
            "surprise": combined_dict['surprise'],
            "angry": combined_dict['angry'],
            "disgust": combined_dict['disgust'],
            "fear": combined_dict['fear'],
            "sad": combined_dict['sad'],
            "faceConfidence": combined_dict["faceConfidence"],
            "communicationScore": round(communicationScore, 2),
            "grammar": round(combined_dict["grammar"] * 10, 2),
            "fluency": round(combined_dict["fluency"] * 10, 2),
            "pronunciation": round(combined_dict["pronunciation"] * 10, 2),
            "speechScore": round(speechScore, 2),
            "tone": round(combined_dict["tone"] * 10, 2),
            "voiceConfidence": round(combined_dict["voiceConfidence"] * 10, 2),
            "speechRate": round(combined_dict["speechRate"], 2),
            "bodyLanguageScore": round(bodyLanguageScore*10, 2),
            "lookingStraight": combined_dict["lookingStraight"],
            "smileCount": combined_dict["smileCount"],
            "handUsage": combined_dict["handUsage"],
            "armsCrossed": combined_dict["armsCrossed"],
            "wristsClosed": combined_dict["wristsClosed"],
            "weightOnOneLeg": combined_dict["weightOnOneLeg"],
            "legMovement": combined_dict["legMovement"],
            "weightBalancedOnBothLegs": combined_dict["weightBalancedOnBothLegs"],
            "eyeContact": combined_dict["eyeContact"],
            "voiceGraphBase64": combined_dict["voiceGraphBase64"]
        }
        print('one_video_data:', one_video_data, type(one_video_data),len(one_video_data))
        return one_video_data

    def post_results(self, one_video_data):
        post_video_result = self.api_object.post_one_video_result(one_video_data)
        print('Post video result:', post_video_result)
        result = self.api_object.get_details(self.videoI_userId['userId'])
        print(result, 'Final result data')
        final_out = find_average(result)
        print('Final output:', final_out)
        self.api_object.post_final_data(final_out)
       
        
    def process(self):
        try:
            # self.convert_video_to_audio()
            # transcribed_text = self.convert_audio_to_text()
            gesture_results = self.analyze_gestures()
            # speech_scores = self.analyze_speech(transcribed_text)
            # one_video_data = self.combine_results(gesture_results, speech_scores)
            # self.post_results(one_video_data) #to push analyzed data and pull that user existing data to calculate their average and then post those calculated data
            return 'Data processed successfully completed!'
        except ValueError as e:
            return str(e)
 