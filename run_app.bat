@echo off
REM Quick Start - Run the app without building EXE
REM EXE化せずにアプリを起動（開発・UI確認用）

echo ===============================================
echo Fixed-length Text Converter - Quick Start
echo ===============================================
echo.
echo Starting the application...
echo (Close the GUI window to return here)
echo.

REM Check Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    python app.py
    goto :end
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    py app.py
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
