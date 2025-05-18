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