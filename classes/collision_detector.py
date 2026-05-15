"""Collision detection module - handles all collision logic."""

from typing import List, Tuple
from classes.constants import COLLISION_RADIUS, TRAIL_SAMPLE, GRACE_FRAMES
from classes.arena import Arena
from classes.player import Player


class CollisionDetector:
    """Manages collision detection between players, trails, and walls."""

    def __init__(self, arena: Arena, collision_radius: float = COLLISION_RADIUS):
        self.arena = arena
        self.collision_radius = collision_radius

    def check_collision(
        self, player: Player, opponent_trail: List[Tuple[float, float]]
    ) -> bool:
        """Check if a player has collided with walls or trails."""
        px, py = player.get_position()

        # Check wall collision
        if not self.arena.is_within_bounds(px, py):
            return True

        # Check opponent trail collision
        if self._near(px, py, opponent_trail):
            return True

        # Check own trail collision (with grace period)
        own_trail = player.trail
        grace = max(0, len(own_trail) - GRACE_FRAMES // TRAIL_SAMPLE)
        safe_end = max(0, len(own_trail) - (GRACE_FRAMES // TRAIL_SAMPLE + 2))

        if self._near(px, py, own_trail[:safe_end]):
            return True

        return False

    def _near(
        self, px: float, py: float, trail: List[Tuple[float, float]]
    ) -> bool:
        """Check if a point is within collision radius of any trail point."""
        for tx, ty in trail:
            if (
                abs(px - tx) < self.collision_radius
                and abs(py - ty) < self.collision_radius
            ):
                return True
        return False
