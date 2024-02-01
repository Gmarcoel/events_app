#!/bin/bash

# Go to script directory
cd "$(dirname "$0")"

# Go to docker directory
cd docker

# Check Docker version
docker_version=$(docker --version)
echo "Docker version: $docker_version"

# Check Docker Compose version
if command -v docker-compose &> /dev/null
then
    docker_compose_version=$(docker-compose version)
    echo "Docker Compose version: $docker_compose_version"
    echo "Running Docker Compose with 'docker-compose up --build'"
    docker-compose up --build
elif command -v docker &> /dev/null
then
    docker_compose_version=$(docker compose version)
    echo "Docker Compose version: $docker_compose_version"
    echo "Running Docker Compose with 'docker compose up --build'"
    docker compose up --build
else
    echo "Neither docker-compose nor docker is installed."
    echo "Unsupported Docker Compose version. Please install Docker Compose version 1.x or 2.x."
fi
