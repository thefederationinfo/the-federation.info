#!/usr/bin/env bash

set -e

if [[ -z "${MAXMIND_LICENSE_KEY}" ]]; then
  echo Define MAXMIND_LICENSE_KEY!
  exit 1
fi

docker login

docker build -f docker/app/Dockerfile -t jaywink/the-federation.info --build-arg "MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}" .
docker push jaywink/the-federation.info:latest

docker build -f docker/nginx/Dockerfile -t jaywink/the-federation.info-web .
docker push jaywink/the-federation.info-web:latest
