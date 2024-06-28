from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_nomic.embeddings import NomicEmbeddings
import chromadb
import html2text
from utils import nomic_api_key
import os
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

embedding_model=None

if os.path.exists('nomic-embed-text-v1.5'):
    embedding_model = SentenceTransformer("nomic-embed-text-v1.5", trust_remote_code=True)
else:
    embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
    try:
        embedding_model.save('nomic-embed-text-v1.5')
    except:
        pass


#HTML and PDF documents dir
PDF_DIR = "data/Pdf_documents"
HTML_DIR = "data"


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=128,
    length_function=len,
    is_separator_regex=True,
    separators=[
        "\n\n\n",
        "\n\n",
        "\n",
        " ",
        ".",
        "\t",
        ",",
        "\u200B",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
)


def Text_Splitter(data):
    chunks = [re.sub("\n", " ", chunk.page_content) for chunk in text_splitter.create_documents(data)]
    chunks = [chunk for chunk in chunks if len(chunk) >= 50]
    return chunks


def ChromaDB_EMB(docs, type, batch_size=512):
    persistent_client = chromadb.PersistentClient(path="./chroma_db")
    collection = persistent_client.get_or_create_collection("IITM-BS-Data")
    
    def process_and_add_batch(batch_docs, batch_start_idx):
        doc_embeddings = embedding_model.encode(batch_docs, convert_to_numpy=True, show_progress_bar=True, output_value='sentence_embedding', precision='float32', normalize_embeddings=True).tolist()
        try:
            collection.add(
                documents=batch_docs,
                embeddings=doc_embeddings,
                ids=[f"vec-{type}_{i}" for i in range(batch_start_idx, batch_start_idx + len(batch_docs))]
            )
        except chromadb.errors.DuplicateIDError:
            pass

    # Process and add documents in batches
    num_docs = len(docs)
    for start_idx in range(0, num_docs, batch_size):
        end_idx = min(start_idx + batch_size, num_docs)
        batch_docs = docs[start_idx:end_idx]
        process_and_add_batch(batch_docs, start_idx)
    
    print(f"Added {num_docs} documents to ChromaDB")
 

def PDF_Parser(file_path):
    loader = PyMuPDFLoader(file_path)
    data = loader.load()
    return [item.page_content for item in data]


def chunk_pdf(PDF_DIR):
	import os
	pdf_files = os.listdir(PDF_DIR)
	data = []
	for item in pdf_files:
		file_path = os.path.join(PDF_DIR, item)
		data.extend(PDF_Parser(file_path))

	chunks = Text_Splitter(data)
	print(f"{len(chunks)} chunks created from pdf files!\n")
	return chunks


def extract_text_from_html(file_path):
    """Extract main body text from an HTML file, excluding certain elements."""
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    body = soup.find('div', {'id': 'mainContent'})

    if body:
        elements_to_exclude = ['header', 'nav', 'footer', 'sidebar', 'button']

        for tag_name in elements_to_exclude:
            elements = body.find_all(tag_name)
            for element in elements:
                element.decompose()
            elements = body.find_all('div', {'id': 'mobNotification'})
            for element in elements:
                element.decompose()

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text = text_maker.handle(str(body))
        return text.strip()
    else:
        return ""


def crawl_directory(directory):
    """Crawl the given directory and extract text from all HTML files."""
    html_texts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                text = extract_text_from_html(file_path)
                html_texts.append(text)
    return html_texts


def chunk_HTML(directory):
    html_texts = crawl_directory(directory)
    html_chunks = Text_Splitter(html_texts)
    print(f"{len(html_chunks)} chunks created from html files!\n")
    return html_chunks


# Chunk and Embed PDF documents to ChromaDB
pdf_docs = chunk_pdf(PDF_DIR)
ChromaDB_EMB(pdf_docs, "pdf")


# Chunk and Embed HTML documents to ChromaDB
html_docs = chunk_HTML(HTML_DIR)
ChromaDB_EMB(html_docs, "html")