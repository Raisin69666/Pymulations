"""
Control panel containing all the options for the simulation, including buttons
and sliders (play/pause, random, clear, ...).

Key principle: this class knows NOTHING about the simulation. It
simply draws widgets and, when passed an event via `handle_event()`, returns
a simple action name (a string) if a button was clicked—or `None` otherwise.
It is `main.py` that decides how to handle that action
(calling `simulation.clear()`, etc.).

This keeps the class 100% reusable: it would work the same way regardless of the
simulation connected to it.
"""

import pygame
import pygame_gui


class ControlPanel:
    """Main control panel for the simulation, containing buttons and sliders."""
    PADDING = 10        # Margin inside widgets
    ROW_HEIGHT = 30     # Standard button height
    ROW_SPACING = 8     # Vertical space between widgets

    def __init__(
            self,
            manager,
            rect,
            pattern_names,
            simulation_name="Simulation",
            initial_speed=5.0
        ):

        self.manager = manager
        self.panel = pygame_gui.elements.UIPanel(relative_rect=rect, manager=manager)

        # Available width for widgets
        self.content_width = rect.width - 2 * self.PADDING
        self._next_y = self.PADDING     # Vertical cursor (stacking purposes)

        # Simulation title
        self.title_label = self._add_widget(
            pygame_gui.elements.UILabel,
            height=32,
            text=simulation_name,
            object_id="#simulation_title",
        )

        # Simulation title text effect
        self.title_label.set_active_effect(
            pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
            params={"time_per_letter": 0.04},
        )

        # Spacer between title and widgets
        self._add_spacer(20)

        self.update_freq = initial_speed

        # Simulation speed text
        self.speed_label = self._add_widget(
            pygame_gui.elements.UILabel,
            height=20,
            text=self._speed_text(),
        )

        # Simulation speed slider
        self.speed_slider = self._add_widget(
            pygame_gui.elements.UIHorizontalSlider,
            height=20,
            start_value=self.update_freq,
            value_range=(0.0, 10.0),        # Need to be floats,
            click_increment=0.1,            # else, Python defaults to int
        )

        # Play/Pause button
        self.play_button = self._add_widget(
            pygame_gui.elements.UIButton, height=self.ROW_HEIGHT, text="Play/Pause"
        )

        # Randomize button
        self.randomize_button = self._add_widget(
            pygame_gui.elements.UIButton, height=self.ROW_HEIGHT, text="Randomize"
        )

        # Clear grid button
        self.clear_button = self._add_widget(
            pygame_gui.elements.UIButton, height=self.ROW_HEIGHT, text="Clear"
        )

        # Spacer between simulation options and pattern selection options
        self._add_spacer(12)

        # Selected pattern text
        self.pattern_label = self._add_widget(
            pygame_gui.elements.UILabel, height=20, text="Load pattern :"
        )

        # Pattern dropdown menu
        self.pattern_dropdown = self._add_widget(
            pygame_gui.elements.UIDropDownMenu,
            height=self.ROW_HEIGHT,
            options_list=pattern_names or ["(none found)"],
            starting_option=(pattern_names or ["(none found)"])[0],
        )

        # Load pattern button
        self.load_pattern_button = self._add_widget(
            pygame_gui.elements.UIButton, height=self.ROW_HEIGHT, text="Load"
        )


    def _add_widget(self, widget_class, height, **kwargs):
        """
        Create a new widget below the last one and move vertical cursor.
        Removes the need to calculate (x, y) coords manually everytime.
        To add new button, simply call this method.
        """
        rect = pygame.Rect(self.PADDING, self._next_y, self.content_width, height)
        widget = widget_class(
            relative_rect=rect,
            manager=self.manager,
            container=self.panel,
            **kwargs
        )
        self._next_y += height + self.ROW_SPACING

        return widget


    def _add_spacer(self, height):
        """Move vertical spacer WITHOUT adding widget"""
        self._next_y += height


    def _speed_text(self):
        """Display current speed as text above the speed slider."""
        return f"Speed : {self.update_freq:.1f}"


    def set_playing_label(self, playing):
        """Updates Play/Pause button text."""
        self.play_button.set_text("Pause" if playing else "Playing")


    def handle_event(self, event):
        """
        Processes a pygame_gui event intended for this panel. Returns
        "toggle_play", "randomize", "clear", or the tuple("load_pattern", pattern_name)
        if a button or menu item was activated; otherwise, returns None.
        The slider updates its own state (update_freq and label) directly,
        without triggering an action.

        The selected pattern is read directly from `self.pattern_dropdown` when the
        "Load" button is clicked (rather than in response to a change event from the
        dropdown menu itself, which proved unreliable depending on the installed
        version of pygame_gui).
        """

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.update_freq = event.value
                self.speed_label.set_text(self._speed_text())
            return None

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                return "toggle_play"
            if event.ui_element == self.randomize_button:
                return "randomize"
            if event.ui_element == self.clear_button:
                return "clear"
            if event.ui_element == self.load_pattern_button:
                return ("load_pattern", self.pattern_dropdown.selected_option[0])

        return None
