#!/bin/bash

set -e

# Create directories for persistent volumes
mkdir -p ./volumes/mongo-data
mkdir -p ./volumes/ollama-data

# Convert docker images to SIF files (if not already done)
echo "Pulling and converting Docker images to SIF..."

apptainer build mongodb.sif docker://mongo:latest
apptainer build ollama.sif docker://ollama/ollama
apptainer build agent.sif docker://adijida/agent:latest

echo "Starting MongoDB..."
apptainer exec \
  --bind "$(pwd)/volumes/mongo-data:/data/db" \
  --env MONGO_INITDB_ROOT_USERNAME=root \
  --env MONGO_INITDB_ROOT_PASSWORD=example \
  mongodb.sif \
  mongod --bind_ip_all &

sleep 5

echo "Starting Ollama..."
apptainer exec \
  --bind "$(pwd)/volumes/ollama-data:/root/.ollama" \
  --env OLLAMA_MODELS=/root/.ollama/models \
  --nv \
  ollama.sif \
  ollama serve &

sleep 5

echo "Starting Agent API..."
apptainer exec \
  --env-file dockerEnvironmentVariables.env \
  --network host \
  agent.sif \
  python app.py
