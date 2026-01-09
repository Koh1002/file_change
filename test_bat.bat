@echo off
echo ========================================
echo バッチファイル動作テスト
echo ========================================
echo.
echo このメッセージが表示されれば、バッチファイルは動作しています。
echo.
echo Pythonを確認します...
echo.

where python
if %errorlevel% equ 0 (
    echo.
    echo Pythonが見つかりました（python）
    python --version
    goto :found
)

where py
if %errorlevel% equ 0 (
    echo.
    echo Pythonが見つかりました（py）
    py --version
    goto :found
)

echo.
echo Pythonが見つかりません
echo.
goto :end

:found
echo.
echo Python確認OK
echo.

:end
echo ========================================
echo テスト完了
echo ========================================
echo.
echo Enterキーを押すと終了します
pause >nul
