"""
icon.png を icon.ico に変換するスクリプト
"""

from PIL import Image
import os

def convert_png_to_ico():
    """icon.png を icon.ico に変換"""
    if not os.path.exists('icon.png'):
        print('エラー: icon.png が見つかりません')
        return False

    try:
        # PNGを開く
        img = Image.open('icon.png')

        # RGBAモードに変換（透明度を保持）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # ICO形式で保存（複数サイズ）
        img.save('icon.ico', format='ICO', sizes=[
            (16, 16),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256)
        ])

        print('✓ icon.ico を作成しました')
        print(f'  入力: icon.png ({img.size[0]}x{img.size[1]})')
        print(f'  出力: icon.ico (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)')
        return True

    except Exception as e:
        print(f'エラー: {e}')
        print('Pillowライブラリが必要です: pip install Pillow')
        return False

if __name__ == '__main__':
    convert_png_to_ico()
