#!/bin/bash

HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

export OLLAMA_HOST="http://${HOST_IP}:11434"

echo "Detected host IP: $HOST_IP"
echo "Using OLLAMA_HOST=$OLLAMA_HOST"

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
  --env OLLAMA_HOST=$OLLAMA_HOST \
  --env HOST_IP=$HOST_IP \
  --env-file "$AGENTS_DIR/dockerEnvironmentVariables.env" \
  --bind "$AGENTS_DIR:/Agents" \
  --pwd /Agents \
  agent.sif \
  python run.py