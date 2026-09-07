"""ビット演算を用いる Hardy-Littlewood 探索の高速版。"""
import os
import sys
import datetime
import argparse
import logging
import logging.handlers
import time
from typing import List, Optional, Sequence, Tuple

import Config as cfg

logger = logging.getLogger(__name__)


def build_bit_tables(primes: Sequence[int], cols: int) -> List[List[int]]:
    """
    各素数 p とそのシフト s (0 <= s < p) に対して、
    各列 idx (1 <= idx <= cols) で (idx - s) % p == 1 となるビットを 0、
    それ以外を 1 としたビットマスクを事前作成する。
    """
    tables: List[List[int]] = []
    for p in primes:
        p_shifts: List[int] = []
        for s in range(p):
            mask = 0
            for idx in range(1, cols + 1):
                if (idx - s) % p != 1:
                    mask |= 1 << (idx - 1)
            p_shifts.append(mask)
        tables.append(p_shifts)
    return tables


def select_search_data(
    primes: Sequence[int],
    nums: Sequence[Sequence[int]],
    primes_count: Optional[int],
) -> Tuple[Sequence[int], Sequence[Sequence[int]]]:
    """指定時は探索に使用する素数とシフト候補を同じ件数に制限する。"""
    if primes_count is None:
        return primes, nums
    if primes_count <= 0:
        raise ValueError(
            f"primes_count は正の整数である必要があります: {primes_count}"
        )
    return primes[:primes_count], nums[:primes_count]


class State:
    """探索に必要な設定値と実行状態を保持する。"""

    def __init__(
        self,
        primes: Sequence[int],
        nums: Optional[Sequence[Sequence[int]]],
        depth: int,
        limit: int,
        target: int,
        max_depth: int,
        cols: int,
    ) -> None:
        if depth <= 0:
            raise ValueError(f"depth は正の整数である必要があります: {depth}")
        if depth > len(primes):
            raise ValueError(
                f"depth={depth} が primes の要素数({len(primes)})を超えています"
            )
        if cols <= 0:
            raise ValueError(f"cols は正の整数である必要があります: {cols}")
        if limit < 0:
            raise ValueError(f"limit は0以上である必要があります: {limit}")

        self.primes = list(primes[:depth])
        self.nums = list(nums[:depth]) if nums is not None else None
        self.depth = depth
        self.limit = limit
        self.target = target
        self.max_depth = max_depth
        self.cols = cols

        self.bit_tables = build_bit_tables(self.primes, self.cols)
        self.max_count = 0
        self.results = 0
        self.nodes_searched = 0
        self.shift_path: List[int] = []
        self.shifts: List[List[int]] = []

    def run(self) -> "State":
        """すべてのシフト経路を探索し、結果をこの状態に格納して返す。"""
        start_time = time.time()
        initial_mask = (1 << self.cols) - 1

        # first_p = self.primes[0]
        first_p = self.nums[0]
        for s in reversed(first_p):
            self.shift_path.append(s)
            self._search(0, initial_mask & self.bit_tables[0][s])
            self.shift_path.pop()

        elapsed = time.time() - start_time
        logger.info(
            "探索完了: 所要時間=%.2f秒, 探索ノード数=%d (%.2f nodes/s)",
            elapsed,
            self.nodes_searched,
            self.nodes_searched / max(elapsed, 1e-6),
        )
        return self

    def _search(self, level: int, current_mask: int) -> None:
        self.nodes_searched += 1
        count = current_mask.bit_count()

        if count < self.limit or count < self.max_count:
            return

        if level + 1 >= self.depth:
            if self.depth == self.max_depth and count > self.target:
                return

            if count > self.max_count:
                self.max_count = count
                self.results = 1
                self.shifts = [list(self.shift_path)]
                logger.info("New max_count=%d (path=%s)", self.max_count, self.shift_path)
            elif count == self.max_count:
                self.results += 1
                self.shifts.append(list(self.shift_path))
            return

        next_level = level + 1
        # next_p = self.primes[next_level]
        next_p = self.nums[next_level]
        table_next = self.bit_tables[next_level]

        # for s in reversed(range(next_p)):
        for s in reversed(next_p):
            self.shift_path.append(s)
            self._search(next_level, current_mask & table_next[s])
            self.shift_path.pop()

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HLSearch fast2: 素数シフト探索プログラム", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--depth", type=int, default=cfg.DEPTH, help="探索する階層数")
    parser.add_argument("-l", "--limit", type=int, default=cfg.LIMIT, help="枝刈り下限")
    parser.add_argument("--max-depth", type=int, default=cfg.MAX_DEPTH, help="最大深さ")
    parser.add_argument("-t", "--target", type=int, default=cfg.TARGET, help="depth == max-depth のときの目標値")
    parser.add_argument("-p", "--primes-count", type=int, default=None, metavar="N", help="PRIMES の先頭 N 個だけ使用")
    parser.add_argument("--cols", type=int, default=cfg.COLS, help="列数")
    # parser.add_argument("--output", type=str, default=shift_path_file, help="結果出力先")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="コンソールログレベル")
    return parser.parse_args(argv)

def setup_logging(base_dir: str | os.PathLike[str], console_level: str = "INFO") -> str:
    log_path = os.path.join(base_dir, "HLSearch_Param.log")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, console_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("ログファイルを作成しました: %s", log_path)
    return log_path

if __name__ == "__main__":
    argv = sys.argv[1:] 
    args = parse_args(argv)
    base = os.path.dirname(os.path.abspath(__file__))
    LOG_PATH = setup_logging(base, args.log_level)

    logger.info("HLSearch_fast2 開始 (log file: %s)", LOG_PATH)
    logger.info("設定: depth=%d limit=%d max_depth=%d target=%d", args.depth, args.limit, args.max_depth, args.target)

    primes, nums = select_search_data(cfg.PRIMES, cfg.NUMS, args.primes_count)
    state = State(primes, nums, args.depth, args.limit, args.target, args.max_depth, args.cols)
    result_state = state.run()

    logger.info("最大値: %d", result_state.max_count)
    logger.info("該当件数: %d", result_state.results)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(base, f"shift_paths_{timestamp}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"max_count:{result_state.max_count}\n")
        f.write(f"results:{result_state.results}\n")
        for shift in result_state.shifts:
            logger.info("シフト経路: %s", shift)
            f.write(f"{shift}\n")


    logger.info("HLSearch_fast2 終了")
