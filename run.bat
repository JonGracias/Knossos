@echo off
echo === Running Maze Game ===
if not exist venv (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b
)
call venv\Scripts\activate.bat
python MazeGame.py
pause
