"""ビット演算を用いる Hardy-Littlewood 探索の高速版。"""
import os
import sys
import datetime
import argparse
import logging
import logging.handlers
from typing import Optional, Sequence, Tuple

import Config as cfg
from State import State, build_bit_tables

logger = logging.getLogger("HLSearch_Param")


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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HLSearch Param: 素数シフト探索プログラム", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--depth", type=int, default=cfg.DEPTH, help="探索する階層数")
    parser.add_argument("--max-depth", type=int, default=cfg.MAX_DEPTH, help="最大深さ")
    parser.add_argument("-t", "--target", type=int, default=cfg.TARGET, help="depth == max-depth のときの目標値")
    parser.add_argument("-p", "--primes-count", type=int, default=None, metavar="N", help="PRIMES の先頭 N 個だけ使用")
    parser.add_argument("--cols", type=int, default=cfg.COLS, help="列数")
    parser.add_argument(
        "--include-paths",
        action="store_true",
        help="該当するシフト経路を保持して結果ファイルに出力",
    )
    parser.add_argument(
        "--no-progress",
        action="store_false",
        dest="show_progress",
        default=cfg.SHOW_PROGRESS,
        help="tqdm による進捗表示を無効化",
    )
    # parser.add_argument("--output", type=str, default=shift_path_file, help="結果出力先")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="コンソールログレベル")
    return parser.parse_args(argv)

def setup_logging(base_dir: str | os.PathLike[str], console_level: str = "INFO") -> str:
    log_path = cfg.LOG_FILE
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    formatter = logging.Formatter(cfg.LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, console_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=cfg.LOG_MAX_BYTES, backupCount=cfg.LOG_BACKUP_COUNT, encoding="utf-8")
    file_handler.setLevel(cfg.FILE_LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("ログファイルを作成しました: %s", log_path)
    return log_path


def main(
    argv: Sequence[str] | None = None,
    base_dir: str | os.PathLike[str] | None = None,
) -> State:
    """コマンドライン引数で探索を実行し、結果をファイルへ出力する。"""
    args = parse_args(argv)
    base = os.fspath(base_dir) if base_dir is not None else os.path.dirname(
        os.path.abspath(__file__)
    )
    LOG_PATH = setup_logging(base, args.log_level)

    logger.info("HLSearch_Param 開始 (log file: %s)", LOG_PATH)
    logger.info("設定: depth=%d max_depth=%d target=%d", args.depth, args.max_depth, args.target)

    primes, nums = select_search_data(cfg.PRIMES, cfg.NUMS, args.primes_count)
    state = State(
        primes,
        nums,
        args.depth,
        args.target,
        args.max_depth,
        args.cols,
        collect_paths=args.include_paths,
        show_progress=args.show_progress,
    )
    result_state = state.run()

    logger.info("最大値: %d", result_state.max_count)
    logger.info("該当件数: %d", result_state.results)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(base, f"results_{timestamp}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"max_count:{result_state.max_count}\n")
        f.write(f"results:{result_state.results}\n")
        f.write(f"depth:{args.depth}\n")
        f.write(f"target:{args.target}\n")
        f.write(f"max_depth:{args.max_depth}\n")
        f.write(f"primes_count:{len(primes)}\n")
        f.write(f"cols:{args.cols}\n")
        f.write(f"include_paths:{args.include_paths}\n")
        f.write(f"show_progress:{args.show_progress}\n")
        if args.include_paths:
            for shift in result_state.shifts:
                logger.info("シフト経路: %s", shift)
                f.write(f"{shift}\n")


    logger.info("HLSearch_Param 終了")
    return result_state


if __name__ == "__main__":
    main(sys.argv[1:])
