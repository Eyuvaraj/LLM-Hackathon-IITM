# IITM_BOT Backend

This directory contains the FastAPI backend for the IITM_BOT project.

## Setup

1. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables**:
    - Copy and Rename `.env-sample` to `.env` and add your API keys and settings:
      ```env
      HF_TOKEN=your_hf_token_here
      GROQ_API_KEY=your_groq_api_key_here
      NOMIC_API_KEY=your_nomic_api_key_here

      base_url=llm_endpoint_url
      api_key=llm_endpoint_api_key

      dev=True
      ```

## Running the Backend

1. **Start the FastAPI Backend**:
    ```bash
    uvicorn api:app --reload --port 5000
    ```

## Docker Instructions

1. **Build Docker Image**:
    ```bash
    docker build -t iitm-bot-backend .
    ```

2. **Run Docker Container**:
    ```bash
    docker run -p 5000:5000 iitm-bot-backend
    ```

## Embedding Files

The backend uses the following embedding files:
- `embeddings.py`: Contains the code for generating embeddings and upserting embeddings into chromaDB.
- `test_embeddings.py`: Contains the code for testing the embeddings through the terminal.

## Note on API Integration

Due to limitations in handling context length in the provided API, I've opted to integrate with GROQ lamma70b instead. But meta-llama/Meta-Llama-3-8B-Instruct can be used by setting the `dev` variable in `.env` to `False`.

if `dev`:

    Model: llama3-70b-8192
    RAG score filter: 0.7
    top_K: 10

else:

    Model: Meta-Llama-3-8B-Instruct
    RAG score filter: 0.5
    top_K: 2
