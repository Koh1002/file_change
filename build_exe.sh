#!/bin/bash
# 固定長テキスト変換ツール - EXEビルドスクリプト（Linux/Mac用）
#
# 使い方：
#   1. Pythonがインストールされていることを確認
#   2. chmod +x build_exe.sh でスクリプトに実行権限を付与
#   3. ./build_exe.sh を実行
#

echo "==============================================="
echo "固定長テキスト変換ツール - EXEビルド"
echo "==============================================="
echo ""

# 仮想環境の作成（存在しない場合）
if [ ! -d "venv" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "エラー: 仮想環境の作成に失敗しました"
        exit 1
    fi
fi

# 仮想環境のアクティベート
echo "仮想環境をアクティベートしています..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "エラー: 仮想環境のアクティベートに失敗しました"
    exit 1
fi

# PyInstallerのインストール
echo "PyInstallerをインストールしています..."
pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "エラー: PyInstallerのインストールに失敗しました"
    exit 1
fi

# EXEのビルド
echo ""
echo "実行ファイルをビルドしています..."
echo "（この処理には数分かかる場合があります）"
echo ""
pyinstaller --onefile --noconsole --name "固定長テキスト変換ツール" app.py
if [ $? -ne 0 ]; then
    echo "エラー: ビルドに失敗しました"
    exit 1
fi

# 成功メッセージ
echo ""
echo "==============================================="
echo "ビルド完了！"
echo "==============================================="
echo ""
echo "実行ファイルは以下の場所に生成されました："
echo "  dist/固定長テキスト変換ツール"
echo ""
echo "このファイルを配布先にコピーすれば使用できます。"
echo ""
