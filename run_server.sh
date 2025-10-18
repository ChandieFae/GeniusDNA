#!/bin/bash
# Script to run the GeniusDNA API server

echo "Starting GeniusDNA API server..."
cd "$(dirname "$0")"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
