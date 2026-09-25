"""
A common interface that every simulation must adhere to.

`main.py` never needs to know the internal rules of a specific simulation
(Game of Life, forest fire, etc.)—it communicates solely through these methods.
This makes it possible to add new simulations without ever modifying the main engine.
"""

from abc import ABC, abstractmethod


class BaseSimulation(ABC):
    """Abstract base class for all simulations."""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    @abstractmethod
    def step(Self):
        """Move simulation one step."""
        raise NotImplementedError

    @abstractmethod
    def randomize(self):
        """Randomize grid."""
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        """Empty grid."""
        raise NotImplementedError

    @abstractmethod
    def toggle_cell(self, col, row):
        """React to mouse clicks."""
        raise NotImplementedError

    @abstractmethod
    def get_cells_to_draw(self):
        """Returns iterable (col, row, color)."""
        raise NotImplementedError

    def get_extra_controls(self):
        """Sliders/buttons for each simulations. Empty by default."""
        return []
