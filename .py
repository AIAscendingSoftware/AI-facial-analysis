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

def process_audio(audio_data):
    if audio_data is None:
        # raise ValueError("There is no audio to extract.")
        raise TypeError('there is no audio to extrat')
    elif audio_data is None:
        print('dsg')
    else:
        print('jji')
    # Process the audio data
    return "Processed Audio"

try:
    result = process_audio(None)
except TypeError as e:
    print(f"Error occured as {e}")

# process_audio(None)

# class necessary_paths:
#     video_path="extracted_audio.wav"
#     audio_path="extracted_audio.wav"


# audio_path=necessary_paths.audio_path
# print(audio_path)

a=(15**2)
# print(a)
# import numpy as np
# a=np.sqrt(25)
# # print(a)
# c=int(8.458336757781179e-06)
# # print(type(c),c)
# import numpy as np

# data = {'happy': [0.0005124567295126976, 0.0005374122793000424, 0.0003223366775273462, 0.0003083065166720189, 0.00022041744109199264, 4.010426356985951e-05, 1.903873510193311e-05, 1.2573278240779473e-05, 6.716470011269848e-05, 2.9130338754683397e-05, 1.4072816995645676e-05, 4.162613932387224e-05, 0.0001172989414044423, 0.0003590185087887221, 0.0001138036054726399, 8.915365015127463e-05, 6.378718353516888e-05, 7.889090625212702e-05, 8.807169164695803e-05, 0.0003899821422237437, 9.485684696895835e-05, 8.750029631702948e-05, 9.814706930425595e-05, 0.0014492613445327152, 0.0030555725970771164, 0.00036014018860441865, 5.77431115145851e-05, 0.00011025525736840791, 0.0001294535536544572, 0.0010811904758156743, 1.2544705222926314e-05, 9.418794483981506e-06, 0.0007257463926748784, 0.0030824681743979454, 0.00036067585824639536, 0.00194744127623154, 0.00026405225526104914, 0.0013434910215437412, 0.01417052699252963, 0.0005691706974175759, 0.0015439914932358079, 0.023182423319667578, 0.012864660714602363, 0.0012132444680901244, 0.0001650007872076305, 0.0004062358129885979, 0.006061453677830286, 0.0011933035239053424, 0.005236739992697054, 0.0003769971726796939, 0.00024726195188537464, 0.00027867417884408496, 7.324738930947206e-05, 5.3105995657783326e-05, 7.600483398259967e-05], 'neutral': [96.84540070946208, 98.27663898468018, 96.72518968582153, 99.78950023651123, 99.86643194356155, 99.81215598438311, 99.87237452699986, 99.59481358528137, 99.8687207698822, 99.99152422052333, 99.8700201433909, 99.46190112375034, 99.35163259506226, 94.32588815689087, 97.52845764160156, 97.5936770439148, 94.3045437335968, 98.56712222099304, 98.58588559459277, 98.59119057655334, 99.86999630153157, 99.50303432363476, 98.33174337933919, 94.17174458503723, 95.40114998817444, 94.83252167701721, 99.6538221629752, 99.5201826095581, 98.678719997406, 93.26432943344116, 99.88868235878243, 99.06079167489956, 98.92546528133543, 99.82333183288574, 98.53891730308533, 97.79755460009304, 98.78202676773071, 88.67270350456238, 79.88066673278809, 94.81467604637146, 86.8268072605133, 87.87911534309387, 91.2008876324229, 94.88043785095215, 97.55495161473175, 98.41443300247192, 96.42213582992554, 97.13826775550842, 97.79676225223992, 98.98242354393005, 99.21705718142135, 98.73494505882263, 99.52700734138489, 99.69339964946506, 99.73447321262796], 'surprise': [5.8305208638393825e-05, 4.647410776215111e-05, 0.0010402090083516669, 6.598828008463897e-05, 7.0935290317552416e-06, 4.9625937438797e-07, 1.4121266109922927e-07, 4.416854437749862e-07, 9.003320755596178e-07, 2.444711252881513e-07, 5.9403485674014826e-08, 3.891003095050389e-07, 9.691751401419424e-07, 1.4069796350213437e-05, 1.3433366419235426e-06, 5.540741199183685e-07, 7.930671230838016e-07, 7.131891521794387e-07, 6.129057548268139e-07, 1.9580701504651188e-06, 1.3883673705554829e-06, 1.5854383640574167e-06, 4.042816100832166e-06, 9.736744459587499e-05, 0.00013343178579816595, 4.8456609391678285e-06, 9.949958783766305e-07, 1.2669985061108946e-06, 5.650163714676637e-06, 0.0001373244117530703, 2.7358508202011937e-07, 3.6462218752698024e-08, 3.994124380605113e-06, 4.748012258914969e-05, 2.4190509151367223e-06, 3.287627717289042e-05, 6.424928500337046e-06, 0.0002638101477714372, 0.0013255164958536625, 4.355972862413182e-05, 6.442783728743962e-05, 0.0034021093597402796, 0.0009832434120088148, 5.514763756764296e-05, 7.453510342608304e-06, 7.81477211830861e-06, 7.249715849866334e-06, 1.0836870245611863e-05, 1.3038370960689136e-05, 1.2457545039978868e-05, 8.458336757781179e-06, 9.335531103715766e-06, 3.484031907419194e-06, 1.1061013209616306e-06, 2.3788131994346275e-06], 'angry': [0.015638785726144376, 0.023322597553487867, 0.2552920486778021, 0.006739799573551863, 0.0021203053065222124, 0.004615141547296087, 0.002995248174826506, 0.039374863263219595, 0.009953287371899933, 0.0008840032788902338, 0.012881478364034197, 0.04391882917528053, 0.06193727604113519, 1.4413009397685528, 0.41264649480581284, 0.21020236890763044, 1.2496275827288628, 0.03787939785979688, 0.01684012295960983, 0.05981503054499626, 0.006684401558294612, 0.132879320070405, 0.6824412789905834, 1.9233239814639091, 0.3861130913719535, 0.5326482933014631, 0.0774118047713819, 0.07061649230308831, 0.6747763138264418, 4.238099232316017, 0.060503380486943155, 0.5140191716116173, 0.4877343133231588, 0.01830542169045657, 0.4829182755202055, 0.9144981005488694, 0.6405587308108807, 4.839659109711647, 4.311360418796539, 2.3397615179419518, 6.797895580530167, 0.8889258839190006, 0.9848380117021807, 1.2807788327336311, 0.6001333955834384, 0.5180092994123697, 0.2779970411211252, 0.5955449771136045, 0.2500390103040325, 0.3277973737567663, 0.17889001076012914, 0.3237807424739003, 0.16543290112167597, 0.10775955803376783, 0.08321753616996325], 'fear': [0.03751409665979038, 0.027383127599023283, 0.3736966522410512, 0.006995095463935286, 0.0034980798129710445, 0.0025955487761132015, 0.0008834342751440533, 0.0060794689488830045, 0.00511970829393249, 0.0006123166438032357, 0.0051134265369123764, 0.07940243595606815, 0.14845083933323622, 2.1532317623496056, 0.668221851810813, 0.760197639465332, 0.949103944003582, 0.9905090555548668, 0.9049172660609801, 0.6039062049239874, 0.0419657498698756, 0.03756691518172861, 0.09123077577796732, 0.9083767421543598, 1.7044037580490112, 2.6857785880565643, 0.044950723300544816, 0.06996949086897075, 0.10626828297972679, 0.3960245754569769, 0.0004851738884066035, 0.003468173078809005, 0.003255995955792015, 0.022448042000178248, 0.011679019371513277, 0.04995052884037965, 0.016261554264929146, 0.63416319899261, 3.5176604986190796, 0.19217648077756166, 0.5537122022360563, 3.819141536951065, 2.092524556370053, 0.7044331636279821, 0.15519086258898526, 0.14440285740420222, 0.26901105884462595, 0.35138344392180443, 0.1994190965540294, 0.05717879394069314, 0.06010330174734007, 0.07696442771703005, 0.025568046839907765, 0.00647444651286544, 0.02059453377085753], 'disgust': [6.017832541237334e-11, 6.445026803914011e-11, 4.124941707650542e-09, 1.5921070139882955e-12, 3.879756719118696e-13, 1.159260164845969e-13, 5.26200138664834e-14, 1.3026463791649366e-12, 1.8112401972670243e-13, 3.056019401387994e-15, 2.775546080295305e-13, 2.3150147755144555e-11, 2.0590311140128437e-10, 3.6059102925811715e-08, 4.456681204634272e-09, 1.3082715466516959e-09, 8.940390094913653e-09, 1.9820273894355367e-10, 1.1047117229934433e-10, 2.1016891352254596e-09, 1.642943827123919e-11, 8.211730396627724e-10, 2.547293777862329e-09, 3.2685718576175304e-07, 2.6086080517906396e-08, 1.3440766555294914e-08, 8.363870533448925e-11, 3.9642538383899417e-10, 5.1319799104776465e-09, 2.6069897351987947e-07, 5.2804397068223e-13, 2.0320929785508596e-12, 8.630338711971033e-11, 4.696030890538605e-11, 2.374743197225415e-10, 3.3316448809398688e-09, 1.4815343396534786e-09, 4.712012113827768e-07, 2.0498589492490282e-06, 4.02592126302892e-08, 1.2635433810359586e-07, 4.50686954422963e-07, 2.1589427089489567e-07, 2.6273958009248588e-08, 1.3217199744881577e-09, 7.852152088261288e-10, 2.183497965768666e-08, 7.2196859601803e-09, 1.0776688672400187e-08, 3.2017793364508274e-10, 7.201545019942806e-11, 5.055002857273783e-10, 3.7572888051708164e-11, 7.664132101680526e-12, 7.427764494341995e-12], 'sad': [3.1008720426711984, 1.6720717772841454, 2.644464187324047, 0.19639525562524796, 0.12772428633119381, 0.18058810558609895, 0.12372803913298483, 0.3597215283662081, 0.11613811366260052, 0.006951354488475831, 0.11197155776077854, 0.4147335450033599, 0.4378645680844784, 2.0792070776224136, 1.3905604369938374, 1.435837708413601, 3.4966599196195602, 0.4044102504849434, 0.492269418212106, 0.7447012234479189, 0.08125537908668096, 0.32643118956274925, 0.8944837909629221, 2.9950132593512535, 2.505148947238922, 1.9486894831061363, 0.22375666473100572, 0.33912158105522394, 0.5401001777499914, 2.1003294736146927, 0.05031671325701256, 0.42171252611056126, 0.5828159277329402, 0.13278410769999027, 0.966124888509512, 1.2360150731214925, 0.5608843173831701, 5.8518677949905396, 12.274820357561111, 2.652771584689617, 5.819982662796974, 7.386229932308197, 5.7079024289788265, 3.133084625005722, 1.689554207271839, 0.9227425791323185, 3.0247902497649193, 1.9136028364300728, 1.748528123077378, 0.6322109140455723, 0.5436959069189969, 0.8640277199447155, 0.28191907331347466, 0.19230952002835394, 0.1616377945475456]}
# average = np.mean(data)
# print(average)

# import numpy as np

# # Initial emotion data
# emotion_data = {
#     'happy': [96.84540070946208, 0.0005374122793000424, 0.00, 0.0003083065166720189, 0.00022041744109199264, 4.010426356985951e-05, 1.903873510193311e-05, 1.2573278240779473e-05, 6.716470011269848e-05, 2.9130338754683397e-05],
#     'angry': [0.015638785726144376, 0.023322597553487867, 67, 0.006739799573551863, 0.0021203053065222124, 0.004615141547296087, 0.002995248174826506, 0.039374863263219595, 0.009953287371899933, 0.0008840032788902338],
#     'neutral': [0, 98.27663898468018, 96.72518968582153, 0, 99.86643194356155, 99.81215598438311, 99.87237452699986, 99.59481358528137, 99.8687207698822, 99.99152422052333]
# }

# # Get the number of frames (assuming all emotions have the same number of frames)
# num_frames = len(next(iter(emotion_data.values())))

# # Initialize a dictionary to store modified values with zeros
# modified_data = {emotion: [0] * num_frames for emotion in emotion_data}

# # Iterate over each frame (index)
# for i in range(num_frames):
#     # Find the emotion with the highest predicted value at index i
#     highest_value = 0
#     highest_emotion = None
    
#     for emotion, values in emotion_data.items():
#         if values[i] > highest_value:
#             highest_value = values[i]
#             highest_emotion = emotion
    
#     # Set the highest value in the corresponding emotion, other emotions will have zero
#     modified_data[highest_emotion][i] = highest_value

# # Calculate the average for each emotion using the modified data
# averages = {emotion: round(np.mean(values)/10,2) for emotion, values in modified_data.items()}
# # print(averages)

# emotions = {'happy': 4, 'neutral': 4, 'surprise': 4, 'angry': 4, 'fear': 4, 'disgust':4, 'sad': 4}

# weights = {'happy': 1.0, 'neutral': 0.5, 'surprise': 0.4, 'angry': -0.7, 'fear': -0.9, 'disgust': -1.0, 'sad': -0.8}

# # Calculate weighted sum
# weighted_sum = sum(emotions[emotion] * weights[emotion] for emotion in emotions)

# # Max possible weighted sum for normalization
# max_weighted_sum = (10 * 1.0 + 10 * 0.5 + 10 * 0.4) + (10 * -0.8 + 10 * -0.7 + 10 * -0.9 + 10 * -1.0)

# # Scale the confidence to a range of 0 to 10
# confidence_score = (weighted_sum / max_weighted_sum) * 10

# print("Confidence Score:", confidence_score)


# Given emotional values
emotions = {'happy': 10, 'neutral': 10, 'surprise': 10, 'angry': 0, 'fear': 0, 'disgust': 0.0, 'sad': 0}

# # Given emotion scores
# happy = 3
# neutral = 10
# surprise = 9
# angry = 1.7
# fear = 4.7
# disgust =6
# sad = 0.6

# # Calculate positive and negative contributions
# positive_contribution = happy + surprise
# negative_contribution = neutral + angry + fear + disgust + sad

# # Total emotions count
# total_emotions = 7

# # Net score
# net_score = (positive_contribution - negative_contribution) / total_emotions

# # Normalize the net score (scaling between 0 to 10)
# normalized_score = ((net_score + 1) / 2) * 10

# # Ensure the score is within 0 to 10 range
# confidence_score = max(0, min(normalized_score, 10))

# print(f"Facial Confidence Score: {confidence_score:.2f}")

# def convert_confidence(score):
#     # Normalize the score to a 0-1 range
#     normalized_score = (score - 1) / 9
#     print('normalized_score:',normalized_score)
#     # Scale to the 5-1 range
#     converted_score = 5 - (normalized_score * 4)
    
#     return round(converted_score, 1)

# Example usage
# print(convert_confidence(.8)) 
# print(convert_confidence(5))  # This will return a value close to 3


def convert_confidence(score):
    # Normalize the score to a 0-1 range
    normalized_score = (score - 1) / 9
    print('normalized_score:', normalized_score)

    # Scale to the 5-1 range
    converted_score = 5 - (normalized_score * 4)

    # Ensure the converted score does not exceed 5
    if converted_score > 5:
        converted_score = 5

    return round(converted_score, 1)

# Example usage
print(convert_confidence(10))  # Output should be 5.0 if beyond 5
