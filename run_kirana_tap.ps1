Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Kirana Tap - AI Grocery Assistant" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Searching for Python installation..." -ForegroundColor Yellow
Write-Host ""

$pythonPath = $null

# Try to find Python using Get-Command first
try {
    $pythonPath = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
    Write-Host "Found Python in PATH: $pythonPath" -ForegroundColor Green
} catch {
    Write-Host "Python not found in PATH, searching common locations..." -ForegroundColor Yellow
    
    # Common Python installation paths
    $commonPaths = @(
        "C:\Python39\python.exe",
        "C:\Python310\python.exe", 
        "C:\Python311\python.exe",
        "C:\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "C:\Program Files\Python39\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python312\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonPath = $path
            Write-Host "Found Python at: $path" -ForegroundColor Green
            break
        }
    }
}

if (-not $pythonPath) {
    Write-Host ""
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please do ONE of the following:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPTION 1 (RECOMMENDED):" -ForegroundColor Cyan
    Write-Host "1. Go to https://python.org/downloads/" -ForegroundColor White
    Write-Host "2. Download and install Python" -ForegroundColor White
    Write-Host "3. Make sure to check 'Add Python to PATH' during installation" -ForegroundColor White
    Write-Host "4. Restart your computer" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTION 2:" -ForegroundColor Cyan
    Write-Host "1. Find where Python is installed on your system" -ForegroundColor White
    Write-Host "2. Tell me the exact path to python.exe" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to continue"
    exit 1
}

Write-Host ""
Write-Host "Using Python at: $pythonPath" -ForegroundColor Green
Write-Host ""

Write-Host "Checking Python version..." -ForegroundColor Yellow
& $pythonPath --version

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $pythonPath -m pip install -r requirements.txt

Write-Host ""
Write-Host "Checking if .env file exists..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env_template.txt" ".env"
    Write-Host ""
    Write-Host "IMPORTANT: Please edit the .env file and add your OpenAI API key" -ForegroundColor Red
    Write-Host "Get your API key from: https://platform.openai.com/api-keys" -ForegroundColor White
    Write-Host ""
    notepad ".env"
}

Write-Host ""
Write-Host "Starting Kirana Tap..." -ForegroundColor Green
Write-Host ""
Write-Host "The application will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& $pythonPath app.py

Read-Host "Press Enter to continue"

