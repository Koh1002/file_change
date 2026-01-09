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

REM 仮想環境の作成（存在しない場合）
if not exist venv (
    echo 仮想環境を作成しています...
    python -m venv venv
    if errorlevel 1 (
        echo エラー: 仮想環境の作成に失敗しました
        pause
        exit /b 1
    )
)

REM 仮想環境のアクティベート
echo 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました
    pause
    exit /b 1
)

REM PyInstallerのインストール
echo PyInstallerをインストールしています...
pip install pyinstaller
if errorlevel 1 (
    echo エラー: PyInstallerのインストールに失敗しました
    pause
    exit /b 1
)

REM EXEのビルド
echo.
echo EXEファイルをビルドしています...
echo （この処理には数分かかる場合があります）
echo.
pyinstaller --onefile --noconsole --name "固定長テキスト変換ツール" app.py
if errorlevel 1 (
    echo エラー: EXEのビルドに失敗しました
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
echo   dist\固定長テキスト変換ツール.exe
echo.
echo このEXEファイルを配布先にコピーすれば使用できます。
echo.
pause
