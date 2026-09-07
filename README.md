# PyHLSearch_Param

ビット演算を使って Hardy-Littlewood 探索を実行する Python スクリプトです。
素数ごとのシフト候補をビットマスクで表現し、候補集合の積集合を高速に探索します。

## 必要環境

- Python 3.10 以上
- 追加パッケージは不要

## 実行方法

リポジトリのルートで実行します。

```powershell
python .\HLSearch_Param.py
```

小さな条件で動作を確認する例:

```powershell
python .\HLSearch_Param.py --depth 3 --limit 0 --cols 100
```

利用可能なオプションは次で確認できます。

```powershell
python .\HLSearch_Param.py --help
```

| オプション | 説明 |
| --- | --- |
| `-d`, `--depth` | 使用する素数とシフト候補の階層数 |
| `-l`, `--limit` | この残存候補数を下回る枝を打ち切る下限 |
| `-t`, `--target` | `depth == max-depth` の場合に使用する上限値 |
| `--max-depth` | `target` の判定を有効にする深さ |
| `-p`, `--primes-count` | `PRIMES` と対応する `NUMS` の先頭 N 件だけを使用 |
| `--cols` | ビットマスクで探索する列数 |
| `--log-level` | コンソール出力のログレベル |

`--primes-count` を指定する場合、`--depth` は指定件数以下にしてください。

## 設定

既定値と探索データは `Config.py` で管理します。

- `COLS`、`LIMIT`、`TARGET`、`DEPTH`、`MAX_DEPTH`: 探索の既定値
- `PRIMES`: 使用する素数の順序付きリスト
- `NUMS`: 各素数に対応する許可済みシフトのリスト

探索時は `NUMS[level]` の各値を、対応する素数のシフト用ビットテーブルの添字として
そのまま使用します。`depth` を増やす、または探索データを変更する場合は、対象範囲の
`NUMS` が存在し、すべてのシフトが `0 <= shift < PRIMES[level]` を満たすことを確認してください。
現在の設定データは全 `PRIMES` 範囲ではこの条件を満たしていないため、深い探索を行う前に
該当するデータを修正してください。選択した `depth` の範囲に不整合がある場合は、探索開始前に
`ValueError` で停止します。

## 出力

実行するとリポジトリのルートに次のファイルを作成します。

- `HLSearch_Param.log`: ローテーションされる実行ログ
- `shift_paths_YYYYMMDD_HHMMSS.txt`: 最大残存候補数と、その値を達成したシフト経路

これらの生成ファイルは Git の管理対象外です。

## テスト

標準ライブラリの `unittest` を使用します。

```powershell
python -m unittest discover -s .\tests -v
```

個別テストは完全修飾名で実行できます。

```powershell
python -m unittest tests.test_hlsearch_param.StateTests.test_run_records_all_paths_tied_for_the_best_count -v
```

## 更新履歴

### 開発中

- `--primes-count` で `PRIMES` と対応する `NUMS` の先頭 N 件を探索対象として選択できるようにした
- ビットマスク生成、探索の枝刈り、引数処理を対象とした単体テストを追加した
- 実行方法、設定、出力、テスト手順を README に記載した
