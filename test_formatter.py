"""
固定長フォーマッターのテストスクリプト
"""

from formatter import FixedLengthFormatter
from utils import write_shift_jis_file


def test_activate():
    """一括アクティベートのテスト"""
    print('=== 一括アクティベート テスト ===')

    # テストデータ
    data_list = [
        ('7130123456789012', '10000'),
        ('7130123456789013', '20000'),
    ]

    # フォーマッター作成
    formatter = FixedLengthFormatter(
        format_type='activate',
        company_code='0000001'
    )

    # ファイル内容生成
    content = formatter.create_file_content(data_list)

    # 各行の長さをチェック
    lines = content.split('\r\n')
    print(f'総行数: {len(lines)}')
    print(f'データ件数: {len(data_list)}')

    for i, line in enumerate(lines):
        if line:  # 最後の空行以外
            print(f'行{i+1}: {len(line)}文字')
            if len(line) != 254:
                print(f'  警告: レコード長が不正です（期待値: 254文字）')

    # ファイル出力
    output_path = 'test_activate.txt'
    write_shift_jis_file(output_path, content)
    print(f'\nファイル出力: {output_path}')

    # 内容確認
    print('\n--- ファイル内容（最初の3行） ---')
    for i, line in enumerate(lines[:3]):
        print(f'{i+1}: [{line}]')


def test_deposit():
    """一括入金のテスト"""
    print('\n\n=== 一括入金 テスト ===')

    # テストデータ
    data_list = [
        ('7130123456789012', '10000'),
        ('7130123456789013', '20000'),
    ]

    # フォーマッター作成
    formatter = FixedLengthFormatter(
        format_type='deposit',
        company_code='0000001'
    )

    # ファイル内容生成
    content = formatter.create_file_content(data_list)

    # 各行の長さをチェック
    lines = content.split('\r\n')
    print(f'総行数: {len(lines)}')
    print(f'データ件数: {len(data_list)}')

    for i, line in enumerate(lines):
        if line:  # 最後の空行以外
            print(f'行{i+1}: {len(line)}文字')
            if len(line) != 254:
                print(f'  警告: レコード長が不正です（期待値: 254文字）')

    # ファイル出力
    output_path = 'test_deposit.txt'
    write_shift_jis_file(output_path, content)
    print(f'\nファイル出力: {output_path}')

    # 内容確認
    print('\n--- ファイル内容（最初の3行） ---')
    for i, line in enumerate(lines[:3]):
        print(f'{i+1}: [{line}]')

    # データレコードの詳細確認
    print('\n--- データレコード詳細（2行目） ---')
    if len(lines) > 1:
        data_record = lines[1]
        print(f'データ区分（1桁）: [{data_record[0]}]')
        print(f'連番（6桁）: [{data_record[1:7]}]')
        print(f'カード番号（16桁）: [{data_record[7:23]}]')
        print(f'入金額（7桁）: [{data_record[23:30]}]')
        print(f'端末番号（30桁）: [{data_record[30:60]}]')
        print(f'端末処理番号（15桁）: [{data_record[60:75]}]')
        print(f'固定値998（3桁）: [{data_record[75:78]}]')
        print(f'固定値2（1桁）: [{data_record[78:79]}]')
        print(f'固定値A102（4桁）: [{data_record[79:83]}]')
        print(f'ダミー（残り）: [{data_record[83:]}]')


if __name__ == '__main__':
    test_activate()
    test_deposit()
