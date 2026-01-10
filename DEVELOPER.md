# 固定長テキスト変換ツール - 開発者ドキュメント

## プロジェクト概要

社内向けの固定長テキスト変換ツール（GUIアプリケーション）。
カード番号と入金額を入力するだけで、指定フォーマットのShift_JISテキストファイルを生成する。

## 技術スタック

- **Python**: 3.8以降
- **GUI**:
  - 標準版: tkinter（標準ライブラリ）
  - モダン版: CustomTkinter（追加パッケージ）
- **ビルド**: PyInstaller
- **文字コード**: Shift_JIS
- **改行コード**: CRLF

## バージョン

### 標準版（app.py）
- シンプルなtkinter UI
- 追加パッケージ不要
- 軽量（EXE: 約15-20MB）

### モダン版（app_modern.py）⭐推奨
- CustomTkinterによるモダンUI
- Material Design風デザイン
- ダークモード対応
- CustomTkinterパッケージが必要
- EXE: 約25-30MB

## ファイル構成

```
.
├── app.py                    # GUIアプリケーション本体（標準版）
├── app_modern.py             # GUIアプリケーション本体（モダン版）⭐
├── formatter.py              # 固定長整形ロジック
├── models.py                # レコード定義（フィールド長、固定値等）
├── utils.py                 # 入力パース、バリデーション、ファイル書き込み
├── test_formatter.py        # テストスクリプト
│
├── run_app.bat              # 標準版起動スクリプト（開発用）
├── run_modern.bat           # モダン版起動スクリプト（開発用）⭐
│
├── build_exe_en.bat         # 標準版ビルドスクリプト
├── build_modern.bat         # モダン版ビルドスクリプト⭐
├── build_exe.sh             # Linux/Macビルドスクリプト
│
├── test_simple.bat          # バッチファイル動作テスト
├── convert_to_sjis.sh       # 文字コード変換スクリプト
│
├── requirements.txt         # 依存パッケージ（標準版）
├── requirements_modern.txt  # 依存パッケージ（モダン版）
│
├── README.txt              # 利用者向けマニュアル
├── BUILD_GUIDE_EN.txt      # ビルド手順書（英語版）
├── QUICK_START.txt         # クイックスタートガイド⭐
├── DEVELOPER.md            # 開発者向けドキュメント（このファイル）
└── .gitignore              # Git除外設定
```

## 主要な設定

### カード発行会社コード
- **固定値**: `7130754`
- GUIから入力欄を削除し、コード内で固定値を使用
- 変更が必要な場合は `app.py:112` の値を変更してください

## 開発環境のセットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd file_change
```

### 2. 仮想環境の作成とアクティベート

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 開発

### アプリケーションの起動

**簡単な方法（推奨）:**

標準版:
```cmd
run_app.bat
```

モダン版（推奨）:
```cmd
run_modern.bat
```

**手動実行:**

標準版:
```bash
python app.py
```

モダン版:
```bash
# 初回のみ
pip install customtkinter

# 起動
python app_modern.py
```

### テストの実行

```bash
python test_formatter.py
```

生成されたテストファイル（`test_activate.txt`, `test_deposit.txt`）を確認して、
以下の点を検証：

- 各行が254文字であること
- 改行コードがCRLFであること
- 固定値（998, 2, A102）が正しい位置に入っていること

## ビルド

### 自動ビルド（推奨）

**標準版:**
```cmd
build_exe_en.bat
```
- 英語メッセージで確実に動作
- 生成ファイル: `dist/FixedLengthConverter.exe`
- サイズ: 約15-20MB

**モダン版（推奨）:**
```cmd
build_modern.bat
```
- CustomTkinterを含む
- 生成ファイル: `dist/FixedLengthConverter_Modern.exe`
- サイズ: 約25-30MB
- UIが綺麗で使いやすい

**Linux/Mac:**
```bash
./build_exe.sh
```

### 手動ビルド

**標準版:**
```bash
pyinstaller --onefile --noconsole --name FixedLengthConverter app.py
```

**モダン版:**
```bash
pip install customtkinter
pyinstaller --onefile --noconsole --name FixedLengthConverter_Modern app_modern.py
```

ビルド成果物は `dist/` ディレクトリに生成されます。

### ビルドのトラブルシューティング

**問題: ウィンドウが一瞬で閉じる**
- 解決策: `build_exe_simple.bat` を使用する

**問題: Pythonが見つからない**
- 解決策: PATHの設定を確認、コンピュータを再起動

**問題: 仮想環境の作成に失敗**
- 解決策: 管理者権限で実行、venvフォルダを削除して再実行

**問題: ビルドに失敗**
- 解決策: build、dist、venvフォルダを削除して再実行

## アーキテクチャ

### models.py - レコード定義

`Field` クラスで各フィールドの定義を管理：
- `length`: フィールド長（バイト数）
- `align`: 左寄せ（'left'）または右寄せ（'right'）
- `padding`: パディング文字（スペースまたはゼロ）
- `fixed_value`: 固定値（可変の場合はNone）

各レコードタイプ（ヘッダー、データ、トレーラー、エンド）のフィールド定義を配列で保持。

### formatter.py - 固定長整形

`FixedLengthFormatter` クラス：
- `create_header()`: ヘッダーレコード生成
- `create_data_record()`: データレコード生成
- `create_trailer()`: トレーラーレコード生成
- `create_end()`: エンドレコード生成
- `create_file_content()`: ファイル全体の生成

各メソッドは254文字のレコードを生成し、最後にCRLFを付加。

### utils.py - ユーティリティ

- `parse_input_text()`: テキストエリアの入力をパース（カンマ/タブ区切り対応）
- `validate_card_number()`: カード番号のバリデーション（16桁の半角数字）
- `validate_amount()`: 入金額のバリデーション（最大7桁の半角数字）
- `validate_company_code()`: カード発行会社コードのバリデーション（7桁の半角数字）
- `validate_data_list()`: データリスト全体のバリデーション
- `write_shift_jis_file()`: Shift_JIS、CRLF改行でファイル書き込み

### app.py - GUIアプリケーション

`FixedLengthConverterApp` クラス：
- tkinterを使用したGUI実装
- 2つのタブ（一括アクティベート、一括入金）
- テキストエリアで複数行入力対応
- サンプルデータ挿入機能
- ファイル保存ダイアログ

## レコードフォーマット仕様

### 共通ルール

- **レコード長**: 254文字 + CRLF（合計256バイト）
- **文字コード**: Shift_JIS
- **改行**: CRLF
- **パディング**: 未使用部分は半角スペース

### レコード構成

1. **ヘッダーレコード**（データ区分=1）
   - カード発行会社コード: 7桁
   - 取引区分: 4桁（アクティベート=0201、入金=0202）
   - 登録・結果区分: 1桁（固定'0'）
   - ダミー: 残りスペース

2. **データレコード**（データ区分=2）× N行
   - ファイル内連番: 6桁（000001〜、ゼロ埋め）
   - カード番号: 16桁
   - 入金額: 7桁（右詰めゼロ埋め）
   - 端末番号: 30桁（スペース）
   - 端末処理番号: 15桁（スペース）
   - 固定値: '998'（3桁）
   - 固定値: '2'（1桁）
   - 固定値: 'A102'（4桁）
   - ダミー: 残りスペース

3. **トレーラーレコード**（データ区分=8）
   - データ件数: 6桁（ゼロ埋め）
   - ダミー: 残りスペース

4. **エンドレコード**（データ区分=9）
   - ダミー: 全てスペース

## カスタマイズ

### フィールド定義の変更

`models.py` の各フィールド定義配列を編集：

```python
DATA_RECORD_FIELDS = [
    Field(1, fixed_value='2'),           # データ区分
    Field(6, align='right', padding='0'), # 連番
    # ... 以下省略
]
```

### 固定値の変更

`models.py` の `fixed_value` パラメータを変更：

```python
Field(3, fixed_value='998'),  # 固定値を変更する場合
```

### バリデーションルールの変更

`utils.py` の各バリデーション関数を編集：

```python
def validate_card_number(card_number):
    if not re.match(r'^\d{16}$', card_number):
        raise ValidationError('...')
```

## トラブルシューティング

### ビルド時の問題

**問題**: PyInstallerでビルドが失敗する

**解決策**:
- Python 3.8以降を使用しているか確認
- 仮想環境が正しくアクティベートされているか確認
- PyInstallerを再インストール: `pip install --upgrade pyinstaller`

### 文字コード関連

**問題**: 生成されたファイルが文字化けする

**解決策**:
- `write_shift_jis_file()` 関数で `newline=''` が指定されているか確認
- 改行コードが `\r\n` で明示的に付加されているか確認

**問題**: バッチファイル実行時に日本語が文字化けする

**原因**:
- Windowsのコマンドプロンプトは Shift_JIS (CP932) を使用
- Linux/Mac で作成したファイルは UTF-8 で保存される
- UTF-8のバッチファイルをWindowsで実行すると文字化けが発生

**解決策**:
- バッチファイルを Shift_JIS に変換する必要があります
- 変換スクリプトを実行してください：
  ```bash
  ./convert_to_sjis.sh
  ```
- または、手動で変換：
  ```bash
  iconv -f UTF-8 -t CP932 build_exe.bat > build_exe_sjis.bat
  mv build_exe_sjis.bat build_exe.bat
  ```

**重要な注意事項**:
- バッチファイル(.bat)を編集した後は、必ず Shift_JIS に変換してからコミットしてください
- Shift_JIS に変換されたファイルは、Linux/Mac のエディタで開くと文字化けして見える場合があります
- 変換後のファイルは `file -i ファイル名` で charset=unknown-8bit と表示されます（これは正常です）

### GUI関連

**問題**: tkinterが起動しない

**解決策**:
- Pythonインストール時にtkinterがインストールされているか確認
- Linux: `sudo apt-get install python3-tk`
- Mac: Homebrewでインストールした場合は `brew install python-tk`

## 配布

### 配布物

1. **EXEファイル**: `dist/固定長テキスト変換ツール.exe`
2. **マニュアル**: `README.txt`

### 配布方法

1. `dist/` ディレクトリから EXE ファイルを取得
2. `README.txt` をコピー
3. 配布先のフォルダに両方を配置
4. 利用者に `README.txt` を読むよう案内

### 注意事項

- Python不要（EXE単体で動作）
- インストール不要（フォルダに置いて実行）
- Windows 10以降を推奨
- セキュリティソフトによってはブロックされる可能性あり

## メンテナンス

### レコードフォーマットの変更

1. `models.py` のフィールド定義を更新
2. `test_formatter.py` でテスト実行
3. 生成されたファイルを手動確認
4. 問題なければビルド

### 新機能の追加

1. 必要に応じて `formatter.py` または `utils.py` を拡張
2. `app.py` にGUI要素を追加
3. テストを実行
4. ビルドと動作確認

## ライセンス

社内利用限定

## サポート

技術的な質問や問題報告は、開発チームにお問い合わせください。
