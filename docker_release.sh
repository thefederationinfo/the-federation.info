#!/usr/bin/env bash

set -e

docker login
docker build -f docker/app/Dockerfile -t jaywink/the-federation.info .
docker push jaywink/the-federation.info:latest
