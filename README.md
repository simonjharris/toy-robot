# Toy Robot Simulator

A simulation of a toy robot moving on a 5x5 square tabletop.

## Requirements

- Python 3.13
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (dev dependencies)

## Development Setup

For running tests, type checking, and linting:

```bash
uv sync
```

### Testing

```bash
pytest
```

With coverage:

```bash
pytest --cov --cov-report=term
```

### Type Checking and Linting

```bash
uv run mypy .
uv run ruff check .
```

## Usage

The tool uses only the standard library, so there's no need for a virtual environment.

Interactive mode:

```bash
python -m toy_robot
```

File mode:

```bash
python -m toy_robot -f commands.txt
```

### Commands

| Command               | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `PLACE X,Y,DIRECTION` | Place the robot at position X,Y facing NORTH, SOUTH, EAST or WEST |
| `MOVE`                | Move one unit forward in the current direction                    |
| `LEFT`                | Rotate 90 degrees left                                            |
| `RIGHT`               | Rotate 90 degrees right                                           |
| `REPORT`              | Output the current position and direction                         |

### Example

```
PLACE 1,2,EAST
MOVE
MOVE
LEFT
MOVE
REPORT
```

Output: `3,3,NORTH`

