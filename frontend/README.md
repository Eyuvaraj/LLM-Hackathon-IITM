# IITM_BOT Frontend

This directory contains the Chainlit-based chatbot frontend for the IITM_BOT project.

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


## Running the Frontend

1. **Start the Chainlit Chatbot**:
    ```bash
    chainlit run app.py -w
    ```

## Docker Instructions

1. **Build Docker Image**:
    ```bash
    docker build -t IITM-bot-frontend .
    ```

2. **Run Docker Container**:
    ```bash
    docker run -p 8000:8000 IITM-bot-frontend
    ```

## Usage

Once the Chainlit chatbot is running, you can interact with the IITM_BOT by navigating to the Chainlit interface in your web browser at [http://localhost:8000/](http://localhost:8000/).