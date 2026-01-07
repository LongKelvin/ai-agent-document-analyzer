# AI Agent Demo - Setup Script for Windows PowerShell
# This script automates the setup process

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "    🤖 AI Agent Document Analysis Demo - Setup Wizard" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python not found. Please install Python 3.10 or higher." -ForegroundColor Red
    Write-Host "     Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
Write-Host ""
Write-Host "🔍 Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✅ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "  📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies (this may take 2-3 minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  ❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host ""
Write-Host "🔍 Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "  ✅ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ⚠️  IMPORTANT: You need to add your Gemini API key!" -ForegroundColor Red
    Write-Host "     1. Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    Write-Host "     2. Edit .env file and replace 'your_api_key_here' with your actual key" -ForegroundColor Yellow
    Write-Host ""
    $openEnv = Read-Host "     Would you like to open .env file now? (y/n)"
    if ($openEnv -eq "y" -or $openEnv -eq "Y") {
        notepad .env
    }
}

# Run verification
Write-Host ""
Write-Host "✅ Running installation verification..." -ForegroundColor Yellow
python check_setup.py

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "    🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Make sure your Gemini API key is configured in .env" -ForegroundColor White
Write-Host "  2. Run the application:" -ForegroundColor White
Write-Host "     python -m app.main" -ForegroundColor Cyan
Write-Host "  3. Open your browser to: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "  - Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "  - Full Guide: README.md" -ForegroundColor White
Write-Host "  - Project Overview: PROJECT_SUMMARY.md" -ForegroundColor White
Write-Host ""

$runNow = Read-Host "Would you like to start the application now? (y/n)"
if ($runNow -eq "y" -or $runNow -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Starting AI Agent Demo Application..." -ForegroundColor Green
    Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python -m app.main
}
