import turtle
import time

### --- Constants --- ###
WIDTH, HEIGHT   = 800, 600
STEP            = 5           # pixels per frame
FRAME_DELAY     = 0.013       # seconds per frame (~75 fps)
TRAIL_THICKNESS = 3
TRAIL_SAMPLE    = 4           # record a position every N frames

### --- Screen Setup --- ###
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("TRON Lightcycle | WASD VS Arrow Keys")
screen.tracer(0)        # disable auto-animation   

### --- Helper: draw text with a pen turtle --- ###
def make_writer():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.color("white")
    return t

writer = make_writer()

def clear_writer():
    writer.clear()

def write_center(msg, y=0, size=24, font="Courier"):
    writer.goto(0, y)
    writer.write(msg, align="center", font=(font, size, "bold"))

### --- Arena border --- ###
def draw_border():
    b = turtle.Turtle()
    b.hideturtle()
    b.speed(0)
    b.penup()
    b.color("#333333")
    b.pensize(2)
    b.goto(-WIDTH//2 + 5, -HEIGHT//2 + 5)
    b.pendown()
    for _ in range(2):
        b.forward(WIDTH - 10)
        b.left(90)
        b.forward(HEIGHT - 10)
        b.left(90)
    b.penup()

draw_border()


### --- Arena limits (inner edge) --- ###
XMIN = -WIDTH  // 2 + 10
XMAX =  WIDTH  // 2 - 10
YMIN = -HEIGHT // 2 + 10
YMAX =  HEIGHT // 2 - 10

### --- Player factory --- ###
def make_player(color, start_x, start_y, start_heading):
    t = turtle.Turtle()
    t.hideturtle()
    t.shape("square")
    t.shapesize(0.4, 0.8)
    t.color(color)
    t.pensize(TRAIL_THICKNESS)
    t.speed(0)
    t.penup()
    t.goto(start_x, start_y)
    t.setheading(start_heading)
    t.pendown()
    t.showturtle()
    return t

### --- Game State --- ###
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.running   = False
        self.game_over = False
        self.winner    = None
        self.frame     = 0
        # trails: list of (x, y) sampled positions
        self.trail_a: list[tuple[float,float]] = []
        self.trail_b: list[tuple[float,float]] = []

state = GameState()

# Players are created once; we reposition them on reset
player_a = make_player("cyan",   -160,  0, 0)    # faces right
player_b = make_player("yellow",  160,  0, 180)  # faces left

def reset_players():
    for t, color, x, y, h, trails in (
        (player_a, "cyan", -160,  0,   0, state.trail_a),
        (player_b, "yellow", 160,  0, 180, state.trail_b),
    ):
        t.clear()          # erase drawn trail
        trails.clear()
        t.color(color)
        t.penup()
        t.goto(x, y)
        t.setheading(h)
        t.pendown()

### --- Direction queues (buffer one pending turn per player) --- ###
next_heading_a = None
next_heading_b = None

def is_reverse(current, new_heading):
    """Prevent a 180° U-turn."""
    return abs(current - new_heading) == 180

def set_a(h):
    global next_heading_a
    if not is_reverse(player_a.heading(), h):
        next_heading_a = h

def set_b(h):
    global next_heading_b
    if not is_reverse(player_b.heading(), h):
        next_heading_b = h

# Player A -> WASD
screen.onkeypress(lambda: set_a(90),  "w")
screen.onkeypress(lambda: set_a(270), "s")
screen.onkeypress(lambda: set_a(180), "a")
screen.onkeypress(lambda: set_a(0),   "d")

# Player B -> Arrow keys
screen.onkeypress(lambda: set_b(90),  "Up")
screen.onkeypress(lambda: set_b(270), "Down")
screen.onkeypress(lambda: set_b(180), "Left")
screen.onkeypress(lambda: set_b(0),   "Right")

# Start / Restart
def start_game():
    global next_heading_a, next_heading_b
    if state.game_over or not state.running:
        clear_writer()
        state.reset()
        reset_players()
        next_heading_a = None
        next_heading_b = None
        state.running = True

screen.onkeypress(start_game, "Return")
screen.onkeypress(start_game, "space")
screen.listen()

### --- Collision detection --- ###
COLLISION_RADIUS = 6   # pixel distance to count as a hit
GRACE_FRAMES     = 30  # ignore self-collision at the very start

def near(px, py, trail, start_idx=0):
    """Return True if (px,py) is within COLLISION_RADIUS of any trail point."""
    for tx, ty in trail[start_idx:]:
        if abs(px - tx) < COLLISION_RADIUS and abs(py - ty) < COLLISION_RADIUS:
            return True
    return False

def check_collision(t, own_trail, opp_trail):
    px, py = t.xcor(), t.ycor()
    # Wall
    if px <= XMIN or px >= XMAX or py <= YMIN or py >= YMAX:
        return True
    # Opponent trail
    if near(px, py, opp_trail):
        return True
    # Own trail — ignore the most-recent GRACE_FRAMES worth of points
    grace = max(0, len(own_trail) - GRACE_FRAMES // TRAIL_SAMPLE)
    if near(px, py, own_trail, start_idx=0) and not near(px, py, own_trail[grace:]):
        return True
    # Simpler: just skip the last few points for self-check
    safe_end = max(0, len(own_trail) - (GRACE_FRAMES // TRAIL_SAMPLE + 2))
    if near(px, py, own_trail[:safe_end]):
        return True
    return False

### --- HUD --- ###
hud = make_writer()

def draw_hud():
    hud.clear()
    hud.color("#00ffff")
    hud.goto(-WIDTH//2 + 15, HEIGHT//2 - 25)
    hud.write("WASD  ◀ Player A", font=("Courier", 11, "bold"))
    hud.color("#ffff00")
    hud.goto(WIDTH//2 - 15, HEIGHT//2 - 25)
    hud.write("Player B ▶  ARROWS", align="right", font=("Courier", 11, "bold"))

draw_hud()

### --- Splash screen --- ###
write_center("T R O N", y=60, size=42)
write_center("LIGHTCYCLE", y=10, size=18)
write_center("Player A: WASD       Player B: ARROWS", y=-50, size=12)
write_center("Press  ENTER  or  SPACE  to start", y=-100, size=14)

screen.update()

### --- Main loop --- ###
while True:
    screen.update()

    if not state.running:
        time.sleep(FRAME_DELAY)
        continue

    # Apply buffered heading changes
    if next_heading_a is not None:
        player_a.setheading(next_heading_a)
        next_heading_a = None
    if next_heading_b is not None:
        player_b.setheading(next_heading_b)
        next_heading_b = None

    # Move both players
    player_a.forward(STEP)
    player_b.forward(STEP)

    # Sample trail positions
    state.frame += 1
    if state.frame % TRAIL_SAMPLE == 0:
        state.trail_a.append((player_a.xcor(), player_a.ycor()))
        state.trail_b.append((player_b.xcor(), player_b.ycor()))

    # Collision checks
    a_dead = check_collision(player_a, state.trail_a, state.trail_b)
    b_dead = check_collision(player_b, state.trail_b, state.trail_a)

    if a_dead or b_dead:
        state.running   = False
        state.game_over = True

        if a_dead and b_dead:
            state.winner = "DRAW"
        elif a_dead:
            state.winner = "Player B  (YELLOW)"
        else:
            state.winner = "Player A  (CYAN)"

        # Flash the losing cycle(s)
        if a_dead:
            player_a.color("red")
        if b_dead:
            player_b.color("red")

        screen.update()

        clear_writer()
        if state.winner == "DRAW":
            write_center("D R A W !", y=40, size=36)
        else:
            write_center(f"{state.winner}", y=40, size=28)
            write_center("WINS!", y=0, size=36)
        write_center("Press  ENTER  or  SPACE  to play again", y=-70, size=13)
        screen.update()

    time.sleep(FRAME_DELAY)