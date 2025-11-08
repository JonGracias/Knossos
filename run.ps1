# run.ps1 – Run Maze Game in Windows PowerShell
if (-not (Test-Path ".\venv")) {
    Write-Host "❌ Virtual environment not found. Run setup.ps1 first!" -ForegroundColor Red
    exit 1
}

Write-Host "Launching Maze Game..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1
python MazeGame.py
pause
