from fastapi import FastAPI, HTTPException
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb
import os
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List, Dict
from groq import Groq
from utils import dev, nomic_api_key, groq_api_key, api_key, base_url, llm_model

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    assistant: str


# API client initialization
if not dev:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    SCORE, top_K = 0.9, 5
else:
    client = Groq(
        api_key=groq_api_key
    )
    SCORE, top_K = 0.9, 6


embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=768, nomic_api_key=nomic_api_key)

# Load the document chunks into Chroma and save to disk
persistent_client = chromadb.PersistentClient(path="./chroma_db")
collection = persistent_client.get_or_create_collection("IITM-BS-Data")

langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="IITM-BS-Data",
    embedding_function=embeddings,
)


def message_dict(role, content):
    return {
        "role": role,
        "content": content
    }


def rag_vectors(text):
    results = langchain_chroma.similarity_search_with_score(text, k=top_K)
    docs = []
    for item in results:
        content = item[0].page_content
        score = item[1]
        if score < SCORE:
            docs.append(content)
    # print(f"Found {len(docs)} documents")
    return docs if docs else None


# def rag_vectors(text):
#     text_embedding = embeddings.embed([text], task_type='search_document')
#     results = langchain_chroma.max_marginal_relevance_search_by_vector(text_embedding, k=top_K, fetch_k=8, lambda_mult=0.9)
#     docs = []
#     for item in results:
#         content = item.page_content
#         docs.append(content)
#     print(f"Found {len(docs)} documents")
#     return docs if docs else None


SYSTEM_PROMPT = """You are an IITM Infobot here to answer any questions students have about the IITM BS degree program. You are knowledgeable about the program, its courses, the application process, and can provide general advice and guidance to interested students. You are friendly, approachable, and eager to help students succeed.

Personalize interactions by asking for the user's name.
Engage in casual, conversational dialogue with expressions like 'Hmm,' 'Ah,' and very rarely emojis!
Maintain a simplified, clear, concise and natural tone.
Avoid excessive detail or technical jargon for clarity and engagement.
Do not assume or provide imaginary information. Ask for clarification if the query is unclear, or kindly say you don't know.
Strictly restrict yourself to answering questions related only to the IITM BS degree program.
Provide responses in Markdown format."""


def rag_prompt(query):
    vectors = rag_vectors(query)
    if vectors and len(vectors) >= 1:
        # print(f"Vectors: \n\n{vectors}\n\n")
        prompt = (
            f"This is User's Query: {query}\n\n"
            "Use the below information to answer the user's query if and only if you find it related or helpful, Take you time to go through it.\n"
            "Note: The information provided may not be complete or may not be relevant to user's query, If not relavant, just ignore it and engage in casual conversation!\n"
        )

        count = 0
        for item in vectors:
            count+=1
            prompt += f"\nInfo {count}: {item}\n"

        prompt += f"\nRemember: Do not assume or provide imaginary information, especially when talking about numbers, time, money..., as your sole aim is to provide accurate and reliable information to the students and if possible provide citation/link/reference if you have proper information in markdown hyperlink format"
        return prompt
    else:
        return query


def get_response(conv: List[Message]) -> str:
    try:
        user_query = conv[-1].content
        augmented_prompt = rag_prompt(user_query)
        
        messages = [
            message_dict("system", SYSTEM_PROMPT),
        ]
        messages.extend(conv[:-1])
        messages.append(message_dict("user", augmented_prompt))


        chat_completion = client.chat.completions.create(
            model=llm_model if not dev else "llama3-70b-8192",
            messages=messages,
            max_tokens=4000
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "🤗Hi There, welcome"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        user_messages = request.messages
        answer = get_response(user_messages)
        return {"assistant": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)