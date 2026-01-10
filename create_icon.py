"""
アイコン画像を追加するためのスクリプト
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """シンプルなアイコンを作成"""
    # 256x256のアイコンを作成
    size = 256
    img = Image.new('RGB', (size, size), color='#2196F3')  # 青色背景
    draw = ImageDraw.Draw(img)

    # 白い円を描画
    margin = 30
    draw.ellipse([margin, margin, size-margin, size-margin], fill='white')

    # 中央にSTの文字を描画（Simple Text Converter）
    try:
        # フォントサイズを大きくして太字に
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()

    # テキストを描画
    text = "ST"

    # テキストの位置を中央に
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - 10)

    draw.text(position, text, fill='#2196F3', font=font)

    # PNG形式で保存
    img.save('icon.png', 'PNG')

    # ICO形式で保存（Windows用）
    img.save('icon.ico', format='ICO', sizes=[(256, 256)])

    print('アイコンを作成しました: icon.png, icon.ico')

if __name__ == '__main__':
    try:
        create_icon()
    except Exception as e:
        print(f'エラー: {e}')
        print('Pillowライブラリが必要です: pip install Pillow')
