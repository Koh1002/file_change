"""
固定長レコードのフィールド定義
"""


class Field:
    """固定長フィールドの定義"""

    def __init__(self, length, align='left', padding=' ', fixed_value=None):
        """
        Args:
            length: フィールド長（バイト数）
            align: 'left' または 'right'（左寄せ/右寄せ）
            padding: パディング文字（' ' または '0'）
            fixed_value: 固定値（Noneの場合は可変）
        """
        self.length = length
        self.align = align
        self.padding = padding
        self.fixed_value = fixed_value

    def format(self, value=''):
        """値をフィールド長に整形"""
        # 固定値がある場合はそれを使用
        if self.fixed_value is not None:
            value = str(self.fixed_value)
        else:
            value = str(value) if value else ''

        # 長さ調整
        if len(value) > self.length:
            raise ValueError(f'値が長すぎます: {value} (最大{self.length}桁)')

        if self.align == 'right':
            return value.rjust(self.length, self.padding)
        else:
            return value.ljust(self.length, self.padding)


# レコード総長（CRLF除く）
RECORD_LENGTH = 254


# ========================================
# ヘッダーレコード定義
# ========================================

# 一括アクティベート ヘッダー（データ区分=1, 取引区分=0201）
HEADER_ACTIVATE_FIELDS = [
    Field(1, fixed_value='1'),           # データ区分
    Field(7, align='right', padding='0'), # カード発行会社コード（可変）
    Field(4, fixed_value='0201'),        # 取引区分
    Field(1, fixed_value='0'),           # 登録・結果区分
    Field(241, padding=' '),             # ダミー
]

# 一括入金 ヘッダー（データ区分=1, 取引区分=0202）
HEADER_DEPOSIT_FIELDS = [
    Field(1, fixed_value='1'),           # データ区分
    Field(7, align='right', padding='0'), # カード発行会社コード（可変）
    Field(4, fixed_value='0202'),        # 取引区分
    Field(1, fixed_value='0'),           # 登録・結果区分
    Field(1, padding=' '),               # 利用停止カード入金可否フラグ
    Field(240, padding=' '),             # ダミー
]


# ========================================
# データレコード定義
# ========================================

# データレコード（データ区分=2）
# 一括アクティベートと一括入金で共通
DATA_RECORD_FIELDS = [
    Field(1, fixed_value='2'),           # データ区分
    Field(6, align='right', padding='0'), # ファイル内連番（可変）
    Field(16, align='left', padding=' '), # カード番号（可変）
    Field(7, align='right', padding='0'), # 入金額/追加入金額（可変）
    Field(30, padding=' '),              # 端末番号
    Field(15, padding=' '),              # 端末処理番号
    Field(16, align='right', padding=' ', fixed_value='100000998'), # 固定値（項番7）
    Field(1, fixed_value='2'),           # 固定値（項番8）
    Field(4, fixed_value='A102'),        # 固定値（項番9）
    Field(158, padding=' '),             # ダミー（残り）254桁に調整
]


# ========================================
# トレーラーレコード定義
# ========================================

# トレーラーレコード（データ区分=8）
TRAILER_FIELDS = [
    Field(1, fixed_value='8'),           # データ区分
    Field(6, align='right', padding='0'), # データ件数（可変）
    Field(247, padding=' '),             # ダミー
]


# ========================================
# エンドレコード定義
# ========================================

# エンドレコード（データ区分=9）
END_FIELDS = [
    Field(1, fixed_value='9'),           # データ区分
    Field(253, padding=' '),             # ダミー
]
