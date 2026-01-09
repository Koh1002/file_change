"""
固定長テキスト変換ツール - GUIアプリケーション
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import os

from formatter import FixedLengthFormatter
from utils import (
    parse_input_text,
    validate_data_list,
    validate_company_code,
    write_shift_jis_file,
    ValidationError
)


class FixedLengthConverterApp:
    """固定長テキスト変換ツールのGUIアプリケーション"""

    def __init__(self, root):
        self.root = root
        self.root.title('固定長テキスト変換ツール')
        self.root.geometry('800x700')

        # タブコントロール
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # タブ1: 一括アクティベート
        self.tab_activate = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_activate, text='一括アクティベート')
        self.create_tab_ui(self.tab_activate, 'activate')

        # タブ2: 一括入金
        self.tab_deposit = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_deposit, text='一括入金')
        self.create_tab_ui(self.tab_deposit, 'deposit')

    def create_tab_ui(self, parent, tab_type):
        """タブのUIを作成"""
        # カード発行会社コード入力
        frame_company = ttk.LabelFrame(parent, text='カード発行会社コード', padding=10)
        frame_company.pack(fill='x', padx=10, pady=10)

        ttk.Label(
            frame_company,
            text='7桁の半角数字（未入力の場合は0000000）:'
        ).pack(side='left', padx=5)

        company_entry = ttk.Entry(frame_company, width=15)
        company_entry.pack(side='left', padx=5)
        company_entry.insert(0, '0000000')

        # データ入力エリア
        frame_input = ttk.LabelFrame(parent, text='データ入力', padding=10)
        frame_input.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(
            frame_input,
            text='カード番号,入金額 の形式で1行ずつ入力\n'
                 '（カンマまたはタブ区切り、Excelからコピペ可）',
            foreground='blue'
        ).pack(anchor='w', padx=5, pady=5)

        # スクロール付きテキストエリア
        text_area = scrolledtext.ScrolledText(
            frame_input,
            width=80,
            height=15,
            wrap='none'
        )
        text_area.pack(fill='both', expand=True, padx=5, pady=5)

        # ボタンフレーム
        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.pack(fill='x', padx=5, pady=5)

        ttk.Button(
            frame_buttons,
            text='サンプル貼り付け',
            command=lambda: self.insert_sample(text_area)
        ).pack(side='left', padx=5)

        ttk.Button(
            frame_buttons,
            text='クリア',
            command=lambda: text_area.delete('1.0', 'end')
        ).pack(side='left', padx=5)

        # 出力ボタン
        frame_output = ttk.Frame(parent)
        frame_output.pack(fill='x', padx=10, pady=10)

        ttk.Button(
            frame_output,
            text='ファイルを生成',
            command=lambda: self.generate_file(
                tab_type,
                company_entry.get(),
                text_area.get('1.0', 'end')
            ),
            style='Accent.TButton'
        ).pack(side='left', padx=5)

        # スタイル設定（アクセントボタン）
        style = ttk.Style()
        style.configure('Accent.TButton', font=('', 11, 'bold'))

    def insert_sample(self, text_area):
        """サンプルデータを挿入"""
        sample_data = (
            '7130123456789012,10000\n'
            '7130123456789013,20000\n'
            '7130123456789014,5000\n'
        )
        text_area.delete('1.0', 'end')
        text_area.insert('1.0', sample_data)

    def generate_file(self, format_type, company_code, input_text):
        """ファイルを生成"""
        try:
            # カード発行会社コードのバリデーション
            if not company_code or not company_code.strip():
                company_code = '0000000'  # デフォルト値
            else:
                validate_company_code(company_code)

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
                company_code=company_code.zfill(7)
            )

            # ファイル内容生成
            content = formatter.create_file_content(data_list)

            # ファイル書き込み（Shift_JIS、CRLF）
            write_shift_jis_file(file_path, content)

            # 成功メッセージ
            messagebox.showinfo(
                '作成完了',
                f'ファイルを作成しました。\n\n'
                f'ファイル: {os.path.basename(file_path)}\n'
                f'データ件数: {len(data_list)}件\n'
                f'保存先: {file_path}'
            )

        except Exception as e:
            messagebox.showerror('エラー', f'処理中にエラーが発生しました:\n\n{str(e)}')


def main():
    """メイン関数"""
    root = tk.Tk()
    app = FixedLengthConverterApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
