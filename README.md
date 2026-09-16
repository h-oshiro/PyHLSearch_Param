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

通常の探索は CPU で実行します。CUDA を使う場合だけ `--use-cuda` を明示的に指定してください。
CuPy が未インストールの場合、または CUDA デバイスを利用できない場合に `--use-cuda` を指定すると、
エラーで停止します。
CUDA 実行時は、各 DFS ノードの次階層にある兄弟シフトを一括で積集合・件数集計し、GPU と CPU 間の
同期回数を抑えます。

## 実行方法

リポジトリのルートで実行します。

```powershell
python .\HLSearch_Param.py
```

小さな条件で動作を確認する例:

```powershell
python .\HLSearch_Param.py --depth 3 --cols 100
```

利用可能なオプションは次で確認できます。

```powershell
python .\HLSearch_Param.py --help
```

| オプション | 説明 |
| --- | --- |
| `-d`, `--depth` | 使用する素数とシフト候補の階層数 |
| `-t`, `--target` | `depth == max-depth` の場合に使用する目標値 |
| `--max-depth` | `target` の判定を有効にする深さ |
| `--cols` | ビットマスクで探索する列数 |
| `--include-paths` | 該当するシフト経路を保持して結果ファイルに出力 |
| `--no-progress` | tqdm による進捗表示を無効化 |
| `--use-cuda` | CUDA を明示的に使用する（利用できない場合はエラー） |
| `--log-level` | コンソール出力のログレベル |

既定では最大値の該当件数のみを集計し、シフト経路は保持・出力しません。経路も必要な場合は
`--include-paths` を指定してください。
進捗表示は既定で有効で、最上位シフトの完了状況を表示します。`Config.py` の `SHOW_PROGRESS` または
`--no-progress` で無効化できます。探索ノード数が 100,000 の倍数に達するごとに、現在の `depth` と
`max_count` も表示します。
固定の残存候補数による下限は設けず、探索中に見つかった最大値を下回る枝のみ打ち切ります。
最初の最大値を見つけた後は、各階層で次のシフトを適用した後の残存候補数が多い順に探索し、
枝刈りの効果を高めます。同数のシフトは従来どおりの順序で探索します。
`depth == max-depth` では、残存候補数が `target` を超える経路は破棄します。`target` と一致する
経路は `State.target_shifts` に保存し、`State.target_results` に件数を加算して、その経路の探索を
終了します。これらの目標一致経路は `--include-paths` の指定に関係なく `State` に保持されます。

## 設定

既定値と探索データは `Config.py` で管理します。

- `COLS`、`TARGET`、`DEPTH`、`MAX_DEPTH`: 探索の既定値
- `PRIMES`: 使用する素数の順序付きリスト
- `NUMS`: 各素数に対応する許可済みシフトのリスト

探索時は `NUMS[level]` の各値を、対応する素数のシフト用ビットテーブルの添字として
そのまま使用します。`depth` を増やす、または探索データを変更する場合は、対象範囲の
`NUMS` が存在し、すべてのシフトが `0 <= shift < PRIMES[level]` を満たすことを確認してください。
選択した `depth` の範囲に不整合がある場合は、探索開始前に
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

- `limit` による固定の枝刈り下限を廃止した
- CUDA の自動検出を廃止し、`--use-cuda` 指定時だけ CUDA を使用するようにした
- `State` クラスとビットテーブル生成処理を `State.py` に分離した
- ビットマスク生成、探索の枝刈り、引数処理を対象とした単体テストを追加した
- `max-depth` で `target` と一致した経路を `State` に記録するようにした
- 実行方法、設定、出力、テスト手順を README に記載した
