#!/bin/bash
set -eoux pipefail

# exit if argument is not passed in
if [ -z "$1" ]; then
  echo "Please pass major, minor or patch"
  exit 1
fi

BUMP_TYPE=$1 # major, minor or patch
# check that the bump type is valid
if [ "$BUMP_TYPE" != "major" ] && [ "$BUMP_TYPE" != "minor" ] && [ "$BUMP_TYPE" != "patch" ]; then
  echo "Please pass major, minor or patch"
  exit 1
fi

NEW_VERSION=`bump2version --list ${BUMP_TYPE} | grep new_version | sed -r s,"^.*=",,`
# push to upstream
git push
git push --tags

VERSION_NUMBER=$NEW_VERSION

# docker build
export DOCKER_BUILDKIT=1
DOCKER_IMAGE=vocabai/clt-nlp-api
docker build -t ${DOCKER_IMAGE}:${VERSION_NUMBER} -f Dockerfile .

# Source the utility functions
source ./docker_test_utils.sh

# Test the container before pushing
echo "Testing container before pushing..."
PORT="8042"
if test_docker_container "$DOCKER_IMAGE" "$VERSION_NUMBER" "$PORT" "$VERSION_NUMBER"; then
  echo "Container tests passed. Pushing to registry..."
  docker push ${DOCKER_IMAGE}:${VERSION_NUMBER}
else
  echo "Container tests failed! Not pushing to registry."
  exit 1
fi
