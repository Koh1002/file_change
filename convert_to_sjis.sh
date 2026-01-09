#!/bin/bash
# バッチファイルをShift_JISに変換するスクリプト
#
# Windowsのコマンドプロンプトは Shift_JIS (CP932) を使用するため、
# Linux/Mac で作成した UTF-8 のバッチファイルを変換する必要があります。
#
# 使い方：
#   ./convert_to_sjis.sh

echo "========================================"
echo "バッチファイルをShift_JISに変換"
echo "========================================"
echo ""

# 変換対象のファイル
FILES=(
    "build_exe.bat"
    "build_exe_simple.bat"
    "build_exe_debug.bat"
    "test_bat.bat"
    "BUILD_MANUAL.txt"
)

# 各ファイルを変換
for FILE in "${FILES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo "[警告] $FILE が見つかりません。スキップします。"
        continue
    fi

    echo "変換中: $FILE"

    # 現在の文字コードを確認
    CURRENT_CHARSET=$(file -i "$FILE" | awk -F'charset=' '{print $2}')
    echo "  現在: $CURRENT_CHARSET"

    # UTF-8の場合のみ変換
    if [[ "$CURRENT_CHARSET" == "utf-8" ]]; then
        # 一時ファイルに変換
        iconv -f UTF-8 -t CP932 "$FILE" > "${FILE}.tmp"

        if [ $? -eq 0 ]; then
            # 変換成功：元のファイルを置き換え
            mv "${FILE}.tmp" "$FILE"
            echo "  変換後: Shift_JIS (CP932)"
            echo "  [OK] 変換完了"
        else
            # 変換失敗：一時ファイルを削除
            rm -f "${FILE}.tmp"
            echo "  [エラー] 変換に失敗しました"
        fi
    else
        echo "  [スキップ] 既に Shift_JIS または他の文字コードです"
    fi

    echo ""
done

echo "========================================"
echo "変換処理が完了しました"
echo "========================================"
echo ""
echo "注意："
echo "  - 変換後のファイルはWindowsで正しく動作します"
echo "  - Linux/Macでは文字化けして見える場合があります"
echo "  - 編集する場合は、UTF-8で編集後に再度このスクリプトを実行してください"
echo ""
