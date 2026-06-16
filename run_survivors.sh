#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/examples"
cd "$SCRIPT_DIR/examples"
python -m survivors
