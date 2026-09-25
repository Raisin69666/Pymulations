"""
Conway's Game of Life simulation.

This module provides :class:`GameOfLife`, a grid-based implementation of
Conway's cellular automaton. Each cell is either alive or dead, and each
simulation step updates the grid according to the standard Game of Life
rules: a live cell survives with two or three live neighbors, a dead cell is
born with exactly three live neighbors, and all other cells are dead in the
next generation.

The simulation stores its state in a NumPy array and uses padded neighbor
calculations so that cells at the grid boundaries behave as though they are
surrounded by dead cells. It also provides helpers for randomizing or
clearing the grid, toggling individual cells, loading patterns, and exposing
live cells with their display color for rendering by the surrounding
application.
"""

import numpy as np

from simulations.base import BaseSimulation

LIVE_CELL_COLOR = (136, 192, 208)   #88C0D0


class GameOfLife(BaseSimulation):
    """Implementation of the Game of Life simulation."""
    def __init__(self, rows, cols):
        super().__init__(rows, cols)

        # grid[row, col] == 1 -> alive, 0 -> dead
        self.grid = np.zeros((rows, cols), dtype=np.int8)

    def step(self):
        padded = np.pad(self.grid, pad_width=1, mode="constant", constant_values=0)

        neighbor_count = (
            padded[0:-2, 0:-2] + padded[0:-2, 1:-1] + padded[0:-2, 2:]
            + padded[1:-1, 0:-2]                    + padded[1:-1, 2:]
            + padded[2:, 0:-2]  + padded[2:, 1:-1]   + padded[2:, 2:]
        )

        born = (neighbor_count == 3) & (self.grid == 0)
        survives = ((neighbor_count == 2) | (neighbor_count == 3)) & (self.grid == 1)

        self.grid = (born | survives).astype(np.int8)


    def randomize(self, min_density=0.2, max_density=0.5):
        """Randomize grid with a random density between min_density and max_density."""
        density = np.random.uniform(min_density, max_density)
        self.grid = (np.random.random(self.grid.shape) < density).astype(np.int8)


    def clear(self):
        """Clear grid."""
        self.grid[:] = 0


    def toggle_cell(self, col, row):
        """React to mouse clicks."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row, col] = 0 if self.grid[row, col] else 1


    def get_cells_to_draw(self):
        """Returns iterable (col, row, color)."""
        rows_idx, cols_idx = np.nonzero(self.grid)
        return zip(cols_idx, rows_idx, [LIVE_CELL_COLOR] * len(rows_idx))


    def load_patterns(self, cells, top_left=None):
        """
        Clear grid and place given pattern. If top_left not passed,
        pattern will be centralized on grid.
        """

        self.clear()

        if not cells:
            return

        pattern_rows = max(r for r, _ in cells) + 1
        pattern_cols = max(c for _, c in cells) + 1

        if top_left is None:
            offset_row = (self.rows - pattern_rows) // 2
            offset_col = (self.cols - pattern_cols) // 2
        else:
            offset_row, offset_col = top_left

        for r, c in cells:
            row, col = r + offset_row, c + offset_col
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.grid[row, col] = 1
