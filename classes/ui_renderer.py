"""UI renderer module - handles all UI rendering."""

import turtle


class UIRenderer:
    """Manages all UI rendering (HUD, splash screens, end screens)."""

    def __init__(self, screen: turtle.Screen, width: int, height: int):
        self.screen = screen
        self.width = width
        self.height = height
        self.writer = self._make_writer()
        self.hud_writer = self._make_writer()

    def _make_writer(self) -> turtle.Turtle:
        """Create a text-writing turtle."""
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.color("white")
        return t

    def draw_splash_screen(self):
        """Draw the initial splash screen."""
        self.writer.clear()
        self._write_center("T R O N", y=60, size=42)
        self._write_center("LIGHTCYCLE", y=10, size=18)
        self._write_center(
            "Player A: WASD       Player B: ARROWS", y=-50, size=12
        )
        self._write_center(
            "Press  ENTER  or  SPACE  to start", y=-100, size=14
        )
        self.screen.update()

    def draw_hud(self):
        """Draw the heads-up display showing player info."""
        self.hud_writer.clear()
        self.hud_writer.color("#00ffff")
        self.hud_writer.goto(-self.width // 2 + 15, self.height // 2 - 25)
        self.hud_writer.write(
            "WASD  ◀ Player A", font=("Courier", 11, "bold")
        )
        self.hud_writer.color("#ffff00")
        self.hud_writer.goto(self.width // 2 - 15, self.height // 2 - 25)
        self.hud_writer.write(
            "Player B ▶  ARROWS", align="right", font=("Courier", 11, "bold")
        )

    def draw_end_screen(self, winner: str):
        """Draw the end game screen."""
        self.writer.clear()
        if winner == "DRAW":
            self._write_center("D R A W !", y=40, size=36)
        else:
            self._write_center(f"{winner}", y=40, size=28)
            self._write_center("WINS!", y=0, size=36)
        self._write_center(
            "Press  ENTER  or  SPACE  to play again", y=-70, size=13
        )
        self.screen.update()

    def clear(self):
        """Clear all UI text."""
        self.writer.clear()

    def _write_center(self, msg: str, y: float = 0, size: int = 24):
        """Helper to write centered text."""
        self.writer.goto(0, y)
        self.writer.write(msg, align="center", font=("Courier", size, "bold"))
