import chainlit as cl
from io import BytesIO
import requests
from pydantic import BaseModel
from typing import List
from utils import dev, nomic_api_key, groq_api_key, hf_token

url = 'http://localhost:5000/chat'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

def message_dict(role, content):
    return {
        "role": role,
        "content": content
    }

CONVERSATION = []

@cl.on_chat_start
async def main():
    await cl.Message(content="Hi! 🧑‍🎓 I'm **IITM_BOT**, your go-to source for information on the **IITM BS degree program**.").send()


@cl.on_message
async def main(message: cl.message.Message):
    try:
        user_message = message.content  # Access the content attribute of the message
        CONVERSATION.append(message_dict("user", user_message))

        # Prepare the data payload to send to the backend
        data = {
            "messages": CONVERSATION
        }

        # Send the payload to the backend
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if "assistant" in response_data:
            await cl.Message(content=response_data["assistant"]).send()
            CONVERSATION.append(message_dict("assistant", response_data["assistant"]))
        else:
            await cl.Message(content="Error: " + response_data.get("error", "Unknown error")).send()
    except Exception as e:
        await cl.Message(content="Error: " + str(e)).send()
