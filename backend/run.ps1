# Quick Start Script for AI Agent Demo
# This script runs the application without reload mode to avoid Windows multiprocessing issues

Write-Host "Starting AI Agent Demo Application..." -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path ".\venv")) {
    Write-Host "[FAIL] Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run setup.ps1 first or create venv manually" -ForegroundColor Yellow
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".\.env")) {
    Write-Host "[WARN] .env file not found!" -ForegroundColor Yellow
    Write-Host "   Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "   Please edit .env and add your GEMINI_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after adding your API key"
}

Write-Host "Starting server (without auto-reload for Windows compatibility)..." -ForegroundColor Green
Write-Host ""
Write-Host "Open your browser to: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Run without reload to avoid multiprocessing issues on Windows
.\venv\Scripts\python.exe -c "import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8000)"
