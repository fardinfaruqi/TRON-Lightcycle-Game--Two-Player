"""Game state module - manages game state tracking."""

from typing import Optional
from classes.constants import TRAIL_SAMPLE


class GameState:
    """Tracks the current state of the game."""

    def __init__(self):
        self.running = False
        self.game_over = False
        self.winner: Optional[str] = None
        self.frame = 0

    def reset(self):
        """Reset game state for a new round."""
        self.running = False
        self.game_over = False
        self.winner = None
        self.frame = 0

    def start(self):
        """Start the game."""
        self.reset()
        self.running = True

    def end_round(self, winner: str):
        """End the current round with a winner."""
        self.running = False
        self.game_over = True
        self.winner = winner

    def increment_frame(self):
        """Increment frame counter."""
        self.frame += 1

    def should_sample_trail(self) -> bool:
        """Check if trail should be sampled this frame."""
        return self.frame % TRAIL_SAMPLE == 0
