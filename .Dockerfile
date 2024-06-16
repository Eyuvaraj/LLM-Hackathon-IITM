# Use an official Python runtime as a parent image
FROM python:3.10-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisord.conf

# Expose ports for Chainlit and FastAPI
EXPOSE 8000
EXPOSE 5000

# Run supervisord to manage both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
