FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make the worker script executable
RUN chmod +x /app/docker/rq_worker.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app:create_app()

# Expose the Flask port
EXPOSE 5000

# Use a multi-stage CMD for different service types
# Default is to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:create_app()"]
