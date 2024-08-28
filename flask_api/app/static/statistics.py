import numpy as np

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

def emotionalsavg(emotion_confidences):

    # Get the number of frames (assuming all emotions have the same number of frames)
    num_frames = len(next(iter(emotion_confidences.values())))
    # Initialize a dictionary to store modified values with zeros
    modified_data = {emotion: [0] * num_frames for emotion in emotion_confidences}
    # Iterate over each frame (index)
    for i in range(num_frames):
        # Find the emotion with the highest predicted value at index i
        highest_value = 0
        highest_emotion = None
        for emotion, values in emotion_confidences.items():
            if values[i] > highest_value:
                highest_value = values[i]
                highest_emotion = emotion
        # Set the highest value in the corresponding emotion, other emotions will have zero
        modified_data[highest_emotion][i] = highest_value
    # Calculate the average for each emotion using the modified data
    emotion_avg_confidences = {emotion: round(np.mean(values)/10, 2) for emotion, values in modified_data.items()}
   
    return emotion_avg_confidences
