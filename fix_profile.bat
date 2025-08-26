@echo off
echo Fixing Chrome Profile...
echo.

echo Removing LOCK file...
if exist "chrome-profile\Default\LOCK" (
    del "chrome-profile\Default\LOCK"
    echo LOCK file removed
) else (
    echo No LOCK file found
)

echo.
echo Restoring Cookies file...
if exist "chrome-profile\Default\Network\Cookies" (
    copy "chrome-profile\Default\Network\Cookies" "chrome-profile\Default\Cookies"
    echo Cookies file restored
) else (
    echo Cookies file not found in Network directory
)

echo.
echo Profile fix complete!
echo Try running your app again.
pause
