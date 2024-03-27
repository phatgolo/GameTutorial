from typing import List
from pgzero.builtins import Actor
from random import randint
from pgzhelper import *

class AsteroidField:
    AMOUNT = 20

    def __init__(self, world_width: int, world_height: int):
        self.asteroids: List[Actor] = []
        self.world_width = world_width
        self.world_height = world_height
        for _ in range(self.AMOUNT):
            asteroid = Actor("asteroid")
            asteroid.radius = asteroid.width * 0.4
            asteroid.pos = randint(0, world_width), -randint(0, world_height)
            self.asteroids.append(asteroid)
    
    def check_collision(self, actor: Actor) -> bool:
        for asteroid in self.asteroids:
            if asteroid.circle_collidecircle(actor):
                return True

        return False

    def update(self, points: int) -> int:
        for asteroid in self.asteroids:
            asteroid.y += 2
        
            if asteroid.top > self.world_height:
                asteroid.pos = randint(0, self.world_width), 0
                points += 1
        
        return points

    def draw(self):
        for asteroid in self.asteroids:
            asteroid.draw()