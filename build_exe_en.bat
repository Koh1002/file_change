@echo off
REM Fixed-length Text Converter - Build Script (English)
REM This script builds the EXE file without any Japanese characters

echo ===============================================
echo Fixed-length Text Converter - EXE Build
echo ===============================================
echo.

REM Check Python
echo [1/4] Checking Python installation...
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :python_found
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :python_found
)

echo.
echo ERROR: Python not found
echo.
echo Please install Python 3.8 or later from:
echo https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:python_found
echo Python command: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Create venv
echo [2/4] Preparing virtual environment...
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment
        echo.
        echo Try running this script as Administrator:
        echo Right-click this file and select "Run as administrator"
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo Using existing virtual environment
)
echo.

REM Activate venv
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment
    echo.
    echo Try deleting the "venv" folder and run this script again.
    echo.
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Install PyInstaller
echo [4/4] Installing PyInstaller...
echo This may take a few minutes...
echo.
pip install pyinstaller
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install PyInstaller
    echo.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo PyInstaller installed successfully
echo.

REM Check app.py
if not exist app.py (
    echo.
    echo ERROR: app.py not found
    echo.
    echo Make sure this script is in the same folder as app.py
    echo.
    pause
    exit /b 1
)

REM Build EXE
echo ===============================================
echo Building EXE file...
echo This will take 3-5 minutes. Please wait...
echo ===============================================
echo.
pyinstaller --onefile --noconsole --name FixedLengthConverter app.py
if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

REM Success
echo.
echo ===============================================
echo Build completed successfully!
echo ===============================================
echo.
echo EXE file location:
echo   %CD%\dist\FixedLengthConverter.exe
echo.
echo You can now distribute this EXE file.
echo.
echo NOTE: The EXE filename is "FixedLengthConverter.exe"
echo       You can rename it to any name you prefer.
echo.
pause
