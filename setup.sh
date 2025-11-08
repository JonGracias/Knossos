#!/bin/bash
echo "=== Maze Game Environment Setup ==="

# Ensure python3 exists
if ! command -v python3 &> /dev/null; then
  echo "❌ Python3 not found. Please install Python 3.11 or later."
  exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
else
  echo "Virtual environment already exists."
fi

# Activate and install
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "⚠️ No requirements.txt found; skipping dependencies."
fi

echo "Verifying pygame..."
python3 - <<EOF
try:
    import pygame
    print("✅ Pygame imported successfully! Version:", pygame.__version__)
except ImportError:
    print("❌ Pygame not found.")
EOF

echo "=== Setup Complete! ==="
echo "Run the game with: ./run.sh"
