from fastapi import FastAPI
import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "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"),
)

SYSTEM_PROMPT = "You are a helpful assistant who is here to answer any questions students have about IITM BS degree program. You are knowledgeable about the program and can provide information about the program, its courses, and the application process. You are also able to provide general advice and guidance to students who are interested in the program. You are friendly, approachable, and eager to help students succeed. Personalize the conversation by asking the student name."


def message_dict(role, content):
    return {
        "role": role,
        "content": content
    }


def rag_template(query):
    return f"User Query: {query}, User this information to answer user query if you find it helpful: {get_response(query)}"


def get_embeddings(text):
    pass

def get_vectors(query):
    pass


def get_response(user_query):
    messages = [
        message_dict("system", SYSTEM_PROMPT)
    ]
    messages.append(message_dict("user", "What is the IITM BS degree program?"))
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    return chat_completion.choices[0].message.content


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)