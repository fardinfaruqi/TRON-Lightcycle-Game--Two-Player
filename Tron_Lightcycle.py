import turtle
import time

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("TRON Lightcycle")
screen.tracer(0)        # disable auto-animation   

XMIN, XMAX = -390, 390
YMIN, YMAX = -290, 290
HIT_DIST   = 6     # pixel radius for a "hit"
GRACE      = 10    # skip own last N trail points

def make_player(color, x, y, heading):
    t = turtle.Turtle()
    t.color(color)
    t.pensize(3)
    t.speed(0)
    t.penup()
    t.goto(x, y)
    t.setheading(heading) # face right
    t.pendown()            # start drawing trail
    return t

a = make_player("cyan",   -160, 0,   0) # Player A starts on the Left, facing right
b = make_player("yellow",  160, 0, 180) # Player B starts on the Right, facing Left

# Block 180° U-turns
def turn(player, h):
    if abs(player.heading() - h) != 180:
        player.setheading(h)

screen.onkeypress(lambda: turn(a, 90),  "w")
screen.onkeypress(lambda: turn(a, 270), "s")
screen.onkeypress(lambda: turn(a, 180), "a")
screen.onkeypress(lambda: turn(a, 0),   "d")

screen.onkeypress(lambda: turn(b, 90),  "Up")
screen.onkeypress(lambda: turn(b, 270), "Down")
screen.onkeypress(lambda: turn(b, 180), "Left")
screen.onkeypress(lambda: turn(b, 0),   "Right")

screen.listen()

trail_a, trail_b = [], []
frame = 0
SAMPLE = 4   # record a point every 4 frames

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

running = True

while True:
    # a.forward(5)        # move 5 px every frame
    # b.forward(5)        # move 5 px every frame

    if running:
        a.forward(5); b.forward(5)
        frame += 1
        if frame % SAMPLE == 0:
            trail_a.append((a.xcor(), a.ycor()))
            trail_b.append((b.xcor(), b.ycor()))

        if is_dead(a, trail_a, trail_b) or is_dead(b, trail_b, trail_a):
            running = False
            print("GAME OVER")   # replace with HUD in step 6

    screen.update()     # manually refresh
    time.sleep(0.013)   # ~75 fps