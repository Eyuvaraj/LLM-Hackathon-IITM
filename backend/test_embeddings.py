from langchain_chroma import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb
from utils import nomic_api_key
import os

embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=768, nomic_api_key=nomic_api_key)

# Load the document chunks into Chroma and save to disk
persistent_client = chromadb.PersistentClient(path="./chroma_db")
collection = persistent_client.get_or_create_collection("IITM-BS-Data")

langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="IITM-BS-Data",
    embedding_function=embeddings,
)

def get_embeddings(text):
    results = langchain_chroma.similarity_search_with_score(text, k=2)
    return results


Test = True

print("embeddings info:")
print("model: nomic-embed-text-v1.5")
print("dimensionality: 768")
print("chuck_size: 256")
print("chunk_overlap: 40")
print("Text splitter: RecursiveCharacterTextSplitter")
print("----------------------------------------------------\n")

print("Chroma info:")
print(f"path: ./chroma_db")
print(f"collection: IITM-BS-Data")
print("Score filter threshold: 0.5")
print("----------------------------------------------------\n\n")


print("Enter 'exit' to quit the program")
while Test:
    query = input("Enter your query: ")
    if query == "exit":
        Test = False
    else:
        items = get_embeddings(query)
        count = 0
        for item in items:
            count += 1
            content = item[0].page_content
            score = item[1]
            print(f"Document-{count} with score: {score}!")
            print(f"Content: {content}")
            if score > 0.5:
                print("\nNot Taken into consideration for answering user query!!")
            print("----------------------------------------------------\n")