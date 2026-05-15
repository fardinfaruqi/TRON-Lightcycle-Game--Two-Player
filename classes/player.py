"""Player module - represents a player's cycle."""

import turtle
from typing import List, Tuple, Optional
from classes.constants import TRAIL_THICKNESS


class Player:
    """Manages a player's turtle, position, heading, and trail."""

    def __init__(
        self,
        name: str,
        color: str,
        start_x: float,
        start_y: float,
        start_heading: float,
    ):
        self.name = name
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.start_heading = start_heading
        self.trail: List[Tuple[float, float]] = []
        self.next_heading: Optional[float] = None
        self._create_turtle()

    def _create_turtle(self):
        """Create and configure the player's turtle."""
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.shape("square")
        self.turtle.shapesize(0.4, 0.8)
        self.turtle.pensize(TRAIL_THICKNESS)
        self.turtle.speed(0)
        self.reset()

    def reset(self):
        """Reset the player to starting position and clear trail."""
        self.turtle.clear()
        self.trail.clear()
        self.turtle.color(self.color)
        self.turtle.penup()
        self.turtle.goto(self.start_x, self.start_y)
        self.turtle.setheading(self.start_heading)
        self.turtle.pendown()
        self.turtle.showturtle()
        self.next_heading = None

    def move(self, distance: float):
        """Move the player forward by the specified distance."""
        self.turtle.forward(distance)

    def set_heading(self, heading: float):
        """Queue a heading change (prevents 180° turns)."""
        if not self._is_reverse(self.turtle.heading(), heading):
            self.next_heading = heading

    def apply_pending_heading(self):
        """Apply any pending heading change."""
        if self.next_heading is not None:
            self.turtle.setheading(self.next_heading)
            self.next_heading = None

    def record_trail_sample(self):
        """Record current position to trail."""
        self.trail.append((self.turtle.xcor(), self.turtle.ycor()))

    def get_position(self) -> Tuple[float, float]:
        """Get player's current position."""
        return (self.turtle.xcor(), self.turtle.ycor())

    def mark_dead(self):
        """Change player color to red when dead."""
        self.turtle.color("red")

    @staticmethod
    def _is_reverse(current: float, new_heading: float) -> bool:
        """Check if the new heading is a 180° turn from current."""
        return abs(current - new_heading) == 180
