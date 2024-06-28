FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY min-requirements-docker.txt .

RUN pip install --no-cache-dir -r min-requirements-docker.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]