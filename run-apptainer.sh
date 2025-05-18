#!/bin/bash

set -e

# Create directories for persistent volumes
mkdir -p ./volumes/mongo-data
mkdir -p ./volumes/ollama-data
mkdir -p ./apptainerdata/agent

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

# Get absolute path to the Agents directory (where this script is)
AGENTS_DIR="$(cd "$(dirname "$0")"; pwd)"

echo "Starting Agents..."
apptainer exec \
  --env-file "$AGENTS_DIR/dockerEnvironmentVariables.env" \
  --bind "$AGENTS_DIR:/Agents" \
  --pwd /Agents \
  agent.sif \
  python run.py