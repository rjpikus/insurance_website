#!/bin/bash
set -e

# RQ Worker startup script for Docker container
echo "Starting RQ Worker service"

# Wait for Redis to be available
echo "Waiting for Redis..."
until python -c "import redis; redis.from_url('${REDIS_URL}').ping()" 2>/dev/null
do
  echo "Redis not available yet - sleeping"
  sleep 1
done

echo "Redis is available! Starting worker..."

# Start the RQ worker
cd /app
exec python -m app.queue_worker
