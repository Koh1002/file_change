@echo off
REM 固定長テキスト変換ツール - EXEビルドスクリプト（Windows用）
REM
REM 使い方：
REM   1. Pythonがインストールされていることを確認
REM   2. このスクリプトをダブルクリックまたはコマンドプロンプトで実行
REM

echo ===============================================
echo 固定長テキスト変換ツール - EXEビルド
echo ===============================================
echo.

REM Pythonのインストール確認
echo [1/4] Pythonのインストールを確認しています...
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
echo エラー: Pythonがインストールされていません。
echo.
echo 以下のURLからPython 3.8以降をインストールしてください：
echo https://www.python.org/downloads/
echo.
echo インストール時に「Add Python to PATH」にチェックを入れてください。
echo.
pause
exit /b 1

:python_found
echo   Python: %PYTHON_CMD%
for /f "delims=" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   バージョン: %PYTHON_VERSION%
echo.

REM 仮想環境の作成（存在しない場合）
echo [2/4] 仮想環境を準備しています...
if not exist venv (
    echo   仮想環境を作成しています...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo.
        echo エラー: 仮想環境の作成に失敗しました。
        echo.
        echo 考えられる原因：
        echo   - Pythonのインストールが不完全
        echo   - ディスク容量不足
        echo   - アクセス権限の問題
        echo.
        echo 解決策：
        echo   1. Pythonを再インストールしてみてください
        echo   2. 管理者権限でこのスクリプトを実行してみてください
        echo.
        pause
        exit /b 1
    )
    echo   仮想環境を作成しました。
) else (
    echo   既存の仮想環境を使用します。
)
echo.

REM 仮想環境のアクティベート
echo [3/4] 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo エラー: 仮想環境のアクティベートに失敗しました。
    echo.
    echo 考えられる原因：
    echo   - venvフォルダが壊れている
    echo   - アクティベートスクリプトが見つからない
    echo.
    echo 解決策：
    echo   1. venvフォルダを削除してから再度実行してください
    echo   2. rmdir /s /q venv で削除できます
    echo.
    pause
    exit /b 1
)
echo   仮想環境をアクティベートしました。
echo.

REM PyInstallerのインストール
echo [4/4] PyInstallerをインストールしています...
pip install pyinstaller
if errorlevel 1 (
    echo.
    echo エラー: PyInstallerのインストールに失敗しました。
    echo.
    echo 考えられる原因：
    echo   - インターネット接続の問題
    echo   - pipのバージョンが古い
    echo.
    echo 解決策：
    echo   1. インターネット接続を確認してください
    echo   2. python -m pip install --upgrade pip でpipを更新してください
    echo.
    pause
    exit /b 1
)
echo   PyInstallerをインストールしました。
echo.

REM EXEのビルド
echo ===============================================
echo EXEファイルをビルドしています...
echo （この処理には数分かかる場合があります）
echo ===============================================
echo.
pyinstaller --onefile --noconsole --name "固定長テキスト変換ツール" app.py
if errorlevel 1 (
    echo.
    echo エラー: EXEのビルドに失敗しました。
    echo.
    echo 考えられる原因：
    echo   - app.pyファイルが見つからない
    echo   - 必要なモジュールが不足している
    echo   - ディスク容量不足
    echo.
    echo 解決策：
    echo   1. このスクリプトがapp.pyと同じフォルダにあるか確認してください
    echo   2. ディスク容量を確認してください
    echo   3. ウイルス対策ソフトが干渉していないか確認してください
    echo.
    pause
    exit /b 1
)

REM 成功メッセージ
echo.
echo ===============================================
echo ビルド完了！
echo ===============================================
echo.
echo EXEファイルは以下の場所に生成されました：
echo   %CD%\dist\固定長テキスト変換ツール.exe
echo.
echo このEXEファイルを配布先にコピーすれば使用できます。
echo.
echo Enterキーを押すと終了します...
pause >nul
