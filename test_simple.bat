@echo off
echo ========================================
echo Simple Test - Batch File and Python
echo ========================================
echo.
echo If you can see this message, the batch file is working.
echo.
echo Checking for Python...
echo.

where python
if %errorlevel% equ 0 (
    echo.
    echo Python found: python command
    python --version
    goto :found
)

where py
if %errorlevel% equ 0 (
    echo.
    echo Python found: py command
    py --version
    goto :found
)

echo.
echo Python NOT found
echo Please install Python from https://www.python.org/downloads/
echo.
goto :end

:found
echo.
echo Python check OK!
echo.

:end
echo ========================================
echo Test completed
echo ========================================
echo.
echo Press any key to exit...
pause >nul
