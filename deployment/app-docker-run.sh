#! /usr/bin/env bash

# This script runs a Docker image for the app.
# The script assumes that the Docker image has already been built using the app-docker-build.sh script.
# Usage: ./app-docker-run.sh

docker run -d \
    -p 80:80 \
    forecast-app