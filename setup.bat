@echo off
echo === Maze Game Environment Setup (Batch) ===

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.11 or later.
    pause
    exit /b
)

:: Create venv if missing
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate and install
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo No requirements.txt found.
)
echo Setup complete! Run the game with: run.bat
pause
