#!/bin/bash
# Utility script for testing Docker containers

test_docker_container() {
    local IMAGE_NAME=$1
    local TAG=$2
    local PORT=${3:-8042}
    local CONTAINER_NAME="clt_nlp_api_test_${TAG//[.:\/]/_}"
    
    echo "Testing Docker image: $IMAGE_NAME:$TAG"
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
            return 1
        fi
        echo "Waiting for API to start (attempt $RETRY_COUNT/$MAX_RETRIES)..."
        sleep 2
    done
    
    # Check API version if expected version is provided
    if [ -n "${4:-}" ]; then
        echo "Verifying API version matches $4..."
        API_VERSION=$(curl -s "http://localhost:$PORT/_health" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        if [ "$API_VERSION" != "$4" ]; then
            echo "ERROR: API version mismatch. Expected: $4, Got: $API_VERSION"
            docker container stop "$CONTAINER_NAME"
            docker container rm "$CONTAINER_NAME"
            return 1
        fi
        echo "API version verified: $API_VERSION"
    fi
    
    echo "API is ready. Running tests..."
    CLT_NLP_API_EXTERNAL_URL="http://localhost:$PORT" python -m pytest test_api.py -v
    TEST_RESULT=$?
    
    # Cleanup
    echo "Tests completed. Stopping and removing container..."
    docker container stop "$CONTAINER_NAME"
    docker container rm "$CONTAINER_NAME"
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo "Test run completed successfully!"
        return 0
    else
        echo "Tests failed!"
        return 1
    fi
}
