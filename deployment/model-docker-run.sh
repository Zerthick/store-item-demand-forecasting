#! /usr/bin/env bash

# This script runs a Docker image for an MLflow model.
# The script assumes that the Docker image has already been built using the model-docker-build.sh script.
# Usage: ./model-docker-run.sh

docker run -d \
    -p 8080:8080 \
    lgbm-model 
   