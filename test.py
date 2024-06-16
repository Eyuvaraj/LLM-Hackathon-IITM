from langchain_chroma import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb

embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=768)

# Load the document chunks into Chroma and save to disk
persistent_client = chromadb.PersistentClient(path="./chroma_db")
collection = persistent_client.get_or_create_collection("IITM-BS-Data")

langchain_chroma = Chroma(
    client=persistent_client,
    collection_name="IITM-BS-Data",
    embedding_function=embeddings,
)

k = langchain_chroma.similarity_search("What did the president say about Ketanji Brown Jackson?")
print(k)