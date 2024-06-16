# import chainlit as cl
# from io import BytesIO
# import requests
# import os


# @cl.on_chat_start
# async def main():
#     await cl.Message(content="Hi, How can I help you? 🤗").send()


# @cl.on_message
# async def main(message: cl.Message):
#     # Your custom logic goes here...

#     # Send a response back to the user
#     await cl.Message(
#         content=f"Received: {message.content}",
#     ).send()


# # @cl.on_audio_chunk
# # async def on_audio_chunk(chunk: cl.AudioChunk):
# #     if chunk.isStart:
# #         buffer = BytesIO()
# #         buffer.name = f"input_audio.{chunk.mimeType.split('/')}"
# #         cl.user_session.set("audio_buffer", buffer)
# #         cl.user_session.set("audio_mime_type", chunk.mimeType)

# #     cl.user_session.get("audio_buffer").write(chunk.data)

# # @cl.on_audio_end
# # async def on_audio_end(elements: list[cl.ElementBased]):
# #     audio_buffer: BytesIO = cl.user_session.get("audio_buffer")
# #     audio_buffer.seek(0)
# #     audio_file = audio_buffer.read()
# #     audio_mime_type: str = cl.user_session.get("audio_mime_type")



# import chainlit as cl
# import requests

# backend_url = "http://localhost:8000/chat"  # FastAPI backend URL

# @cl.on_message
# def main(message: str):
#     response = requests.post(backend_url, json={"question": message})
#     response_data = response.json()
#     cl.Message(content=response_data["answer"]).send()


import chainlit as cl
import requests

backend_url = "http://localhost:5000/chat"  # FastAPI backend URL

@cl.on_message
def main(message: str):
    response = requests.post(backend_url, json={"question": message})
    response_data = response.json()
    if "answer" in response_data:
        cl.Message(content=response_data["answer"]).send()
    else:
        cl.Message(content="Error: " + response_data.get("error", "Unknown error")).send()
