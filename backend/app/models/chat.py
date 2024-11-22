from pydantic import BaseModel
from typing import Dict

class SensorData(BaseModel):
    temperature: float
    humidity: float
    toxicGases: float

class ChatMessage(BaseModel):
    message: str
    sensorData: SensorData

class ChatResponse(BaseModel):
    message: str