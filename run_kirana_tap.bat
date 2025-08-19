@echo off
echo ========================================
echo    Kirana Tap - AI Grocery Assistant
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Checking version...
python --version

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking if .env file exists...
if not exist .env (
    echo Creating .env file from template...
    copy env_template.txt .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your OpenAI API key
    echo Get your API key from: https://platform.openai.com/api-keys
    echo.
    notepad .env
)

echo.
echo Starting Kirana Tap...
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
