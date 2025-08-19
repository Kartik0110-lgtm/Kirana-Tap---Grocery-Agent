@echo off
echo ========================================
echo    Kirana Tap - AI Grocery Assistant
echo ========================================
echo.

echo Searching for Python installation...
echo.

set PYTHON_FOUND=0

REM Try common Python locations
if exist "C:\Python39\python.exe" (
    set PYTHON_PATH=C:\Python39\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Python39\
) else if exist "C:\Python310\python.exe" (
    set PYTHON_PATH=C:\Python310\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Python310\
) else if exist "C:\Python311\python.exe" (
    set PYTHON_PATH=C:\Python311\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Python311\
) else if exist "C:\Python312\python.exe" (
    set PYTHON_PATH=C:\Python312\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Python312\
) else if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: %LOCALAPPDATA%\Programs\Python\Python39\
) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python310\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: %LOCALAPPDATA%\Programs\Python\Python310\
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: %LOCALAPPDATA%\Programs\Python\Python311\
) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: %LOCALAPPDATA%\Programs\Python\Python312\
) else if exist "C:\Program Files\Python39\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python39\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Program Files\Python39\
) else if exist "C:\Program Files\Python310\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python310\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Program Files\Python310\
) else if exist "C:\Program Files\Python311\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python311\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Program Files\Python311\
) else if exist "C:\Program Files\Python312\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python312\python.exe
    set PYTHON_FOUND=1
    echo Found Python at: C:\Program Files\Python312\
)

if %PYTHON_FOUND%==0 (
    echo.
    echo ERROR: Python not found in common locations!
    echo.
    echo Please do ONE of the following:
    echo.
    echo OPTION 1 (RECOMMENDED):
    echo 1. Go to https://python.org/downloads/
    echo 2. Download and install Python
    echo 3. Make sure to check "Add Python to PATH" during installation
    echo 4. Restart your computer
    echo.
    echo OPTION 2:
    echo 1. Find where Python is installed on your system
    echo 2. Add that path to your system PATH variable
    echo.
    echo Press any key to continue...
    pause >nul
    exit /b 1
)

echo.
echo Using Python at: %PYTHON_PATH%
echo.

echo Checking Python version...
"%PYTHON_PATH%" --version

echo.
echo Installing dependencies...
"%PYTHON_PATH%" -m pip install -r requirements.txt

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

"%PYTHON_PATH%" app.py

pause
