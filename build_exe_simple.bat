@echo off
REM 固定長テキスト変換ツール - 簡易ビルドスクリプト
REM
REM このスクリプトは、より詳細なメッセージとエラーハンドリングを提供します。
REM ビルドに失敗する場合は、こちらのスクリプトを使用してください。
REM

title 固定長テキスト変換ツール - EXEビルド

:start
cls
echo.
echo ========================================================
echo   固定長テキスト変換ツール - 簡易ビルドスクリプト
echo ========================================================
echo.
echo このスクリプトは、EXEファイルを自動的に作成します。
echo.
echo 必要なもの：
echo   - Python 3.8以降がインストールされていること
echo   - インターネット接続
echo.
echo --------------------------------------------------------
echo.
pause

cls
echo.
echo ========================================================
echo   ステップ1: 環境チェック
echo ========================================================
echo.

REM Pythonコマンドの確認
echo Pythonコマンドを確認しています...
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo   [OK] python コマンドが見つかりました
    goto :check_version
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo   [OK] py コマンドが見つかりました
    goto :check_version
)

echo   [エラー] Pythonが見つかりません！
echo.
echo   Pythonをインストールしてください：
echo   https://www.python.org/downloads/
echo.
echo   インストール時の注意：
echo   - 「Add Python to PATH」に必ずチェックを入れてください
echo   - インストール後、コンピュータを再起動してください
echo.
goto :error_exit

:check_version
for /f "delims=" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   バージョン: %PYTHON_VERSION%
echo.
pause

cls
echo.
echo ========================================================
echo   ステップ2: 仮想環境の準備
echo ========================================================
echo.

if exist venv (
    echo 既存の仮想環境が見つかりました。
    echo.
    choice /C YN /M "既存の仮想環境を削除して新しく作成しますか"
    if errorlevel 2 goto :skip_venv_delete
    if errorlevel 1 goto :delete_venv
)

:create_venv
echo 仮想環境を作成しています...
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo.
    echo   [エラー] 仮想環境の作成に失敗しました。
    echo.
    echo   以下を試してください：
    echo   1. 管理者権限でこのスクリプトを実行
    echo   2. Pythonを再インストール
    echo   3. ディスク容量を確認
    echo.
    goto :error_exit
)
echo   [OK] 仮想環境を作成しました
goto :activate_venv

:delete_venv
echo 既存の仮想環境を削除しています...
rmdir /s /q venv
if exist venv (
    echo   [警告] 完全に削除できませんでしたが、続行します...
)
goto :create_venv

:skip_venv_delete
echo 既存の仮想環境を使用します。
echo.

:activate_venv
echo 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo   [エラー] 仮想環境のアクティベートに失敗しました。
    echo.
    echo   venvフォルダを削除してから再度実行してください：
    echo   rmdir /s /q venv
    echo.
    goto :error_exit
)
echo   [OK] 仮想環境をアクティベートしました
echo.
pause

cls
echo.
echo ========================================================
echo   ステップ3: PyInstallerのインストール
echo ========================================================
echo.

echo PyInstallerをインストールしています...
echo （この処理には数分かかる場合があります）
echo.
pip install --upgrade pip
pip install pyinstaller
if errorlevel 1 (
    echo.
    echo   [エラー] PyInstallerのインストールに失敗しました。
    echo.
    echo   以下を確認してください：
    echo   1. インターネット接続
    echo   2. ファイアウォール設定
    echo   3. プロキシ設定
    echo.
    goto :error_exit
)
echo.
echo   [OK] PyInstallerをインストールしました
echo.
pause

cls
echo.
echo ========================================================
echo   ステップ4: EXEファイルのビルド
echo ========================================================
echo.

echo 必要なファイルをチェックしています...
if not exist app.py (
    echo   [エラー] app.pyが見つかりません！
    echo.
    echo   このスクリプトは、app.pyと同じフォルダで実行してください。
    echo.
    goto :error_exit
)
echo   [OK] app.py が見つかりました
echo.

echo EXEファイルをビルドしています...
echo （この処理には3～5分かかります。しばらくお待ちください）
echo.
pyinstaller --onefile --noconsole --name "固定長テキスト変換ツール" app.py
if errorlevel 1 (
    echo.
    echo   [エラー] EXEのビルドに失敗しました。
    echo.
    echo   以下を確認してください：
    echo   1. ディスク容量（最低500MB以上必要）
    echo   2. ウイルス対策ソフトが干渉していないか
    echo   3. buildフォルダとdistフォルダを削除してから再実行
    echo.
    goto :error_exit
)

cls
echo.
echo ========================================================
echo   ビルド完了！
echo ========================================================
echo.
echo EXEファイルが正常に作成されました。
echo.
echo 【ファイルの場所】
echo   %CD%\dist\固定長テキスト変換ツール.exe
echo.
echo 【次のステップ】
echo   1. distフォルダを開く
echo   2. 「固定長テキスト変換ツール.exe」を配布先にコピー
echo   3. README.txtも一緒に配布してください
echo.
echo ========================================================
echo.
choice /C YN /M "distフォルダを開きますか"
if errorlevel 2 goto :normal_exit
if errorlevel 1 start explorer dist
goto :normal_exit

:error_exit
echo.
echo ========================================================
echo   エラーが発生しました
echo ========================================================
echo.
echo ビルドを中断しました。
echo 上記のエラーメッセージを確認して、問題を解決してください。
echo.
echo 不明な場合は、開発者にお問い合わせください。
echo.
pause
exit /b 1

:normal_exit
echo.
echo Enterキーを押すと終了します...
pause >nul
exit /b 0
