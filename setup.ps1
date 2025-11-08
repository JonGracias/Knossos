# setup.ps1 – One-click environment setup for the Maze Game project
# Run this script by right-clicking > "Run with PowerShell" or from the terminal with: ./setup.ps1

Write-Host "=== Maze Game Environment Setup ===" -ForegroundColor Cyan

# Step 1. Ensure Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found in PATH. Please install Python 3.11 or later." -ForegroundColor Red
    exit 1
}

# Step 2. Create virtual environment if it doesn’t exist
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}
else {
    Write-Host "Virtual environment already exists."
}

# Step 3. Activate environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Step 4. Upgrade pip and setuptools
Write-Host "Upgrading pip and setuptools..."
python -m pip install --upgrade pip setuptools wheel

# Step 5. Install dependencies from requirements.txt
if (Test-Path ".\requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
}
else {
    Write-Host "No requirements.txt found; skipping dependency install." -ForegroundColor Yellow
}

# Step 6. Verify Pygame
Write-Host "Testing Pygame installation..."
python - << 'EOF'
try:
    import pygame
    print("✅ Pygame imported successfully!", pygame.__version__)
except ImportError:
    print("❌ Pygame not found.")
EOF

Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host "You can now run your game with: `python MazeGame.py`" -ForegroundColor Yellow
pause
