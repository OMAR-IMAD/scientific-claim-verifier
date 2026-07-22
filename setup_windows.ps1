$ErrorActionPreference = "Stop"

Write-Host "Creating Python 3.12 virtual environment..."
py -3.12 -m venv .venv

Write-Host "Activating environment..."
.\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing base dependencies..."
python -m pip install -r requirements-base.txt

Write-Host "Checking environment..."
python scripts\check_environment.py

Write-Host ""
Write-Host "Base setup completed successfully."
