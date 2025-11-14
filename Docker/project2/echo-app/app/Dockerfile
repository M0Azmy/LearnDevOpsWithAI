# Simple Python web server image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Command to run the application (Default)
CMD ["python", "app.py"]
