#!/bin/bash

set -e

# Create directories for persistent volumes
mkdir -p ./volumes/mongo-data
mkdir -p ./volumes/ollama-data
mkdir -p ./apptainerdata/agent

# Convert docker images to SIF files (if not already done)
echo "Pulling and converting Docker images to SIF..."

# Disable cache explicitly for each build
echo "Building MongoDB image..."
SINGULARITY_DISABLE_CACHE=True apptainer build mongodb.sif docker://mongo:latest

echo "Building Ollama image..."
SINGULARITY_DISABLE_CACHE=True apptainer build ollama.sif docker://ollama/ollama

echo "Building Agent image..."
SINGULARITY_DISABLE_CACHE=True apptainer build agent.sif docker://adijida/agent:latest

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
  --bind "$(pwd)/agent:/agent" \
  --bind "$(pwd)/apptainerdata/agent:/agent/data" \
  agent.sif \
  bash -c "cd /agent && python run.py"