"""
Loading Game of Life patterns in "plaintext" (.cells) format — the
standard format used by conwaylife.com/patterns (LifeWiki), the
largest catalog of known patterns (gliders, guns, oscillators...).

To add a new pattern: download its .cells file from
https://conwaylife.com/patterns and place it "./patterns". It
will automatically appear in the list (see list_available_patterns).

Format (see https://conwaylife.com/wiki/Plaintext):
- Lines starting with "!" are comments (ignored).
- "." = dead cell, "O" (letter, not zero) = live cell.
- Trailing spaces/dots can be omitted.
"""

from pathlib import Path

PATTERNS_DIR = Path(__file__).parent / "patterns"


def load_cells_file(path):
    """
    Read a .cells file and returns all live cells as a tuple (row, col).
    Relative to top left corner ( * >= 0)
    """

    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if not line.startswith("!")]

    return [
        (row, col)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        # Letter "O" (not zero)
        if char == "O"
    ]


def list_available_patterns():
    """
    Returns visible names of all pattern files found in .patterns
    """

    if not PATTERNS_DIR.exists():
        return []
    stems = sorted(p.stem for p in PATTERNS_DIR.glob("*.cells"))
    return [stem.replace("_", " ").title() for stem in stems]


def get_pattern_path(display_name):
    """
    Converts shown name into file path.
    """
    
    stem = display_name.lower().replace(" ", "_")
    return PATTERNS_DIR / f"{stem}.cells"
