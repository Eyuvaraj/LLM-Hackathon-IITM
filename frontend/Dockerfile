FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application folder into the container
COPY . /app/

# Expose the port your app runs on (optional)
EXPOSE 5000

# Define the command to run the application
CMD ["chainlit", "run", "app.py"]
