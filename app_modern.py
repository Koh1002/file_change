"""
固定長テキスト変換ツール - モダンGUIアプリケーション（CustomTkinter版）
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

from formatter import FixedLengthFormatter
from utils import (
    parse_input_text,
    validate_data_list,
    write_shift_jis_file,
    ValidationError
)

# CustomTkinterの外観設定
ctk.set_appearance_mode("System")  # System, Dark, Light
ctk.set_default_color_theme("blue")  # blue, green, dark-blue


class FixedLengthConverterApp:
    """固定長テキスト変換ツールのモダンGUIアプリケーション"""

    def __init__(self, root):
        self.root = root
        self.root.title('固定長テキスト変換ツール')
        self.root.geometry('900x750')

        # アイコンを設定（icon.icoまたはicon.pngがある場合）
        try:
            if os.path.exists('icon.ico'):
                self.root.iconbitmap('icon.ico')
            elif os.path.exists('icon.png'):
                from PIL import Image, ImageTk
                icon_image = Image.open('icon.png')
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)
        except Exception as e:
            pass  # アイコンファイルがない場合はスキップ

        # タブビュー
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill='both', expand=True, padx=20, pady=20)

        # タブ1: 一括アクティベート
        self.tab_activate = self.tabview.add("一括アクティベート")
        self.create_tab_ui(self.tab_activate, 'activate')

        # タブ2: 一括入金
        self.tab_deposit = self.tabview.add("一括入金")
        self.create_tab_ui(self.tab_deposit, 'deposit')

    def create_tab_ui(self, parent, tab_type):
        """タブのUIを作成"""
        # メインフレーム
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # ヘッダーフレーム（ロゴと説明）
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill='x', padx=10, pady=(10, 5))

        # ロゴ画像（icon.pngがある場合）
        try:
            if os.path.exists('icon.png'):
                from PIL import Image, ImageTk
                logo_image = Image.open('icon.png')
                logo_image = logo_image.resize((40, 40), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
                logo_label.image = logo_photo  # 参照を保持
                logo_label.pack(side='left', padx=(0, 10))
        except Exception:
            pass  # ロゴがない場合はスキップ

        # 説明ラベル
        info_label = ctk.CTkLabel(
            header_frame,
            text='📝 カード番号,入金額 の形式で1行ずつ入力（カンマまたはタブ区切り、Excelからコピペ可）',
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color=("#1f538d", "#3a7ebf")
        )
        info_label.pack(side='left', fill='x', expand=True)

        # データ入力エリア
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # テキストボックス
        text_area = ctk.CTkTextbox(
            input_frame,
            width=800,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=13, weight='bold'),
            wrap='none'
        )
        text_area.pack(fill='both', expand=True, padx=10, pady=10)

        # ボタンフレーム
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill='x', padx=10, pady=10)

        # サンプルボタン
        sample_btn = ctk.CTkButton(
            button_frame,
            text='📋 サンプル貼り付け',
            command=lambda: self.insert_sample(text_area),
            width=150,
            height=35,
            font=ctk.CTkFont(size=14, weight='bold')
        )
        sample_btn.pack(side='left', padx=5)

        # クリアボタン
        clear_btn = ctk.CTkButton(
            button_frame,
            text='🗑️ クリア',
            command=lambda: text_area.delete('1.0', 'end'),
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight='bold'),
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        clear_btn.pack(side='left', padx=5)

        # 生成ボタン（右側）
        generate_btn = ctk.CTkButton(
            button_frame,
            text='✨ ファイルを生成',
            command=lambda: self.generate_file(
                tab_type,
                text_area.get('1.0', 'end')
            ),
            width=180,
            height=40,
            font=ctk.CTkFont(size=14, weight='bold'),
            fg_color="#2e7d32",
            hover_color="#1b5e20"
        )
        generate_btn.pack(side='right', padx=5)

        # ステータスラベル
        status_label = ctk.CTkLabel(
            main_frame,
            text='💡 カード発行会社コード: 7130754（固定）',
            font=ctk.CTkFont(size=13, weight='bold'),
            text_color=("gray50", "gray70")
        )
        status_label.pack(pady=5, padx=10, anchor='w')

    def insert_sample(self, text_area):
        """サンプルデータを挿入"""
        sample_data = (
            '7130123456789012,10000\n'
            '7130123456789013,20000\n'
            '7130123456789014,5000\n'
        )
        text_area.delete('1.0', 'end')
        text_area.insert('1.0', sample_data)

    def generate_file(self, format_type, input_text):
        """ファイルを生成"""
        try:
            # カード発行会社コードは固定値
            company_code = '7130754'

            # 入力テキストのパース
            try:
                data_list = parse_input_text(input_text)
            except ValidationError as e:
                messagebox.showerror('入力エラー', str(e))
                return

            # データのバリデーション
            errors = validate_data_list(data_list)
            if errors:
                error_message = '\n'.join(errors)
                if len(errors) > 20:
                    error_message = '\n'.join(errors[:20]) + \
                                    f'\n\n... 他 {len(errors) - 20} 件のエラー'
                messagebox.showerror('バリデーションエラー', error_message)
                return

            # 保存ダイアログ
            format_name = '一括アクティベート' if format_type == 'activate' else '一括入金'
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            default_filename = f'トモズ様_{format_name}_{timestamp}.txt'

            file_path = filedialog.asksaveasfilename(
                title='保存先を選択',
                defaultextension='.txt',
                initialfile=default_filename,
                filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
            )

            if not file_path:
                return  # キャンセル

            # フォーマッター作成
            formatter = FixedLengthFormatter(
                format_type=format_type,
                company_code=company_code
            )

            # ファイル内容生成
            content = formatter.create_file_content(data_list)

            # ファイル書き込み（Shift_JIS、CRLF）
            write_shift_jis_file(file_path, content)

            # 成功メッセージ
            messagebox.showinfo(
                '作成完了',
                f'✅ ファイルを作成しました。\n\n'
                f'ファイル: {os.path.basename(file_path)}\n'
                f'データ件数: {len(data_list)}件\n'
                f'保存先: {file_path}'
            )

        except Exception as e:
            messagebox.showerror('エラー', f'処理中にエラーが発生しました:\n\n{str(e)}')


def main():
    """メイン関数"""
    root = ctk.CTk()
    app = FixedLengthConverterApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
