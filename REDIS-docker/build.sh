#!/bin/sh

set -x
if [ -z "$1" ]; then
  echo "using default tag: latest"
fi


TAG_VERSION=${1:-latest}
NAME="heu-green-testday/redis"
CONTAINER_REGISTRY="eu.gcr.io"

IMAGE_NAME="${CONTAINER_REGISTRY}/${NAME}:${TAG_VERSION}"


docker build --rm -t $NAME .
docker tag $NAME $IMAGE_NAME
# docker push $IMAGE_NAME

# if [ "$2" = "--push" ]; then
#   docker push $REGISTRY/$NAME
# else
#   echo "Skipping $NAME image push to docker repository"
# fi