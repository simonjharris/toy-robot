# Toy Robot Simulator

A simulation of a toy robot moving on a 5x5 square tabletop.

## Requirements

- Python 3.13
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (dev dependencies)

## Setup

No dependencies are required to run the application. For development tools (pytest, mypy, ruff):

```bash
uv sync
```

## Usage

Interactive mode:

```bash
python main.py
```

File mode:

```bash
python main.py -f commands.txt
```

### Commands

| Command               | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `PLACE X,Y,DIRECTION` | Place the robot at position X,Y facing NORTH, SOUTH, EAST or WEST |
| `MOVE`                | Move one unit forward in the current direction                    |
| `LEFT`                | Rotate 90 degrees left                                            |
| `RIGHT`               | Rotate 90 degrees right                                           |
| `REPORT`              | Output the current position and direction                         |
| `EXIT`                | Exit the simulator                                                |

## Testing

```bash
pytest
```

With coverage:

```bash
pytest --cov --cov-report=term
```