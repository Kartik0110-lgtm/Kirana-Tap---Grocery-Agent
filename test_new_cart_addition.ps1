# PowerShell script to test the new cart addition functionality
Write-Host "🚀 Testing New Cart Addition Functionality..." -ForegroundColor Green
Write-Host "This will test the improved add_first_item_to_cart function" -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    python --version
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH" -ForegroundColor Yellow
    exit 1
}

# Run the new cart addition test
Write-Host "🚀 Running new cart addition test..." -ForegroundColor Green
python test_new_cart_addition.py

Write-Host ""
Write-Host "✅ New cart addition test completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"
