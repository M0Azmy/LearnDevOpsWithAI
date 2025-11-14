# Dockerfile for a simple flask app "hello-world"

# Use the official python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./app/requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container  
COPY /app/ .

# Expose the port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]


