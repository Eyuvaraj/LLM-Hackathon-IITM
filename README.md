# IITM_BOT Project

This project consists of an interactive chatbot (`IITM_BOT`) and a FastAPI backend. The chatbot helps students with questions about the IITM BS degree program by providing information on courses, the application process, and general advice.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://oauth2: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@github.com/Eyuvaraj/LLM-Hackathon-IITM.git
    cd LLM-Hackathon-IITM.git
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables**:
    - Rename`.env-sample` to `.env` and add your API keys and settings:
      ```env
      HF_TOKEN=your_hf_token_here
      GROQ_API_KEY=your_groq_api_key_here
      NOMIC_API_KEY=your_nomic_api_key_here
      dev=True
      ```

## Running the Project

1. **Start the FastAPI Backend**:
    ```bash
    uvicorn api:app --reload --port 5000
    ```

2. **Start the Chainlit Chatbot**:
    ```bash
    chainlit run app.py -w
    ```

## Note on Docker

Currently, I was unable to build a working Docker image for this project. Please follow the setup instructions above to run the project locally.

## Embedding Files

The project uses the following embedding files:
- `embeddings.py`: Contains the code for generating embeddings and upserting embeddings into chromaDB.
- `test_embeddings.py`: Contains the code for testing the embeddings through terminal.

## Usage

Once the backend and chatbot are running, you can interact with the IITM_BOT by navigating to the Chainlit interface in your web browser at [http://localhost:8000/](http://localhost:8000/). The bot will assist you with queries related to the IITM BS degree program.

## Note on API Integration

Due to limitations in handling context length in the provided api, I've opted to integrate with GROQ lamma70b instead. But meta-llama/Meta-Llama-3-8B-Instruct can be used by setting dev variable in .env to False

if Dev:

    Model: llama3-70b-8192
    RAG score filter: 0.7
    top_K: 10

else:

    Model: Meta-Llama-3-8B-Instruct
    RAG score filter: 0.5
    top_K: 2


![App Screenshot](./public/avatars/screentshot.png)