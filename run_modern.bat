@echo off
REM Run Modern UI Version (CustomTkinter)
REM モダンUI版を起動（開発・UI確認用）

echo ===============================================
echo Fixed-length Text Converter - Modern UI
echo ===============================================
echo.

REM Check if customtkinter is installed
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo CustomTkinter is not installed.
    echo Installing CustomTkinter...
    echo.
    pip install customtkinter
    echo.
)

echo Starting the modern UI application...
echo (Close the GUI window to return here)
echo.

REM Check Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    python app_modern.py
    goto :end
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    py app_modern.py
    goto :end
)

echo ERROR: Python not found
echo Please install Python from https://www.python.org/downloads/
echo.
pause
exit /b 1

:end
echo.
echo Application closed.
echo.
pause
