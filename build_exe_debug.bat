@echo off
setlocal enabledelayedexpansion

REM ============================================
REM 固定長テキスト変換ツール - デバッグ版ビルドスクリプト
REM ============================================

set LOG_FILE=build_log.txt

echo ビルド開始 %date% %time% > %LOG_FILE%
echo. >> %LOG_FILE%

echo ===============================================
echo 固定長テキスト変換ツール - EXEビルド
echo ===============================================
echo.
echo ログファイル: %LOG_FILE%
echo エラーが発生した場合は、このファイルを確認してください。
echo.

REM Python確認
echo Python確認中... >> %LOG_FILE%
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo Python found: python >> %LOG_FILE%
    goto :python_found
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo Python found: py >> %LOG_FILE%
    goto :python_found
)

echo ERROR: Python not found >> %LOG_FILE%
echo.
echo [エラー] Pythonが見つかりません
echo.
echo 以下をインストールしてください:
echo https://www.python.org/downloads/
echo.
echo インストール時に「Add Python to PATH」にチェックを入れてください。
echo.
echo 詳細はログファイルを確認: %LOG_FILE%
echo.
pause
exit /b 1

:python_found
%PYTHON_CMD% --version >> %LOG_FILE% 2>&1
echo Python: %PYTHON_CMD%
echo.

REM 仮想環境作成
echo 仮想環境を準備中... >> %LOG_FILE%
if not exist venv (
    echo 仮想環境を作成しています...
    echo Creating venv... >> %LOG_FILE%
    %PYTHON_CMD% -m venv venv >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo ERROR: venv creation failed >> %LOG_FILE%
        echo.
        echo [エラー] 仮想環境の作成に失敗しました
        echo 詳細はログファイルを確認: %LOG_FILE%
        echo.
        pause
        exit /b 1
    )
    echo venv created successfully >> %LOG_FILE%
) else (
    echo venv already exists >> %LOG_FILE%
)
echo 仮想環境OK
echo.

REM アクティベート
echo 仮想環境をアクティベート中... >> %LOG_FILE%
call venv\Scripts\activate.bat >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: venv activation failed >> %LOG_FILE%
    echo.
    echo [エラー] 仮想環境のアクティベートに失敗しました
    echo venvフォルダを削除して再実行してください
    echo 詳細はログファイルを確認: %LOG_FILE%
    echo.
    pause
    exit /b 1
)
echo venv activated >> %LOG_FILE%
echo アクティベートOK
echo.

REM PyInstallerインストール
echo PyInstallerをインストール中... >> %LOG_FILE%
echo PyInstallerをインストールしています...（数分かかります）
echo.
pip install pyinstaller >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller installation failed >> %LOG_FILE%
    echo.
    echo [エラー] PyInstallerのインストールに失敗しました
    echo インターネット接続を確認してください
    echo 詳細はログファイルを確認: %LOG_FILE%
    echo.
    pause
    exit /b 1
)
echo PyInstaller installed >> %LOG_FILE%
echo PyInstallerインストールOK
echo.

REM app.py確認
if not exist app.py (
    echo ERROR: app.py not found >> %LOG_FILE%
    echo.
    echo [エラー] app.pyが見つかりません
    echo このスクリプトをapp.pyと同じフォルダで実行してください
    echo 詳細はログファイルを確認: %LOG_FILE%
    echo.
    pause
    exit /b 1
)
echo app.py found >> %LOG_FILE%

REM ビルド
echo ===============================================
echo EXEファイルをビルドしています...
echo （3-5分かかります。お待ちください）
echo ===============================================
echo.
echo Building EXE... >> %LOG_FILE%
pyinstaller --onefile --noconsole --name "固定長テキスト変換ツール" app.py >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo ERROR: Build failed >> %LOG_FILE%
    echo.
    echo [エラー] ビルドに失敗しました
    echo 詳細はログファイルを確認: %LOG_FILE%
    echo.
    pause
    exit /b 1
)
echo Build completed >> %LOG_FILE%

REM 成功
echo.
echo ===============================================
echo ビルド成功！
echo ===============================================
echo.
echo EXEファイル: dist\固定長テキスト変換ツール.exe
echo.
echo Build successful >> %LOG_FILE%

if exist "dist\固定長テキスト変換ツール.exe" (
    echo EXE file verified >> %LOG_FILE%
    echo EXEファイルの作成を確認しました
) else (
    echo WARNING: EXE file not found >> %LOG_FILE%
    echo 警告: EXEファイルが見つかりません
)

echo.
echo ログファイル: %LOG_FILE%
echo.
pause
