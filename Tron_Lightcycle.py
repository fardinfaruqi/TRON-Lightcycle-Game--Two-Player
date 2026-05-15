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
screen.title("TRON Lightcycle")
screen.tracer(0)        # disable auto-animation   

XMIN, XMAX = -390, 390
YMIN, YMAX = -290, 290
HIT_DIST   = 6     # pixel radius for a "hit"
GRACE      = 10    # skip own last N trail points

# --- writer turtle for HUD ---
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color("white")

def show_text(msg, y=0, size=28):
    writer.goto(0, y)
    writer.write(msg, align="center", font=("Courier", size, "bold"))

def make_player(color, x, y, heading):
    t = turtle.Turtle()
    t.color(color)
    t.pensize(TRAIL_THICKNESS)
    t.speed(0)
    t.penup()
    t.goto(x, y)
    t.setheading(heading)
    t.pendown()
    return t

a = b = None

# Block 180° U-turns
def turn(player, h):
    if abs(player.heading() - h) != 180:
        player.setheading(h)

def start():
    global a, b, trail_a, trail_b, frame, running
    writer.clear()
    if a: a.clear(); a.hideturtle()
    if b: b.clear(); b.hideturtle()
    trail_a, trail_b = [], []
    frame = 0
    a = make_player("cyan",   -160, 0,   0)
    b = make_player("yellow",  160, 0, 180)
    running = True

screen.onkeypress(lambda: turn(a, 90),  "w")
screen.onkeypress(lambda: turn(a, 270), "s")
screen.onkeypress(lambda: turn(a, 180), "a")
screen.onkeypress(lambda: turn(a, 0),   "d")

screen.onkeypress(lambda: turn(b, 90),  "Up")
screen.onkeypress(lambda: turn(b, 270), "Down")
screen.onkeypress(lambda: turn(b, 180), "Left")
screen.onkeypress(lambda: turn(b, 0),   "Right")

screen.onkeypress(start, "Return")
screen.onkeypress(start, "space")

screen.listen()

trail_a, trail_b = [], []
frame = 0
running = False

show_text("TRON", y=30, size=42)
show_text("Press ENTER to start", y=-30, size=14)
screen.update()

def hits_trail(px, py, trail, skip_last=0):
    for tx, ty in trail[:len(trail)-skip_last]:
        if abs(px-tx) < HIT_DIST and abs(py-ty) < HIT_DIST:
            return True
    return False

def is_dead(t, own, opp):
    x, y = t.xcor(), t.ycor()
    if x < XMIN or x > XMAX or y < YMIN or y > YMAX:
        return True
    if hits_trail(x, y, opp):
        return True
    if hits_trail(x, y, own, skip_last=GRACE):
        return True
    return False

# running = True

while True:
    # a.forward(5)        # move 5 px every frame
    # b.forward(5)        # move 5 px every frame

    if running:
        a.forward(STEP)
        b.forward(STEP)
        frame += 1
        if frame % TRAIL_SAMPLE == 0:
            trail_a.append((a.xcor(), a.ycor()))
            trail_b.append((b.xcor(), b.ycor()))

        a_dead = is_dead(a, trail_a, trail_b)
        b_dead = is_dead(b, trail_b, trail_a)

        if a_dead or b_dead:
            running = False
            if a_dead: a.color("red")
            if b_dead: b.color("red")
            screen.update()
            if a_dead and b_dead:
                show_text("DRAW!", y=20, size=36)
            elif b_dead:
                show_text("CYAN WINS!", y=20, size=36)
            else:
                show_text("YELLOW WINS!", y=20, size=36)
            show_text("Press ENTER to play again", y=-40, size=13)

    screen.update()     # manually refresh
    time.sleep(FRAME_DELAY)

    