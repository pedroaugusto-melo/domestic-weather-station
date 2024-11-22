from fastapi import APIRouter, HTTPException
from openai import OpenAI
from app.core.config import settings
from typing import List, Dict

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@router.get("/suggestions")
async def get_ai_suggestions(temperature: float, humidity: float, toxic_gases: float):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an environmental analysis expert. Analyze the current readings and provide 3-4 actionable suggestions 
                    for improving comfort and safety. Focus on health impacts and practical solutions. Keep suggestions concise and direct. Write in portuguese (pt-br).
                    Format the response as a JSON array of objects, each with 'title' and 'description' fields."""
                },
                {
                    "role": "user",
                    "content": f"""Current readings:
                    Temperature: {temperature}°C
                    Humidity: {humidity}%
                    Toxic Gas Levels: {toxic_gases} ppm
                    
                    Provide analysis and suggestions based on these values."""
                }
            ]
        )
        
        return {"suggestions": completion.choices[0].message.content.replace("```json", "").replace("```", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))