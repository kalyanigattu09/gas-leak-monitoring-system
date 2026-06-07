# Smart Gas Monitoring System — Module 1 environment setup (Windows PowerShell)
# Run from project root:  .\scripts\setup_env.ps1

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "=== Smart Gas Monitoring — Module 1 Setup ===" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"

# Resolve Python executable
$PythonCmd = $null
foreach ($candidate in @("python", "python3", "py")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        if ($candidate -eq "py") {
            $PythonCmd = "py -3"
        } else {
            $PythonCmd = $candidate
        }
        break
    }
}

if (-not $PythonCmd) {
    Write-Host ""
    Write-Host "ERROR: Python 3.10+ is not installed or not on PATH." -ForegroundColor Red
    Write-Host "Install from https://www.python.org/downloads/ and enable 'Add Python to PATH'." -ForegroundColor Yellow
    exit 1
}

Write-Host "Using Python: $PythonCmd" -ForegroundColor Green

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    Invoke-Expression "$PythonCmd -m venv venv"
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Gray
}

# Activate venv
$ActivateScript = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    Write-Host "ERROR: Could not find venv activation script." -ForegroundColor Red
    exit 1
}
. $ActivateScript

Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# Copy .env.example to .env if missing
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example — update DB_PASSWORD and SECRET_KEY." -ForegroundColor Yellow
} else {
    Write-Host ".env already exists." -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Install PostgreSQL and create database (see scripts/create_db.sql)"
Write-Host "  2. Edit .env with your PostgreSQL credentials"
Write-Host "  3. Activate venv:  .\venv\Scripts\Activate.ps1"
Write-Host "  4. Run migrations:  python manage.py migrate"
Write-Host "  5. Start server:    python manage.py runserver"
Write-Host ""
