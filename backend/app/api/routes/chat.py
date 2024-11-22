from fastapi import APIRouter, HTTPException
from openai import OpenAI
from app.core.config import settings
from app.models.chat import ChatMessage, ChatResponse

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@router.post("", response_model=ChatResponse)
async def chat(data: ChatMessage):
    try:
        # Create or retrieve the assistant
        assistant = client.beta.assistants.retrieve(settings.OPENAI_ASSISTANT_ID)

        # Create a thread
        thread = client.beta.threads.create()

        # Add the user's message with context
        message = f"""
        Current readings:
        Temperature: {data.sensorData.temperature}°C
        Humidity: {data.sensorData.humidity}%
        Toxic Gas Levels: {data.sensorData.toxicGases} ppm

        User question: {data.message}
        """

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break

        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_message = messages.data[0].content[0].text.value

        return ChatResponse(message=assistant_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 