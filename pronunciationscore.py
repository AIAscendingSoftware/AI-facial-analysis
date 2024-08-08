# import torch
# import torchaudio

# # Load the pre-trained Wav2Vec2 model
# model = torch.hub.load('facebookresearch/fairseq', 'wav2vec2_large_lv60k')
# model.eval()

# def get_pronunciation_score(audio_path):
#   """
#   Calculates a pronunciation score for an audio file.

#   Args:
#     audio_path: Path to the audio file.

#   Returns:
#     Pronunciation score.
#   """

#   # Load audio file
#   waveform, sample_rate = torchaudio.load(audio_path)


#   # Convert to tensor
#   waveform = waveform.to(next(model.parameters()).device)

#   # Extract features from the model
#   with torch.no_grad():
#     features = model.feature_extractor(waveform)

#   # Apply your pronunciation scoring logic here
#   # This is a placeholder, replace with your actual scoring method
#   pronunciation_score = torch.mean(features).item()

#   return pronunciation_score

# # Example usage
# audio_file = "D:\AI Projects\AI facial analysis\extracted_audio.wav"
# score = get_pronunciation_score(audio_file)
# print("Pronunciation score:", score)

# import torch
# import torchaudio
# from fairseq.models.wav2vec import Wav2Vec2Model

# # Load the model checkpoint directly
# model_path = 'D:/AI Projects/AI facial analysis/fairseq/wav2vec2_large_lv60k.pt'  # Replace with the correct path to your model checkpoint

# # Load the Wav2Vec2 model
# model, cfg, task = Wav2Vec2Model.load_model_ensemble_and_task([model_path])

# # Use the first model in the ensemble (if there's more than one)
# model = model[0]
# device = torch.device('cpu')
# model = model.to(device)
# model.eval()

# # Example function to calculate pronunciation score
# def get_pronunciation_score(audio_path):
#     """
#     Calculates a pronunciation score for an audio file.

#     Args:
#         audio_path: Path to the audio file.

#     Returns:
#         Pronunciation score.
#     """
#     # Load audio file
#     waveform, sample_rate = torchaudio.load(audio_path)
    
#     # Convert to tensor and ensure correct device
#     waveform = waveform.to(device)
    
#     # Extract features from the model
#     with torch.no_grad():
#         features = model.feature_extractor(waveform)
    
#     # Apply your pronunciation scoring logic here
#     pronunciation_score = torch.mean(features).item()

#     return pronunciation_score

# # Example usage
# audio_file = "D:/AI Projects/AI facial analysis/extracted_audio.wav"
# score = get_pronunciation_score(audio_file)
# print("Pronunciation score:", score)


# import os
# import wave
# import numpy as np
# from pocketsphinx import Pocketsphinx, Decoder
# from collections import defaultdict

# def get_pronunciation_score(audio_file):
#     # Load the audio file
#     wav = wave.open(audio_file, 'r')
#     audio_data = wav.readframes(wav.getnframes())
#     wav.close()

#     # Configure the CMU Sphinx decoder
#     config = Decoder.default_config()
#     config.set_string('-hmm', 'path/to/acoustic/model')
#     config.set_string('-lm', 'path/to/language/model')
#     config.set_string('-dict', 'path/to/pronunciation/dictionary')
#     decoder = Decoder(config)

#     # Decode the audio
#     decoder.start_utt()
#     decoder.process_raw(audio_data, False, True)
#     decoder.end_utt()

#     # Get the pronunciation scores for each recognized word
#     total_score = 0
#     num_words = 0
#     for seg, score, _, _ in decoder.seg():
#         total_score += score
#         num_words += 1

#     # Calculate the final pronunciation score
#     if num_words > 0:
#         final_score = total_score / num_words
#     else:
#         final_score = 0

#     return final_score

# # Example usage
# audio_file = "D:\AI Projects\AI facial analysis\AI-facial-analysis\mixkit-cartoon-girl-saying-no-no-no-2257.wav"
# score = get_pronunciation_score(audio_file)
# print(f"Pronunciation score: {score:.2f}")
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\path\\to\\your\\service-account-file.json"



from google.cloud import speech

def get_pronunciation_score(audio_file):
    # Initialize the Google Cloud Speech-to-Text client
    client = speech.SpeechClient()

    # Load the audio file
    with open(audio_file, 'rb') as audio_content:
        audio = speech.RecognitionAudio(content=audio_content.read())

    # Configure the recognition request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Perform the speech recognition
    response = client.recognize(config=config, audio=audio)

    # Calculate the pronunciation score
    total_score = 0
    num_words = 0
    for result in response.results:
        for alternative in result.alternatives:
            total_score += alternative.confidence
            num_words += 1

    if num_words > 0:
        final_score = total_score / num_words
    else:
        final_score = 0

    return final_score

# Example usage
audio_file = "D:\AI Projects\AI facial analysis\AI-facial-analysis\mixkit-cartoon-girl-saying-no-no-no-2257.wav"
score = get_pronunciation_score(audio_file)
print(f"Pronunciation score: {score:.2f}")