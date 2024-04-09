from pgzero.actor import Actor
from pygame import Vector2

class Projectile(Actor):
    def __init__(self, image: str, xy: tuple[int, int], force: Vector2):
        super().__init__(image, xy, anchor=("center", "bottom"))
        self.force = force
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.mass = 1

    def update(self):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.acceleration = Vector2(0, 0)
