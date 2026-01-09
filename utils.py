"""
ユーティリティ関数（パース、バリデーション、ファイル書き込み）
"""

import re


class ValidationError(Exception):
    """バリデーションエラー"""
    pass


def parse_input_text(text):
    """
    テキストエリアの入力をパースして (card_number, amount) のリストに変換

    Args:
        text: 入力テキスト（カンマまたはタブ区切り、改行区切り）

    Returns:
        list: [(card_number, amount), ...] のリスト

    Raises:
        ValidationError: パース失敗時
    """
    lines = text.strip().split('\n')
    data_list = []

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue  # 空行はスキップ

        # タブまたはカンマで分割
        parts = re.split(r'[,\t]', line)
        if len(parts) < 2:
            raise ValidationError(
                f'行{i}: カード番号と入金額をカンマまたはタブで区切って入力してください\n'
                f'入力内容: {line}'
            )

        card_number = parts[0].strip()
        amount = parts[1].strip()

        data_list.append((card_number, amount))

    return data_list


def validate_card_number(card_number):
    """
    カード番号のバリデーション

    Args:
        card_number: カード番号

    Raises:
        ValidationError: バリデーション失敗時
    """
    # 半角数字のみ、16桁
    if not re.match(r'^\d{16}$', card_number):
        raise ValidationError(
            f'カード番号は16桁の半角数字で入力してください: {card_number}'
        )


def validate_amount(amount):
    """
    入金額のバリデーション

    Args:
        amount: 入金額

    Raises:
        ValidationError: バリデーション失敗時
    """
    # 半角数字のみ、最大7桁
    if not re.match(r'^\d{1,7}$', amount):
        raise ValidationError(
            f'入金額は7桁以内の半角数字で入力してください: {amount}'
        )

    # 数値チェック
    try:
        amt = int(amount)
        if amt < 0:
            raise ValidationError(f'入金額は0以上の数値を入力してください: {amount}')
    except ValueError:
        raise ValidationError(f'入金額が不正です: {amount}')


def validate_company_code(company_code):
    """
    カード発行会社コードのバリデーション

    Args:
        company_code: カード発行会社コード

    Raises:
        ValidationError: バリデーション失敗時
    """
    # 半角数字のみ、7桁（空白の場合はスキップ）
    if company_code and company_code.strip():
        if not re.match(r'^\d{7}$', company_code):
            raise ValidationError(
                f'カード発行会社コードは7桁の半角数字で入力してください: {company_code}'
            )


def validate_data_list(data_list):
    """
    データリスト全体のバリデーション

    Args:
        data_list: [(card_number, amount), ...] のリスト

    Returns:
        list: エラーメッセージのリスト（エラーがない場合は空）
    """
    errors = []

    if not data_list:
        errors.append('データが入力されていません')
        return errors

    if len(data_list) > 100000:
        errors.append(f'データ件数が多すぎます: {len(data_list)}件（最大100,000件）')
        return errors

    for i, (card_number, amount) in enumerate(data_list, start=1):
        try:
            validate_card_number(card_number)
        except ValidationError as e:
            errors.append(f'行{i}: {str(e)}')

        try:
            validate_amount(amount)
        except ValidationError as e:
            errors.append(f'行{i}: {str(e)}')

    return errors


def write_shift_jis_file(file_path, content):
    """
    Shift_JIS、CRLF改行でファイルを書き込み

    Args:
        file_path: 出力ファイルパス
        content: 書き込む内容（CRLFを含む）

    Raises:
        Exception: 書き込み失敗時
    """
    try:
        # newline='' でバイナリモードに近い書き込み（改行変換を抑制）
        with open(file_path, 'w', encoding='shift_jis', newline='') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f'ファイルの書き込みに失敗しました: {str(e)}')
