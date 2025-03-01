#!/bin/bash
set -e

# Source the utility functions
source ./docker_test_utils.sh

# Configuration
IMAGE_NAME="vocabai/clt-nlp-api"
TAG="test-$(date +%Y%m%d-%H%M%S)"
PORT="8042"

echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t "$IMAGE_NAME:$TAG" -f Dockerfile .

# Run tests using the utility function
test_docker_container "$IMAGE_NAME" "$TAG" "$PORT"
exit $?
