"""Input handler module - manages keyboard input."""

import turtle
from classes.player import Player


class InputHandler:
    """Handles keyboard input for both players and game control."""

    def __init__(self, screen: turtle.Screen):
        self.screen = screen
        self.game_start_callback = None

    def bind_player_a_keys(self, player: Player):
        """Bind WASD keys to Player A."""
        self.screen.onkeypress(lambda: player.set_heading(90), "w")  # up
        self.screen.onkeypress(lambda: player.set_heading(270), "s")  # down
        self.screen.onkeypress(lambda: player.set_heading(180), "a")  # left
        self.screen.onkeypress(lambda: player.set_heading(0), "d")  # right

    def bind_player_b_keys(self, player: Player):
        """Bind Arrow keys to Player B."""
        self.screen.onkeypress(lambda: player.set_heading(90), "Up")
        self.screen.onkeypress(lambda: player.set_heading(270), "Down")
        self.screen.onkeypress(lambda: player.set_heading(180), "Left")
        self.screen.onkeypress(lambda: player.set_heading(0), "Right")

    def bind_game_control(self, callback):
        """Bind game start/restart keys."""
        self.game_start_callback = callback
        self.screen.onkeypress(callback, "Return")
        self.screen.onkeypress(callback, "space")
        self.screen.listen()
