#!/bin/bash

# Get the directory where the .command file is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"
source venv/bin/activate

python main.py