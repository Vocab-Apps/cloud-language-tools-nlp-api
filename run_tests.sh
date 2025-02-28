#!/bin/bash
set -e

# Configuration
IMAGE_NAME="lucwastiaux/spacy-api"
TAG="test-$(date +%Y%m%d-%H%M%S)"
CONTAINER_NAME="spacy_api_test"
PORT="8042"

echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t "$IMAGE_NAME:$TAG" -f Dockerfile .

echo "Starting container: $CONTAINER_NAME"
docker run --name "$CONTAINER_NAME" -d -p "0.0.0.0:$PORT:$PORT/tcp" "$IMAGE_NAME:$TAG"

# Wait for the API to be ready
echo "Waiting for API to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
while ! curl -s "http://localhost:$PORT/_health" > /dev/null; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "API failed to start after $MAX_RETRIES attempts"
        docker container stop "$CONTAINER_NAME"
        docker container rm "$CONTAINER_NAME"
        exit 1
    fi
    echo "Waiting for API to start (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    sleep 2
done

echo "API is ready. Running tests..."
SPACY_API_EXTERNAL_URL="http://localhost:$PORT" python -m pytest test_api.py -v

# Cleanup
echo "Tests completed. Stopping and removing container..."
docker container stop "$CONTAINER_NAME"
docker container rm "$CONTAINER_NAME"

echo "Test run completed successfully!"
