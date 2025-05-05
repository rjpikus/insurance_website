# Batch Processing Service

A scalable, distributed batch processing service built with Flask, Redis Queue (RQ), and Ray for distributed computing.

## 🚀 Features

- **HTTP API** for job submission and status checking
- **Background processing** with Redis Queue
- **Distributed computing** with Ray framework
- **Workflow orchestration** with Prefect
- **Containerized** with Docker
- **Railway deployment** ready

## 📋 System Architecture

This service consists of the following components:

1. **Web API**: Flask-based HTTP API for job submission and monitoring
2. **Queue**: Redis-based job queue for asynchronous processing
3. **Workers**: Background workers that consume jobs from the queue
4. **Distributed Computing**: Ray framework for parallel processing
5. **Orchestration**: Prefect for complex workflow management

## 🔧 Setup & Installation

### Local Development

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis**
   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

4. **Start the API server**
   ```bash
   flask run
   ```

5. **Start a worker**
   ```bash
   python -m app.queue_worker
   ```

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t batch-service -f docker/Dockerfile .
   ```

2. **Run the API container**
   ```bash
   docker run -p 5000:5000 --env-file .env batch-service
   ```

3. **Run a worker container**
   ```bash
   docker run --env-file .env batch-service ./docker/rq_worker.sh
   ```

## 📤 API Endpoints

### `POST /enqueue`
Enqueue a new batch processing job.

Example payload for data processing:
```json
{
  "job_type": "data_processing",
  "data": {
    "item1": "value1",
    "item2": "value2"
  },
  "options": {
    "use_ray": true,
    "batch_size": 10
  }
}
```

Example payload for text processing:
```json
{
  "job_type": "text_processing",
  "data": "Text content to process...",
  "options": {
    "operations": ["count", "tokenize", "sentiment"],
    "use_ray": true
  }
}
```

### `GET /job/{job_id}`
Get the status and results of a specific job.

### `GET /jobs`
List all jobs in the queue.

### `GET /health`
Health check endpoint.

## 📦 Deployment on Railway

This service is configured for deployment on Railway. Railway.json handles the configuration.

1. Link your repository to Railway
2. Set up the required environment variables
3. Deploy!

## 🧪 Testing

Run the tests with pytest:
```bash
pytest
```

## 🔍 Environment Variables

- `FLASK_HOST` - Host to bind Flask server (default: 0.0.0.0)
- `FLASK_PORT` - Port for Flask server (default: 5000)
- `FLASK_DEBUG` - Enable debug mode (default: False)
- `REDIS_URL` - Redis connection URL (default: redis://localhost:6379/0)
- `RQ_QUEUE_NAME` - Name of the RQ queue (default: batch_processing)
- `RAY_ADDRESS` - Ray cluster address (default: None - local)
- `RAY_NUM_CPUS` - Number of CPUs for Ray (default: 2)
- `LOG_LEVEL` - Logging level (default: INFO)
- `TIMEOUT` - Job timeout in seconds (default: 3600)
