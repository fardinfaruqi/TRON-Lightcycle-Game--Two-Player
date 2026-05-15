"""Game module - main game controller."""

import turtle
import time
from classes.constants import WIDTH, HEIGHT, STEP, FRAME_DELAY
from classes.arena import Arena
from classes.player import Player
from classes.collision_detector import CollisionDetector
from classes.input_handler import InputHandler
from classes.ui_renderer import UIRenderer
from classes.game_state import GameState


class Game:
    """Main game controller that orchestrates all game components."""

    def __init__(self, width: int, height: int):
        # Initialize screen
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.bgcolor("black")
        self.screen.title("TRON Lightcycle | WASD VS Arrow Keys")
        self.screen.tracer(0)  # Disable auto-animation

        # Initialize game components
        self.arena = Arena(width, height)
        self.state = GameState()
        self.ui = UIRenderer(self.screen, width, height)
        self.input_handler = InputHandler(self.screen)
        self.collision_detector = CollisionDetector(self.arena)

        # Create players
        self.player_a = Player("Player A", "cyan", -160, 0, 0)  # faces right
        self.player_b = Player("Player B", "yellow", 160, 0, 180)  # faces left

        # Bind input
        self._setup_input()

        # Draw initial UI
        self.arena.draw_border()
        self.ui.draw_hud()
        self.ui.draw_splash_screen()

    def _setup_input(self):
        """Bind all keyboard input handlers."""
        self.input_handler.bind_player_a_keys(self.player_a)
        self.input_handler.bind_player_b_keys(self.player_b)
        self.input_handler.bind_game_control(self._on_game_start)

    def _on_game_start(self):
        """Handle game start/restart."""
        if self.state.game_over or not self.state.running:
            self.ui.clear()
            self.player_a.reset()
            self.player_b.reset()
            self.state.reset()
            self.state.start()

    def _update_players(self):
        """Update player positions and trails."""
        self.player_a.apply_pending_heading()
        self.player_b.apply_pending_heading()

        self.player_a.move(STEP)
        self.player_b.move(STEP)

        self.state.increment_frame()

        if self.state.should_sample_trail():
            self.player_a.record_trail_sample()
            self.player_b.record_trail_sample()

    def _check_collisions(self):
        """Check for collisions and determine winners."""
        a_dead = self.collision_detector.check_collision(
            self.player_a, self.player_b.trail
        )
        b_dead = self.collision_detector.check_collision(
            self.player_b, self.player_a.trail
        )

        if a_dead or b_dead:
            if a_dead:
                self.player_a.mark_dead()
            if b_dead:
                self.player_b.mark_dead()

            if a_dead and b_dead:
                winner = "DRAW"
            elif a_dead:
                winner = "Player B  (YELLOW)"
            else:
                winner = "Player A  (CYAN)"

            self.state.end_round(winner)

    def _render_end_screen(self):
        """Render the end game screen."""
        self.screen.update()
        self.ui.draw_end_screen(self.state.winner)

    def run(self):
        """Main game loop."""
        while True:
            self.screen.update()

            if not self.state.running:
                time.sleep(FRAME_DELAY)
                continue

            self._update_players()
            self._check_collisions()

            if self.state.game_over:
                self._render_end_screen()

            time.sleep(FRAME_DELAY)
