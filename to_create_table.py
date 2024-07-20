from pydantic import BaseModel, Field
from typing import Optional

class ProCommunicationAiFaceDetailsModel(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    user_id: Optional[int] = Field(None, alias='userId')
    video_id: Optional[int] = Field(None, alias='videoId')
    overall_score: Optional[float] = Field(None, alias='overAllScroe')
    facial_score: Optional[float] = Field(None, alias='fcialScore')
    happy: Optional[float] = Field(None, alias='happy')
    neutral: Optional[float] = Field(None, alias='nautral')
    surprise: Optional[float] = Field(None, alias='surprise')
    angry: Optional[float] = Field(None, alias='angry')
    disgust: Optional[float] = Field(None, alias='disgust')
    fear: Optional[float] = Field(None, alias='fear')
    sad: Optional[float] = Field(None, alias='sad')
    face_confidence: Optional[float] = Field(None, alias='faceConfidence')
    communication_score: Optional[float] = Field(None, alias='communicationScore')
    grammar: Optional[float] = Field(None, alias='grammar')
    fluency: Optional[float] = Field(None, alias='fluency')
    pronunciation: Optional[float] = Field(None, alias='pronunciation')
    speech_score: Optional[float] = Field(None, alias='speechScore')
    tone: Optional[float] = Field(None, alias='tone')
    voice_confidence: Optional[float] = Field(None, alias='voiceConfidence')
    speech_rate: Optional[float] = Field(None, alias='speechRate')
    body_language_score: Optional[float] = Field(None, alias='bodyLanguageScore')
    looking_straight: Optional[float] = Field(None, alias='lookingStraight')
    smile_count: Optional[float] = Field(None, alias='smileCount')
    hand_usage: Optional[float] = Field(None, alias='handUsage')
    arms_crossed: Optional[float] = Field(None, alias='armsCrossed')
    wrists_closed: Optional[float] = Field(None, alias='wristsClosed')
    weight_on_one_leg: Optional[float] = Field(None, alias='weightOnOneLeg')
    leg_movement: Optional[float] = Field(None, alias='legMovement')
    weight_balanced_on_both_legs: Optional[float] = Field(None, alias='weightBalancedOnBothLegs')
    eye_contact: Optional[float] = Field(None, alias='eyeContact')
    voice_graph_base64: Optional[str] = Field(None, alias='voiceGraphBase64')

# Example usage
example_data = {
    'id': 1,
    'userId': 123,
    'videoId': 456,
    'overAllScroe': 90.5,
    'fcialScore': 88.7,
    'happy': 70.0,
    'nautral': 20.0,
    'surprise': 10.0,
    'angry': 0.0,
    'disgust': 0.0,
    'fear': 0.0,
    'sad': 0.0,
    'faceConfidence': 95.0,
    'communicationScore': 85.0,
    'grammar': 80.0,
    'fluency': 75.0,
    'pronunciation': 85.0,
    'speechScore': 78.0,
    'tone': 80.0,
    'voiceConfidence': 85.0,
    'speechRate': 90.0,
    'bodyLanguageScore': 80.0,
    'lookingStraight': 90.0,
    'smileCount': 5.0,
    'handUsage': 70.0,
    'armsCrossed': 0.0,
    'wristsClosed': 0.0,
    'weightOnOneLeg': 10.0,
    'legMovement': 20.0,
    'weightBalancedOnBothLegs': 70.0,
    'eyeContact': 80.0,
    'voiceGraphBase64': 'base64encodedstring'
}

model_instance = ProCommunicationAiFaceDetailsModel(**example_data)
print(model_instance)