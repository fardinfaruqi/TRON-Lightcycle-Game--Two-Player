"""Game constants and configuration."""

WIDTH = 800
HEIGHT = 600
STEP = 5  # pixels per frame
FRAME_DELAY = 0.013  # seconds per frame (~75 fps)
TRAIL_THICKNESS = 3
TRAIL_SAMPLE = 4  # record a position every N frames
COLLISION_RADIUS = 6  # pixel distance to count as a hit
GRACE_FRAMES = 30  # ignore self-collision at the very start
