"""
Main entry point for the simulation. Initializes the simulation, control panel,
and handles the main loop for user input and rendering. Simulation logic is
encapsulated in their respective classes (e.g., GameOfLife) which handle the rules
and state of the simulation. The main loop manages user interactions,
updates the simulation state, and renders the grid and UI elements on the screen.
"""

import pygame
import pygame_gui

from simulations import (
    GameOfLife,
    get_pattern_path,
    list_available_patterns,
    load_cells_file,
)
from ui import ControlPanel

# Colors - "Nord" themed
BACKGROUND = (46, 52, 64)  # 2E3440
GRID_LINE = (59, 66, 82)  # 3B4252

# Simulation dimension settings
TILE_SIZE = 10
SIM_WIDTH, SIM_HEIGHT = 1600, 900  # (1600 - 220) x 900
ROWS, COLS = SIM_HEIGHT // TILE_SIZE, SIM_WIDTH // TILE_SIZE

# Panel dimension setting
PANEL_WIDTH = 220

# Overall window dimension
WINDOW_WIDTH = PANEL_WIDTH + SIM_WIDTH
WINDOW_HEIGHT = SIM_HEIGHT

# Frame per second
FPS = 60

# Pygame/Pygame_Gui initialization
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), "theme.json")
clock = pygame.time.Clock()


def draw_grid(cells_to_draw):
    """Draws the grid and the cells on the screen."""
    for col, row, color in cells_to_draw:
        top_left = (PANEL_WIDTH + col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(ROWS + 1):  # +1 to include last row
        y = row * TILE_SIZE
        pygame.draw.line(
            screen, GRID_LINE, (PANEL_WIDTH, y), (PANEL_WIDTH + SIM_WIDTH, y)
        )

    for col in range(COLS + 1):  # +1 to include last right col
        x = PANEL_WIDTH + col * TILE_SIZE
        pygame.draw.line(screen, GRID_LINE, (x, 0), (x, SIM_HEIGHT))


def main():
    """Main loop for the simulation."""
    running = True
    playing = False
    count = 0

    # Simulation to load - Main entry point for which sim to load
    simulation = GameOfLife(rows=ROWS, cols=COLS)

    control_panel = ControlPanel(
        manager=ui_manager,
        rect=pygame.Rect(0, 0, PANEL_WIDTH, WINDOW_HEIGHT),
        simulation_name="Game of Life",
        pattern_names=list_available_patterns(),
        initial_speed=5.0,
    )

    control_panel.set_playing_label(playing)

    while running:
        time_delta = clock.tick(FPS) / 1000.0

        if playing:
            count += 0.1

        if count >= control_panel.update_freq:
            count = 0
            simulation.step()

        pygame.display.set_caption(
            f"Raisin's PyGame of Life - {'Playing' if playing else 'Paused'}"
        )

        # Centralize all inputs and decide which function to run accordingly
        action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # "mouse_x >= PANEL_WIDTH" exclude ALL panel, not only the widgets
                if not ui_manager.get_hovering_any_element() and mouse_x >= PANEL_WIDTH:
                    col = (mouse_x - PANEL_WIDTH) // TILE_SIZE
                    row = mouse_y // TILE_SIZE
                    simulation.toggle_cell(col, row)

            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Play/pause
                    action = "toggle_play"
                elif event.key == pygame.K_c:  # Clear grid and pause sim
                    action = "clear"
                elif event.key == pygame.K_r:  # Randomize grid
                    action = "randomize"

            # Panel handles is own slider
            # Returns action as a string if button click
            panel_action = control_panel.handle_event(event)
            if panel_action is not None:
                action = panel_action

            ui_manager.process_events(event)

        # Defining actions
        if action == "toggle_play":  # Play/Pause action
            playing = not playing
            control_panel.set_playing_label(playing)
        elif action == "clear":  # Clear action
            simulation.clear()
            playing = False
            count = 0
            control_panel.set_playing_label(playing)
        elif action == "randomize":  # Randomize action
            simulation.randomize()
        elif isinstance(action, tuple) and action[0] == "load_pattern":
            pattern_name = action[1]
            cells = load_cells_file(get_pattern_path(pattern_name))
            simulation.load_patterns(cells)
            playing = False
            count = 0
            control_panel.set_playing_label(playing)

        ui_manager.update(time_delta)

        screen.fill(BACKGROUND)
        draw_grid(simulation.get_cells_to_draw())
        ui_manager.draw_ui(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
