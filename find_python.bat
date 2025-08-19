@echo off
echo Searching for Python...
echo.

echo Checking PATH...
where python
if %errorlevel% neq 0 (
    echo Python not found in PATH
    echo.
    echo Searching common locations...
    echo.
    
    if exist "C:\Python39\python.exe" echo Found: C:\Python39\python.exe
    if exist "C:\Python310\python.exe" echo Found: C:\Python310\python.exe
    if exist "C:\Python311\python.exe" echo Found: C:\Python311\python.exe
    if exist "C:\Python312\python.exe" echo Found: C:\Python312\python.exe
    
    if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" echo Found: %LOCALAPPDATA%\Programs\Python\Python39\python.exe
    if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" echo Found: %LOCALAPPDATA%\Programs\Python\Python310\python.exe
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" echo Found: %LOCALAPPDATA%\Programs\Python\Python311\python.exe
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" echo Found: %LOCALAPPDATA%\Programs\Python\Python312\python.exe
    
    if exist "C:\Program Files\Python39\python.exe" echo Found: C:\Program Files\Python39\python.exe
    if exist "C:\Program Files\Python310\python.exe" echo Found: C:\Program Files\Python310\python.exe
    if exist "C:\Program Files\Python311\python.exe" echo Found: C:\Program Files\Python311\python.exe
    if exist "C:\Program Files\Python312\python.exe" echo Found: C:\Program Files\Python312\python.exe
) else (
    echo Python found in PATH!
)

echo.
echo Press any key to continue...
pause >nul
