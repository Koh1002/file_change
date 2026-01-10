@echo off
REM Build Modern UI Version to EXE
REM モダンUI版をEXE化

echo ===============================================
echo Build Modern UI Version - EXE
echo ===============================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
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
echo Please install Python from https://www.python.org/downloads/
echo.
pause
exit /b 1

:python_found
echo Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Create venv
echo [2/5] Preparing virtual environment...
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
) else (
    echo Using existing virtual environment
)
echo.

REM Activate venv
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take a few minutes...
echo.
pip install customtkinter pyinstaller Pillow
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed
echo.

REM Check app_modern.py
if not exist app_modern.py (
    echo ERROR: app_modern.py not found
    pause
    exit /b 1
)

REM Build EXE
echo [5/5] Building EXE file...
echo This will take 3-5 minutes. Please wait...
echo.

REM Check for icon file
set ICON_PARAM=
if exist icon.ico (
    set ICON_PARAM=--icon=icon.ico
    echo Using icon: icon.ico
)

pyinstaller --onefile --noconsole --name FixedLengthConverter_Modern %ICON_PARAM% app_modern.py
if errorlevel 1 (
    echo ERROR: Build failed
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
echo   %CD%\dist\FixedLengthConverter_Modern.exe
echo.
echo This is the MODERN UI version with CustomTkinter.
echo.
pause
