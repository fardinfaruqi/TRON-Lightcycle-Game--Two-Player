import turtle
import time

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("TRON Lightcycle")
screen.tracer(0)        # disable auto-animation

# --- Player A ---
a = turtle.Turtle()
a.color("cyan")
a.pensize(3)
a.speed(0)
a.penup()
a.goto(-160, 0)
a.setheading(0)     # face right
a.pendown()         # start drawing trail

while True:
    a.forward(5)        # move 5 px every frame
    screen.update()     # manually refresh
    time.sleep(0.013)   # ~75 fps