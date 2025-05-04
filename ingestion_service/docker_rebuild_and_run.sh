#!/bin/bash
set -e

IMAGE_NAME="ingestion-service"
CONTAINER_NAME="ingestion-service-running"
PORT=5000

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Stopping any running container named $CONTAINER_NAME (if exists)..."
docker stop $CONTAINER_NAME 2>/dev/null || true

echo "Removing old container (if exists)..."
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "Starting new container..."
docker run --rm --name $CONTAINER_NAME -p $PORT:5000 --env-file .env $IMAGE_NAME
