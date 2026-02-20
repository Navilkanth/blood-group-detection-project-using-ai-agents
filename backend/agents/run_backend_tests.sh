#!/bin/bash

echo "================================"
echo "Backend Test Suite Runner"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -r requirements-dev.txt

echo "Running tests..."
python tests/run_tests.py

echo ""
echo "Tests complete. Coverage report available in htmlcov/index.html"
