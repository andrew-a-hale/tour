# Knight's Tour Solver

A Python implementation of the Knight's Tour problem, a classic chess puzzle
where a knight must visit every square on a chessboard exactly once.

## Features

- Implements two algorithms for solving the Knight's Tour:
  - **DFS**: Depth-first search algorithm
  - **Warnsdorff**: Heuristic algorithm that chooses the next move with the fewest onward moves
- Configurable board dimensions
- Command-line interface

## Installation

```bash
uv sync
```

## Usage

Run with default 5x5 board:

```bash
uv run main.py
```

Specify custom board dimensions:

```bash
uv run main.py --width 8 --height 8
```

## How it Works

The program implements a `Game` class that:
1. Calculates valid knight moves from any position
2. Uses either DFS or Warnsdorff's algorithm to find a complete tour
3. Returns the sequence of coordinates visited by the knight

## TODO

-- [] SAT Solver
