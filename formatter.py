"""
固定長テキストのフォーマット処理
"""

from models import (
    RECORD_LENGTH,
    HEADER_ACTIVATE_FIELDS,
    HEADER_DEPOSIT_FIELDS,
    DATA_RECORD_FIELDS,
    TRAILER_FIELDS,
    END_FIELDS
)


class FixedLengthFormatter:
    """固定長テキストのフォーマッター"""

    def __init__(self, format_type='activate', company_code='0000000'):
        """
        Args:
            format_type: 'activate' または 'deposit'
            company_code: カード発行会社コード（7桁）
        """
        self.format_type = format_type
        self.company_code = company_code

    def format_record(self, fields, values=None):
        """
        フィールド定義に従ってレコードを整形

        Args:
            fields: Fieldオブジェクトのリスト
            values: 可変値の辞書（フィールドインデックス: 値）

        Returns:
            str: 整形されたレコード（254文字）
        """
        if values is None:
            values = {}

        record = ''
        for i, field in enumerate(fields):
            value = values.get(i, '')
            record += field.format(value)

        # レコード長チェック
        if len(record) != RECORD_LENGTH:
            raise ValueError(
                f'レコード長が不正です: {len(record)}文字 '
                f'(期待値: {RECORD_LENGTH}文字)'
            )

        return record

    def create_header(self):
        """ヘッダーレコードを生成"""
        if self.format_type == 'activate':
            fields = HEADER_ACTIVATE_FIELDS
        else:
            fields = HEADER_DEPOSIT_FIELDS

        # カード発行会社コードを設定（インデックス1）
        values = {1: self.company_code}
        return self.format_record(fields, values)

    def create_data_record(self, seq_no, card_number, amount):
        """
        データレコードを生成

        Args:
            seq_no: ファイル内連番（1から）
            card_number: カード番号（16桁）
            amount: 入金額/追加入金額（最大7桁）

        Returns:
            str: 整形されたデータレコード（254文字）
        """
        values = {
            1: str(seq_no).zfill(6),     # 連番（6桁ゼロ埋め）
            2: card_number,              # カード番号
            3: str(amount).zfill(7),     # 入金額（7桁ゼロ埋め）
        }
        return self.format_record(DATA_RECORD_FIELDS, values)

    def create_trailer(self, data_count):
        """
        トレーラーレコードを生成

        Args:
            data_count: データ件数

        Returns:
            str: 整形されたトレーラーレコード（254文字）
        """
        values = {1: str(data_count).zfill(6)}  # データ件数（6桁ゼロ埋め）
        return self.format_record(TRAILER_FIELDS, values)

    def create_end(self):
        """エンドレコードを生成"""
        return self.format_record(END_FIELDS)

    def create_file_content(self, data_list):
        """
        固定長ファイル全体を生成

        Args:
            data_list: [(card_number, amount), ...] のリスト

        Returns:
            str: ファイル全体の内容（各行にCRLF付き）
        """
        lines = []

        # ヘッダー
        lines.append(self.create_header())

        # データレコード
        for i, (card_number, amount) in enumerate(data_list, start=1):
            lines.append(self.create_data_record(i, card_number, amount))

        # トレーラー
        lines.append(self.create_trailer(len(data_list)))

        # エンド
        lines.append(self.create_end())

        # 各行にCRLFを付けて結合
        return '\r\n'.join(lines) + '\r\n'
