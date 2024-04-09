from pgzero.actor import Actor
from pgzhelper import *

class Explosion(Actor):
    def __init__(self, actor: Actor):
        super().__init__("gray_explosion1", (actor.x, actor.y))
        self.images = ["gray_explosion1", "gray_explosion2", "gray_explosion3", "gray_explosion4", "gray_explosion4"]
        self.fps = 10

    def animate_once(self) -> bool:
        frame = self.animate()
        done = frame == len(self.images) - 1
        return done

