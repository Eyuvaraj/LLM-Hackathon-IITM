# IITM_BOT Project

This project consists of an interactive chatbot (`IITM Infobot`) and a FastAPI backend. The chatbot helps students with questions about the IITM BS degree program by providing information on courses, the application process, and general advice.

## Project Structure

- `frontend/`: Contains the Chainlit-based chatbot frontend.
- `backend/`: Contains the FastAPI backend and related components.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Eyuvaraj/LLM-Hackathon-IITM.git
    cd LLM-Hackathon-IITM
    ```

2. **Environment Variables**:
    - Copy and Rename `.env-sample` to `.env` in  `backend/` directory and add your API keys and settings:
      ```env
      HF_TOKEN=your_hf_token_here
      GROQ_API_KEY=your_groq_api_key_here
      NOMIC_API_KEY=your_nomic_api_key_here
      base_url=local_llm_url
      api_key=local_llm_api_key
      dev=True
      ```

## Running the Project

### Backend

1. **Navigate to the Backend Directory**:
    ```bash
    cd backend
    ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Backend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the FastAPI Backend**:
    ```bash
    uvicorn api:app --reload --port 5000
    ```

### Frontend

1. **Navigate to the Frontend Directory**:
    ```bash
    cd frontend
    ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Frontend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Chainlit Chatbot**:
    ```bash
    chainlit run app.py -w
    ```

## Docker Instructions

You can also use Docker to run the backend and frontend components.

### Backend

1. **Navigate to the Backend Directory**:
    ```bash
    cd backend
    ```

2. **Build Docker Image**:
    ```bash
    docker build -t IITM-bot-backend .
    ```

3. **Run Docker Container**:
    ```bash
    docker run -p 5000:5000 IITM-bot-backend
    ```

### Frontend

1. **Navigate to the Frontend Directory**:
    ```bash
    cd frontend
    ```

2. **Build Docker Image**:
    ```bash
    docker build -t IITM-bot-frontend .
    ```

3. **Run Docker Container**:
    ```bash
    docker run -p 8000:8000 IITM-bot-frontend
    ```

## Usage

Once the backend and chatbot are running, you can interact with the IITM_BOT by navigating to the Chainlit interface in your web browser at [http://localhost:8000/](http://localhost:8000/). The bot will assist you with queries related to the IITM BS degree program.

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

## Embedding Files

The project uses the following embedding files:
- `backend/embeddings.py`: Contains the code for generating embeddings and upserting embeddings into chromaDB.
- `backend/test_embeddings.py`: Contains the code for testing the embeddings through the terminal.

## My Certificate

![21F2000664_hackathon](https://github.com/user-attachments/assets/eb90668f-8030-473c-9037-606ed6e1e0da)


## Leaderboard

![Hackathon](https://github.com/user-attachments/assets/ef61b762-7b0b-47e2-8cc7-e278c8fac3c0)


