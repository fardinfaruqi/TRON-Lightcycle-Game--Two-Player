import turtle
import time

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("TRON Lightcycle")
screen.tracer(0)        # disable auto-animation

while True:
    screen.update()     # manually refresh
    time.sleep(0.013)   # ~75 fps