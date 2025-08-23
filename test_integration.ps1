# PowerShell script to test Kirana Tap integration
Write-Host "🔍 Testing Kirana Tap Integration..." -ForegroundColor Green
Write-Host "This will verify that your Flask app can use the working BlinkitAutomation" -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    python --version
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH" -ForegroundColor Yellow
    exit 1
}

# Run the integration test
Write-Host "🚀 Running integration test..." -ForegroundColor Green
python test_integration.py

Write-Host ""
Write-Host "✅ Integration test completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"
