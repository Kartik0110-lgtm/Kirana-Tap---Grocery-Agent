# PowerShell script to run the debug search test
Write-Host "🔍 Running Blinkit Search Debug Test..." -ForegroundColor Green

# Check if Python is available
try {
    python --version
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH" -ForegroundColor Yellow
    exit 1
}

# Check if required packages are installed
Write-Host "📦 Checking required packages..." -ForegroundColor Yellow
try {
    python -c "import selenium; print('✅ Selenium installed')"
} catch {
    Write-Host "❌ Selenium not installed. Installing..." -ForegroundColor Red
    pip install selenium
}

# Run the debug script
Write-Host "🚀 Starting debug test..." -ForegroundColor Green
python debug_search.py

Write-Host "✅ Debug test completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"
