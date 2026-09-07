# PyHLSearch_Param Copilot Instructions

## Commands

The project has no build system, linter, or formatter configured. Run the
standard-library unit-test suite from the repository root:

```powershell
python -m unittest discover -s .\tests -v
```

Run one test by its fully qualified name:

```powershell
python -m unittest tests.test_hlsearch_param.StateTests.test_run_records_all_paths_tied_for_the_best_count -v
```

Run the search program directly from the repository root:

```powershell
python .\HLSearch_Param.py
```

Use the CLI arguments to run a smaller, practical search while developing:

```powershell
python .\HLSearch_Param.py --depth 3 --limit 0 --cols 100 --max-depth 249
python .\HLSearch_Param.py --help
```

There are no individual tests to select. For a lightweight syntax check of the
two source modules, run:

```powershell
python -m py_compile .\HLSearch_Param.py .\Config.py
```

`do.bat` currently invokes the obsolete `HLSearch_nums.py`; invoke
`HLSearch_Param.py` directly unless that launcher is updated as part of the
change.

## Architecture

`HLSearch_Param.py` contains the command-line entry point and search engine.
`parse_args()` takes default values from `Config.py`; `main()` initializes
logging, constructs `State`, runs it, and writes matching shift paths to a
timestamped `shift_paths_YYYYMMDD_HHMMSS.txt` file next to the source.

`State` performs a depth-first search over allowed shift values. Before searching,
`build_bit_tables()` creates one integer bitmask for every allowed prime/shift
combination across `cols` candidate columns. `_search()` intersects those masks
with bitwise `&`, uses `int.bit_count()` as the surviving-candidate count, and
prunes paths below `limit` or the current `max_count`. At leaves it records every
path tied for the best count; when `depth == max_depth`, paths exceeding `target`
are discarded.

`Config.py` owns both runtime defaults and the data driving the search:

- `PRIMES` is the ordered prime sequence.
- `NUMS` supplies permitted shifts positionally for each searched prime.
- The early `NUMS` entries intentionally enumerate all residues, while later
  entries restrict the search to precomputed subsets.

## Repository-Specific Conventions

- `State` directly indexes `NUMS[level]` and then
  `bit_tables[level][shift]`. Before raising the usable depth or modifying the
  data, ensure the needed `NUMS` prefix exists and each shift is a valid
  `0 <= shift < PRIMES[index]` table index. The committed configuration does
  not meet those conditions for its entire declared `PRIMES` range, so retain
  the default shallow depth unless the relevant data is corrected.
- `State` validates `depth`, `cols`, `limit`, selected `NUMS` length, primes
  being integers of at least two, and every selected shift before building bit
  tables. Preserve these constraints when extending the command-line interface
  or configuration.
- `--primes-count` restricts both `PRIMES` and `NUMS` to their first N entries
  before constructing `State`; `--depth` must not exceed that selected count.
- Search artifacts are intentionally written in the repository directory:
  `HLSearch_Param.log` (with rotating backups) and timestamped shift-path files.
  These generated `.log` and `.txt` files are ignored by Git.
- Logging is initialized through `setup_logging()` with a DEBUG rotating file
  handler and a separately configurable console level. Use the module `logger`
  rather than creating unrelated loggers.
