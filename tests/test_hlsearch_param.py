import unittest

from HLSearch_Param import State, build_bit_tables, parse_args, select_search_data


class BuildBitTablesTests(unittest.TestCase):
    def test_masks_exclude_the_expected_columns_for_each_shift(self) -> None:
        self.assertEqual(build_bit_tables([2], 4), [[0b1010, 0b0101]])


class SelectSearchDataTests(unittest.TestCase):
    def test_limits_primes_and_shift_lists_to_the_requested_count(self) -> None:
        primes, nums = select_search_data(
            primes=[2, 3, 5],
            nums=[[0, 1], [0, 1, 2], [0, 1, 2, 3, 4]],
            primes_count=2,
        )

        self.assertEqual(primes, [2, 3])
        self.assertEqual(nums, [[0, 1], [0, 1, 2]])

    def test_keeps_all_data_when_no_count_is_requested(self) -> None:
        primes = [2, 3]
        nums = [[0, 1], [0, 1, 2]]

        self.assertEqual(select_search_data(primes, nums, None), (primes, nums))

    def test_rejects_non_positive_count(self) -> None:
        with self.assertRaises(ValueError):
            select_search_data([2], [[0, 1]], 0)


class StateTests(unittest.TestCase):
    def test_rejects_invalid_constructor_arguments(self) -> None:
        with self.assertRaises(ValueError):
            State([2], [[0, 1]], 0, 0, 0, 1, 1)
        with self.assertRaises(ValueError):
            State([2], [[0, 1]], 2, 0, 0, 2, 1)
        with self.assertRaises(ValueError):
            State([2], [[0, 1]], 1, 0, 0, 1, 0)
        with self.assertRaises(ValueError):
            State([2], [[0, 1]], 1, -1, 0, 1, 1)

    def test_run_records_all_paths_tied_for_the_best_count(self) -> None:
        state = State(
            primes=[2, 3],
            nums=[[0, 1], [0, 1, 2]],
            depth=2,
            limit=0,
            target=99,
            max_depth=3,
            cols=6,
        ).run()

        self.assertEqual(state.max_count, 2)
        self.assertEqual(state.results, 6)
        self.assertEqual(
            state.shifts,
            [[1, 2], [1, 1], [1, 0], [0, 2], [0, 1], [0, 0]],
        )
        self.assertEqual(state.nodes_searched, 8)
        self.assertEqual(state.shift_path, [])

    def test_run_prunes_paths_below_the_limit(self) -> None:
        state = State(
            primes=[2, 3],
            nums=[[0, 1], [0, 1, 2]],
            depth=2,
            limit=4,
            target=99,
            max_depth=3,
            cols=6,
        ).run()

        self.assertEqual(state.max_count, 0)
        self.assertEqual(state.results, 0)
        self.assertEqual(state.nodes_searched, 2)

    def test_run_discards_counts_above_target_at_max_depth(self) -> None:
        state = State(
            primes=[2],
            nums=[[0, 1]],
            depth=1,
            limit=0,
            target=1,
            max_depth=1,
            cols=4,
        ).run()

        self.assertEqual(state.max_count, 0)
        self.assertEqual(state.results, 0)
        self.assertEqual(state.shifts, [])


class ParseArgsTests(unittest.TestCase):
    def test_parses_overridden_search_options(self) -> None:
        args = parse_args(
            [
                "--depth",
                "3",
                "--limit",
                "10",
                "--max-depth",
                "4",
                "--target",
                "5",
                "--primes-count",
                "6",
                "--cols",
                "100",
                "--log-level",
                "DEBUG",
            ]
        )

        self.assertEqual(args.depth, 3)
        self.assertEqual(args.limit, 10)
        self.assertEqual(args.max_depth, 4)
        self.assertEqual(args.target, 5)
        self.assertEqual(args.primes_count, 6)
        self.assertEqual(args.cols, 100)
        self.assertEqual(args.log_level, "DEBUG")
