# PyHLSearch_Param

ビット演算を使って Hardy-Littlewood 探索を実行する Python スクリプトです。
素数ごとのシフト候補をビットマスクで表現し、候補集合の積集合を高速に探索します。

## 構成

- `HLSearch_Param.py`: コマンドライン引数、ログ初期化、探索の実行と結果ファイル出力
- `State.py`: ビットテーブル生成と、探索状態を保持して深さ優先探索を実行する `State` クラス
- `Config.py`: 既定の探索パラメータ、素数、シフト候補

## 必要環境

- Python 3.10 以上
- CPU 実行: 追加パッケージは不要
- CUDA 実行: CUDA 環境に対応する [CuPy](https://cupy.dev/)（例: `pip install cupy-cuda12x`）
- 進捗表示: [tqdm](https://tqdm.github.io/)（`pip install tqdm`）

CuPy と使用可能な CUDA デバイスを検出すると、`State` は自動的に CUDA を使って探索します。
CuPy が未インストールの場合、または CUDA デバイスを利用できない場合は、従来どおり CPU で実行します。

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
| `--include-paths` | 該当するシフト経路を保持して結果ファイルに出力 |
| `--no-progress` | tqdm による進捗表示を無効化 |
| `--log-level` | コンソール出力のログレベル |

`--primes-count` を指定する場合、`--depth` は指定件数以下にしてください。
既定では最大値の該当件数のみを集計し、シフト経路は保持・出力しません。経路も必要な場合は
`--include-paths` を指定してください。
進捗表示は既定で有効です。`Config.py` の `SHOW_PROGRESS` または `--no-progress` で無効化できます。

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
- `results_YYYYMMDD_HHMMSS.txt`: 最大残存候補数、実行時の探索設定、最大値を達成したシフト経路

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
- `State` クラスとビットテーブル生成処理を `State.py` に分離した
- ビットマスク生成、探索の枝刈り、引数処理を対象とした単体テストを追加した
- 実行方法、設定、出力、テスト手順を README に記載した
