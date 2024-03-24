from typing import List
from pgzero.builtins import Actor
from random import randint

class Asteroids:
    AMOUNT = 20

    def __init__(self, world_width: int, world_height: int):
        self.asteroids: List[Actor] = []
        self.world_width = world_width
        self.world_height = world_height
        for _ in range(0, self.AMOUNT):
            asteroid = Actor("asteroid1")
            asteroid.pos = randint(0, world_width), -randint(0, world_height)
            self.asteroids.append(asteroid)

    def update(self, score: int) -> int:
        for asteroid in self.asteroids:
            asteroid.top += 2
        
            if asteroid.top > self.world_height:
                asteroid.pos = randint(0, self.world_width), 0
                score += 1
        
        return score

    def collides(self, actor: Actor) -> bool:
        result = -1
        for i, asteriod in enumerate(self.asteroids):
            if asteriod.colliderect(actor):
                result = i
        
        if result > -1:
            self.asteroids.pop(result)
        
        return result >= 0

    def draw(self):
        for asteroid in self.asteroids:
            asteroid.draw()