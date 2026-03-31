#!/usr/bin/env bash

set -e

if [[ -z "${MAXMIND_LICENSE_KEY}" ]]; then
  echo Define MAXMIND_LICENSE_KEY!
  exit 1
fi

docker build -f docker/app/Dockerfile -t codeberg.org/thefederationinfo/backend:latest --build-arg "MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}" .
docker push codeberg.org/thefederationinfo/backend:latest

docker build -f docker/nginx/Dockerfile -t codeberg.org/thefederationinfo/frontend:latest .
docker push codeberg.org/thefederationinfo/frontend:latest
