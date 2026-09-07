# Config.py
"""
HLSearch.py が使用する設定値をまとめた設定モジュール。

ロギング設定や探索パラメータ(LIMIT / TARGET / DEPTH など)を、
HLSearch.py 本体のロジックに触れずにここだけ編集すれば変更できるようにする。
"""

import logging
from pathlib import Path
from typing import List

# 後方互換性のためのデバッグ設定。詳細ログは FILE_LOG_LEVEL で制御する。
DEBUG: bool = False

# ============================================================
# ロギング設定
# ============================================================

# ログファイルの出力先ディレクトリ(このファイルと同じ場所)
LOG_DIR: Path = Path(__file__).resolve().parent

# ログファイル名は固定(HLSearch_Param.log)。サイズが上限を超えたら
# HLSearch_Param.log.1, HLSearch_Param.log.2, ... にローテーションする。
LOG_FILE: Path = LOG_DIR / "HLSearch_Param.log"

# 1ファイルあたりの最大サイズ(bytes)。超えたらローテーション。
LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB

# 保持する世代数(HLSearch.log.1 ~ HLSearch.log.<LOG_BACKUP_COUNT>)
LOG_BACKUP_COUNT: int = 100

# コンソール / ファイル それぞれの出力レベル
# ファイルには詳細なデバッグログを記録し、コンソールには重要なログのみ表示
CONSOLE_LOG_LEVEL: int = logging.INFO
FILE_LOG_LEVEL: int = logging.DEBUG

# ログのフォーマット
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(funcName)s: %(message)s"

# max_count を達成した shift_path を書き出すファイル(このファイルと同じ場所)。
SHIFT_PATH_FILE: Path = LOG_DIR / "shift_path.txt"


# ============================================================
# 探索パラメータ
# ============================================================

# 列数(元コードの range(1, 3160) に対応)
COLS: int = 3159

# この件数以上の zero_mask カウントが出ない枝は打ち切る
LIMIT: int = 400

# 目標値。max_count がちょうど TARGET のとき、それを超える更新を許可するかどうかの
# 判定に使う特別な閾値(_search() 内の分岐を参照)
TARGET: int = 447

# 探索する階層数(= 使用する素数の個数)。
DEPTH: int = 8
MAX_DEPTH: int = 249

# 進捗表示・実行制御設定
SHOW_PROGRESS: bool = True  # プログレスバー(tqdm)を表示するかどうか


# ============================================================
# 素数リスト
# ============================================================

# 2,3,5,7,11,13,...,1579 の素数リスト
PRIMES: List[int] = [
    2, 3, 5, 7, 11, 13, 17, 19,
    23, 29, 31, 37, 41, 43, 47, 53,
    59, 61, 67, 71, 73, 79, 83, 89,
    97, 101, 103, 107, 109, 113, 127, 131,
    137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
    229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479,
    487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619,
    631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769,
    773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929,
    937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061,
    1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193,
    1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307,
    1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459,
    1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579,
]

NUMS: list[list[int]] = [
    [1],    # 2
    [1],    # 3
    [4],    # 5
    [4],    # 7
    [i for i in range(11)],    # 11
    [i for i in range(13)],    # 13
    [i for i in range(17)],    # 17
    [i for i in range(19)],    # 19
    [i for i in range(23)],    # 23
    [i for i in range(29)],    # 29
    [i for i in range(31)],    # 31
    [i for i in range(37)],    # 37
    [i for i in range(41)],    # 41
    [i for i in range(43)],    # 43
    [i for i in range(47)],    # 47
    [i for i in range(53)],    # 53
    [i for i in range(59)],    # 59
    [i for i in range(61)],    # 61
    [i for i in range(67)],    # 67
    [i for i in range(71)],    # 71
    [i for i in range(73)],    # 73
    [i for i in range(79)],    # 79
    [i for i in range(83)],    # 83
    [i for i in range(89)],    # 89
    [i for i in range(97)],    # 97
    [i for i in range(101)],    # 101
    [i for i in range(103)],    # 103
    [i for i in range(107)],    # 107
    [i for i in range(109)],    # 109
    [i for i in range(113)],    # 113
    [i for i in range(127)],    # 127
    [i for i in range(131)],    # 131
    [i for i in range(137)],    # 137
    [i for i in range(139)],    # 139
    [i for i in range(149)],    # 149
    [i for i in range(151)],    # 151
    [i for i in range(157)],    # 157
    [i for i in range(163)],    # 163
    [i for i in range(167)],    # 167
    [i for i in range(173)],    # 173
    [i for i in range(179)],    # 179
    [i for i in range(181)],    # 181
    [i for i in range(191)],    # 191
    [i for i in range(193)],    # 193
    [i for i in range(197)],    # 197
    [i for i in range(199)],    # 199
    [i for i in range(211)],    # 211
    [i for i in range(223)],    # 223
    [i for i in range(227)],    # 227
    [i for i in range(229)],    # 229
    [i for i in range(233)],    # 233
    [i for i in range(239)],    # 239
    [i for i in range(241)],    # 241
    [i for i in range(251)],    # 251
    [i for i in range(257)],    # 257
    [i for i in range(263)],    # 263
    [i for i in range(269)],    # 269
    [i for i in range(271)],    # 271
    [i for i in range(277)],    # 277
    [i for i in range(281)],    # 281
    [i for i in range(283)],    # 283   
    [i for i in range(293)],    # 293
    [i for i in range(307)],    # 307
    [i for i in range(311)],    # 311
    [i for i in range(313)],    # 313
    [i for i in range(317)],    # 317
    [i for i in range(331)],    # 331
    [i for i in range(337)],    # 337
    [i for i in range(347)],    # 347
    [i for i in range(349)],    # 349
    [i for i in range(353)],    # 353
    [i for i in range(359)],    # 359
    [i for i in range(367)],    # 367
    [i for i in range(373)],    # 373
    [i for i in range(379)],    # 379
    [i for i in range(383)],    # 383
    [i for i in range(389)],    # 389
    [i for i in range(397)],    # 397
    [i for i in range(401)],    # 401
    [i for i in range(409)],    # 409
    [i for i in range(419)],    # 419
    [i for i in range(421)],    # 421
    [i for i in range(431)],    # 431
    [i for i in range(433)],    # 433
    [i for i in range(439)],    # 439
    [i for i in range(443)],    # 443
    [i for i in range(449)],    # 449
    [i for i in range(457)],    # 457
    [i for i in range(461)],    # 461
    [i for i in range(463)],    # 463
    [i for i in range(467)],    # 467
    [i for i in range(479)],    # 479
    [i for i in range(487)],    # 487
    [i for i in range(491)],    # 491
    [i for i in range(499)],    # 499
    [i for i in range(503)],    # 503
    [i for i in range(509)],    # 509
    [i for i in range(521)],    # 521
    [i for i in range(523)],    # 523
    [i for i in range(541)],    # 541
    [i for i in range(547)],    # 547
    [i for i in range(557)],    # 557
    [i for i in range(563)],    # 563
    [i for i in range(569)],    # 569
    [i for i in range(571)],    # 571
    [i for i in range(577)],    # 577
    [i for i in range(587)],    # 587
    [i for i in range(593)],    # 593
    [i for i in range(599)],    # 599
    [i for i in range(601)],    # 601
    [i for i in range(607)],    # 607
    [i for i in range(613)],    # 613
    [i for i in range(617)],    # 617
    [i for i in range(619)],    # 619
    [i for i in range(631)],    # 631
    [i for i in range(641)],    # 641
    [i for i in range(643)],    # 643
    [i for i in range(647)],    # 647
    [i for i in range(653)],    # 653
    [i for i in range(659)],    # 659
    [i for i in range(661)],    # 661
    [i for i in range(673)],    # 673
    [i for i in range(677)],    # 677
    [i for i in range(683)],    # 683
    [i for i in range(691)],    # 691
    [i for i in range(701)],    # 701
    [i for i in range(709)],    # 709
    [i for i in range(719)],    # 719
    [i for i in range(727)],    # 727
    [i for i in range(733)],    # 733
    [i for i in range(739)],    # 739
    [i for i in range(743)],    # 743
    [i for i in range(751)],    # 751
    [i for i in range(757)],    # 757
    [i for i in range(761)],    # 761
    [i for i in range(769)],    # 769
    [i for i in range(773)],    # 773
    [i for i in range(787)],    # 787
    [i for i in range(797)],    # 797
    [i for i in range(809)],    # 809
    [i for i in range(811)],    # 811
    [i for i in range(821)],    # 821
    [i for i in range(823)],    # 823
    [i for i in range(827)],    # 827
    [i for i in range(829)],    # 829
    [i for i in range(839)],    # 839
    [i for i in range(853)],    # 853
    [i for i in range(857)],    # 857
    [i for i in range(859)],    # 859
    [i for i in range(863)],    # 863
    [i for i in range(877)],    # 877
    [i for i in range(881)],    # 881
    [i for i in range(883)],    # 883
    [i for i in range(887)],    # 887
    [i for i in range(907)],    # 907
    [i for i in range(911)],    # 911
    [i for i in range(919)],    # 919
    [i for i in range(929)],    # 929
    [i for i in range(937)],    # 937
    [i for i in range(941)],    # 941
    [i for i in range(947)],    # 947
    [i for i in range(953)],    # 953
    [i for i in range(967)],    # 967
    [i for i in range(971)],    # 971
    [i for i in range(977)],    # 977
    [i for i in range(983)],    # 983
    [i for i in range(991)],    # 991
    [i for i in range(997)],    # 997
    [i for i in range(1009)],    # 1009
    [i for i in range(1013)],    # 1013
    [i for i in range(1019)],    # 1019
    [i for i in range(1021)],    # 1021
    [i for i in range(1031)],    # 1031
    [i for i in range(1033)],    # 1033
    [i for i in range(1039)],    # 1039
    [i for i in range(1049)],    # 1049
    [i for i in range(1051)],    # 1051
    [i for i in range(1061)],    # 1061
    [i for i in range(1063)],    # 1063
    [i for i in range(1069)],    # 1069
    [i for i in range(1087)],    # 1087
    [i for i in range(1091)],    # 1091
    [i for i in range(1093)],    # 1093
    [i for i in range(1097)],    # 1097
    [i for i in range(1103)],    # 1103
    [i for i in range(1109)],    # 1109
    [i for i in range(1117)],    # 1117
    [i for i in range(1123)],    # 1123
    [i for i in range(1129)],    # 1129
    [i for i in range(1151)],    # 1151
    [i for i in range(1153)],    # 1153
    [i for i in range(1163)],    # 1163
    [i for i in range(1171)],    # 1171
    [i for i in range(1181)],    # 1181
    [i for i in range(1187)],    # 1187
    [i for i in range(1193)],    # 1193
    [i for i in range(1201)],    # 1201
    [i for i in range(1213)],    # 1213
    [i for i in range(1217)],    # 1217
    [i for i in range(1223)],    # 1223
    [i for i in range(1229)],    # 1229
    [i for i in range(1231)],    # 1231
    [i for i in range(1237)],    # 1237
    [i for i in range(1249)],    # 1249
    [i for i in range(1259)],    # 1259
    [i for i in range(1277)],    # 1277
    [i for i in range(1279)],    # 1279
    [i for i in range(1283)],    # 1283
    [i for i in range(1289)],    # 1289
    [i for i in range(1291)],    # 1291
    [i for i in range(1297)],    # 1297
    [i for i in range(1301)],    # 1301
    [i for i in range(1303)],    # 1303
    [i for i in range(1307)],    # 1307
    [i for i in range(1319)],    # 1319
    [i for i in range(1321)],    # 1321
    [i for i in range(1327)],    # 1327
    [i for i in range(1361)],    # 1361
    [i for i in range(1367)],    # 1367
    [i for i in range(1373)],    # 1373
    [i for i in range(1381)],    # 1381
    [i for i in range(1399)],    # 1399
    [i for i in range(1409)],    # 1409
    [i for i in range(1423)],    # 1423
    [i for i in range(1427)],    # 1427
    [i for i in range(1429)],    # 1429
    [i for i in range(1433)],    # 1433
    [i for i in range(1439)],    # 1439
    [i for i in range(1447)],    # 1447
    [i for i in range(1451)],    # 1451
    [i for i in range(1453)],    # 1453
    [i for i in range(1459)],    # 1459
    [i for i in range(1471)],    # 1471
    [i for i in range(1481)],    # 1481
    [i for i in range(1483)],    # 1483
    [i for i in range(1487)],    # 1487
    [i for i in range(1489)],    # 1489
    [i for i in range(1493)],    # 1493
    [i for i in range(1499)],    # 1499
    [i for i in range(1511)],    # 1511
    [i for i in range(1523)],    # 1523
    [i for i in range(1531)],    # 1531
    [i for i in range(1543)],    # 1543
    [i for i in range(1549)],    # 1549
    [i for i in range(1553)],    # 1553
    [i for i in range(1559)],    # 1559
    [i for i in range(1567)],    # 1567
    [i for i in range(1571)],    # 1571
    [i for i in range(1579)],    # 1579
]
