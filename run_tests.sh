#!/usr/bin/env bash
set -euo pipefail

# Activate venv (Git Bash на Windows)
source venv/Scripts/activate

# Add src to PYTHONPATH for this session
export PYTHONPATH="$(pwd)/src"

# Run unittest discovery
python -m unittest discover -v -s tests -p "test_*.py"

# Command for run tests in Git Bash on Windows:
# Shellbash run_tests.sh