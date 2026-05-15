"""Arena module - manages game boundaries and borders."""

import turtle
from classes.constants import WIDTH, HEIGHT


class Arena:
    """Handles arena setup, border drawing, and boundary definitions."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.xmin = -width // 2 + 10
        self.xmax = width // 2 - 10
        self.ymin = -height // 2 + 10
        self.ymax = height // 2 - 10

    def draw_border(self):
        """Draw the arena border on the game screen."""
        b = turtle.Turtle()
        b.hideturtle()
        b.speed(0)
        b.penup()
        b.color("#333333")
        b.pensize(2)
        b.goto(-self.width // 2 + 5, -self.height // 2 + 5)
        b.pendown()
        for _ in range(2):
            b.forward(self.width - 10)
            b.left(90)
            b.forward(self.height - 10)
            b.left(90)
        b.penup()

    def is_within_bounds(self, x: float, y: float) -> bool:
        """Check if a position is within arena bounds."""
        return self.xmin < x < self.xmax and self.ymin < y < self.ymax
