#!/usr/bin/env bash

set -e

if [[ -z "${MAXMIND_LICENSE_KEY}" ]]; then
  echo Define MAXMIND_LICENSE_KEY!
  exit 1
fi

docker login

docker build -f docker/app/Dockerfile -t a6543/the-federation_backend --build-arg "MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}" .
docker push a6543/the-federation_backend:latest

docker build -f docker/nginx/Dockerfile -t a6543/the-federation_frontend .
docker push a6543/the-federation_frontend:latest
