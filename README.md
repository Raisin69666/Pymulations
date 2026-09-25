# Pymulations

Pymulations is a small Python simulation playground. It is **not meant to be a
professional, production-ready framework**. The point is to learn by making
things: experiment with simulation rules, poke at the UI, break something,
then figure out why it broke.

The first simulation is Conway's Game of Life, with a Pygame window, a simple
control panel, randomization, and a handful of classic `.cells` patterns. It is
also the only one... for now. :)

## Getting started

### 1. Clone the project

Clone the repository:

```bash
git clone https://github.com/Raisin69666/Pymulations
cd Pymulations
```

### 2. Create a virtual environment

Using a virtual environment keeps this experiment's packages separate from
the rest of your Python projects.

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
python -m pip install pygame pygame-gui
```

### 4. Run the application

From the project root, with the virtual environment activated:

```bash
python main.py
```

Close the window normally when you are done. The application loads its theme
from `theme.json`, so keep that file next to `main.py`.

## Playing with the simulation

- Click cells on the grid to turn them on or off.
- Use **Play/Pause** to start or stop the simulation.
- Use **Randomize** to create a new starting board.
- Use **Clear** to empty the board and pause it.
- Adjust the speed slider to change how often generations advance.
- Choose a pattern and press **Load** to try a built-in design.
- Press `Space` to play or pause, `C` to clear, and `R` to randomize.

## Project layout

```text
main.py                     # Starts Pygame and runs the main loop
simulations/                # Simulation rules and pattern loading
simulations/patterns/       # Built-in Game of Life patterns
ui/control_panel.py         # Reusable controls for the simulation window
theme.json                  # Pygame GUI styling
```

The UI sends simple actions back to `main.py`, while the simulation code owns
the rules and state. That separation is intentionally straightforward so it is
easy to follow while learning.

## Next ideas

Some possible directions for future experiments:

- Add more simulations, such as Langton's Ant, forest fires, falling sand, or reaction-diffusion patterns.
- Add click and drag capabilities to the UI/mouse.
- Make the grid resizable instead of using a fixed window size.
- Add step-forward and step-back controls.
- Save and load custom patterns.
- Add generation, population, and activity counters.
- Improve the pattern editor and add pattern previews.
- Add tests for simulation rules and pattern parsing.
- Turn the simulation picker into a real framework for swapping simulations.
