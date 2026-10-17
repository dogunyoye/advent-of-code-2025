# Advent of Code 2025

Python solutions for [Advent of Code 2025](https://adventofcode.com/2025).

## Requirements

- Python 3.10+
- Third-party packages for a few days (see `requirements.txt`):

```bash
pip install -r requirements.txt
```

Days 01-07, 11 and 12 use only the standard library.

## Layout

```
aoc_utils/          Shared helpers (aoc_helper.py, timer.py)
dayNN/              One folder per day
    dayNN.py        Solution (parses input in main(), prints part 1 and 2)
    dayNN.txt       Puzzle input (git-ignored)
```

## Usage

Run a solution from the repository root so package imports resolve:

```bash
python -m day01.day01
```

Some days define extra exploratory entry points (for example, `day09.py` also
prints an alternate part 2 implementation).

## Creating a new day

`aoc_utils/aoc_helper.py` scaffolds the folder, solution file and empty input:

```bash
python aoc_utils/aoc_helper.py day13
```
