import chainlit as cl
from io import BytesIO
import requests
from pydantic import BaseModel
from typing import List
import os

url = os.environ.get('CHAT_ENDPOINT_URL', 'http://127.0.0.1:5000/chat')
print('url:', url)

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

def message_dict(role, content):
    return {
        "role": role,
        "content": content
    }


@cl.on_chat_start
async def main():
    cl.user_session.set("CONVERSATIONS", [])
    await cl.Message("Hi, There! 🧑‍🎓 I'm **IITM Infobot**, your go-to source for information on the **[IITM BS degree program](https://study.iitm.ac.in/ds/)**.").send()


@cl.on_message
async def main(message: cl.message.Message):
    try:
        user_message = message.content  # Access the content attribute of the message
        CONVERSATIONS = cl.user_session.get("CONVERSATIONS")
        CONVERSATIONS.append(message_dict("user", user_message))

        # Prepare the data payload to send to the backend
        data = {
            "messages": CONVERSATIONS
        }

        # Send the payload to the backend
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if "assistant" in response_data:
            await cl.Message(content=response_data["assistant"]).send()
            CONVERSATIONS.append(message_dict("assistant", response_data["assistant"]))
        else:
            await cl.Message(content="Error: " + response_data.get("error", "Unknown error")).send()
    except Exception as e:
        await cl.Message(content="Error: " + str(e)).send()