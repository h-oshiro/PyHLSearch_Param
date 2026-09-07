"""Hardy-Littlewood 探索の状態管理とビットマスク探索ロジック。"""
import logging
import sys
import time
from types import ModuleType
from typing import List, Optional, Sequence

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


logger = logging.getLogger("HLSearch_Param")


def _load_cuda_module() -> Optional[ModuleType]:
    """利用可能な CUDA デバイスを持つ CuPy モジュールを返す。"""
    try:
        import cupy
    except ImportError:
        return None

    try:
        if cupy.cuda.runtime.getDeviceCount() == 0:
            return None
    except cupy.cuda.runtime.CUDARuntimeError:
        return None

    return cupy


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


def build_cuda_bit_tables(
    primes: Sequence[int], cols: int, cupy: ModuleType
) -> List[object]:
    """CUDA 上でシフトごとの候補列マスクを構築する。"""
    columns = cupy.arange(1, cols + 1, dtype=cupy.int64)
    return [
        (columns[None, :] - cupy.arange(prime, dtype=cupy.int64)[:, None]) % prime
        != 1
        for prime in primes
    ]


class State:
    """探索に必要な設定値と実行状態を保持する。"""

    def __init__(
        self,
        primes: Sequence[int],
        nums: Sequence[Sequence[int]],
        depth: int,
        limit: int,
        target: int,
        max_depth: int,
        cols: int,
        use_cuda: Optional[bool] = None,
        collect_paths: bool = False,
        show_progress: bool = True,
    ) -> None:
        if depth <= 0:
            raise ValueError(f"depth は正の整数である必要があります: {depth}")
        if depth > len(primes):
            raise ValueError(
                f"depth={depth} が primes の要素数({len(primes)})を超えています"
            )
        if depth > len(nums):
            raise ValueError(
                f"depth={depth} が nums の要素数({len(nums)})を超えています"
            )
        if cols <= 0:
            raise ValueError(f"cols は正の整数である必要があります: {cols}")
        if limit < 0:
            raise ValueError(f"limit は0以上である必要があります: {limit}")

        self.primes = list(primes[:depth])
        self.nums = [list(shifts) for shifts in nums[:depth]]
        for level, (prime, shifts) in enumerate(zip(self.primes, self.nums)):
            if not isinstance(prime, int) or prime <= 1:
                raise ValueError(
                    f"primes[{level}] は2以上の整数である必要があります: {prime!r}"
                )
            for shift in shifts:
                if not isinstance(shift, int) or not 0 <= shift < prime:
                    raise ValueError(
                        f"nums[{level}] のシフトは0以上{prime}未満の整数である必要があります: "
                        f"{shift!r}"
                    )

        self.depth = depth
        self.limit = limit
        self.target = target
        self.max_depth = max_depth
        self.cols = cols
        self.collect_paths = collect_paths
        self.show_progress = show_progress

        self._cupy = _load_cuda_module() if use_cuda is not False else None
        if use_cuda is True and self._cupy is None:
            raise RuntimeError("CUDA を利用できる CuPy 環境が必要です")
        self.uses_cuda = self._cupy is not None
        if self.uses_cuda:
            self.bit_tables = build_cuda_bit_tables(
                self.primes, self.cols, self._cupy
            )
            logger.info("CUDA を使用して探索します")
        else:
            self.bit_tables = build_bit_tables(self.primes, self.cols)
        self.max_count = 0
        self.results = 0
        self.nodes_searched = 0
        self.shift_path: List[int] = []
        self.shifts: List[List[int]] = []

    def run(self) -> "State":
        """すべてのシフト経路を探索し、結果をこの状態に格納して返す。"""
        start_time = time.time()
        initial_mask = (
            self._cupy.ones(self.cols, dtype=self._cupy.bool_)
            if self.uses_cuda
            else (1 << self.cols) - 1
        )

        shifts = reversed(self.nums[0])
        if self.show_progress:
            if tqdm is None:
                logger.warning(
                    "tqdm が未導入のため進捗表示を無効にします。"
                    "`pip install tqdm` で有効化できます。"
                )
            else:
                shifts = tqdm(
                    shifts,
                    total=len(self.nums[0]),
                    desc="探索中",
                    unit="shift",
                    disable=not sys.stderr.isatty(),
                )

        for shift in shifts:
            self.shift_path.append(shift)
            self._search(0, initial_mask & self.bit_tables[0][shift])
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
        count = (
            int(self._cupy.count_nonzero(current_mask).item())
            if self.uses_cuda
            else current_mask.bit_count()
        )

        if count < self.limit or count < self.max_count:
            return

        if level + 1 >= self.depth:
            if self.depth == self.max_depth and count > self.target:
                return

            if count > self.max_count:
                self.max_count = count
                self.results = 1
                self.shifts = [list(self.shift_path)] if self.collect_paths else []
                if self.collect_paths:
                    logger.info(
                        "New max_count=%d (path=%s)",
                        self.max_count,
                        self.shift_path,
                    )
                else:
                    logger.info("New max_count=%d", self.max_count)
            elif count == self.max_count:
                self.results += 1
                if self.collect_paths:
                    self.shifts.append(list(self.shift_path))
            return

        next_level = level + 1
        shifts = self.nums[next_level]
        table_next = self.bit_tables[next_level]
        for shift in reversed(shifts):
            self.shift_path.append(shift)
            self._search(next_level, current_mask & table_next[shift])
            self.shift_path.pop()
