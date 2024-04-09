from typing import List
from pgzero.actor import Actor
from pgzhelper import *

class Explosion(Actor):
    def __init__(self, actor: Actor, images):
        super().__init__(images[0], (actor.x, actor.y))
        self.images = images
        self.fps = 10

    def animate_once(self) -> bool:
        frame = self.animate()
        done = frame == len(self.images) - 1
        return done

class PlayerExplosion(Explosion):
    def __init__(self, actor: Actor):
        super().__init__(actor, ["fire_explosion1", "fire_explosion2", "fire_explosion3", "fire_explosion4", "fire_explosion4"])

class AsteroidExplosion(Explosion):
    def __init__(self, actor: Actor):
        super().__init__(actor, ["gray_explosion1", "gray_explosion2", "gray_explosion3", "gray_explosion4", "gray_explosion4"])