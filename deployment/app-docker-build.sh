#! /usr/bin/env bash

# This script builds a Docker image for the app.
# Usage: ./app-docker-build.sh

# Build the Docker image for the app
cd $(dirname "$0")/.. || exit 1
docker build -t forecast-app .
