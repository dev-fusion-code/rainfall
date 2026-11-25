# rainfall

Falling characters in the terminal, written in Python with curses.

## Requirements

- Python 3

On Windows, install `windows-curses` first:

    pip install windows-curses

## Usage

    python rainfall.py

Quit with `q` or `Esc`.

## Options

| Option | Description | Default |
| --- | --- | --- |
| `--text` | Characters or word used in the rain | a to z |
| `--color` | green, red, cyan, blue, yellow, magenta, white | green |
| `--speed` | Speed multiplier, must be above 0 | 1.0 |

Examples:

    python rainfall.py --color red --speed 2
    python rainfall.py --text SAKETH --color cyan --speed 0.5

## Settings

A few values can be changed at the top of `rainfall.py`:

- `SPEEDS`: base fall speeds
- `COLUMN_GAP`: spacing between columns
- `FRAME_DELAY`: delay between frames in seconds

## How it works

Each column has a drop with its own length and speed. Every frame, the drop moves down and its characters are drawn again with random picks from the character pool. The head is white, the next few characters are bright, and the tail is dim. When a drop leaves the screen, a new one starts at the top.