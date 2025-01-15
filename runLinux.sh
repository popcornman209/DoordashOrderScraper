#!/bin/bash

# Get the directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"
source venv/bin/activate

python main.py