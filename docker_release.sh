#!/usr/bin/env bash

set -e

if [[ -z "${MAXMIND_LICENSE_KEY}" ]]; then
  echo Define MAXMIND_LICENSE_KEY!
  exit 1
fi

SHA=$(git rev-parse --short=8 HEAD)
TAG="v1-${SHA}"

docker build -f docker/app/Dockerfile -t codeberg.org/thefederationinfo/backend:latest -t "codeberg.org/thefederationinfo/backend:${TAG}" --build-arg "MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}" .
docker push codeberg.org/thefederationinfo/backend:latest
docker push "codeberg.org/thefederationinfo/backend:${TAG}"

docker build -f docker/nginx/Dockerfile -t codeberg.org/thefederationinfo/frontend:latest -t "codeberg.org/thefederationinfo/frontend:${TAG}" .
docker push codeberg.org/thefederationinfo/frontend:latest
docker push "codeberg.org/thefederationinfo/frontend:${TAG}"
