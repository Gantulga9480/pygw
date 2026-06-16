#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
export PYTHONPATH="$PARENT_DIR:$SCRIPT_DIR/examples"
cd "$SCRIPT_DIR/examples"
python -m survivors
