#!/bin/bash

WORK_DIR="/home/ubuntu/calc-visualizer/server"
DOCKER_COMPOSE_FILE="$WORK_DIR/docker-compose.yml"

# Pull the latest Docker image and restart the container
docker compose -f $DOCKER_COMPOSE_FILE down calc-visualizer
docker compose -f $DOCKER_COMPOSE_FILE pull calc-visualizer
docker compose -f $DOCKER_COMPOSE_FILE up -d calc-visualizer

# Clean up unused Docker images
docker image prune -f
