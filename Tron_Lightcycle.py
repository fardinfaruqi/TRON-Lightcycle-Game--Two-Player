import turtle
import time

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("TRON Lightcycle")
screen.tracer(0)        # disable auto-animation   

def make_player(color, x, y, heading):
    t = turtle.Turtle()
    t.color(color);
    t.pensize(3);
    t.speed(0)
    t.penup();
    t.goto(x, y)
    t.setheading(heading); # face right
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

while True:
    a.forward(5)        # move 5 px every frame
    b.forward(5)        # move 5 px every frame
    screen.update()     # manually refresh
    time.sleep(0.013)   # ~75 fps