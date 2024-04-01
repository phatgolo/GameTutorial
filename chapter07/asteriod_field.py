from typing import List
from pgzero.builtins import Actor
from random import randint, random
from pgzhelper import *

class AsteroidField:
    AMOUNT = 15

    def __init__(self, world_width: int, world_height: int):
        self.asteroids: List[Asteroid] = []
        self.world_width = world_width
        self.world_height = world_height
        for _ in range(self.AMOUNT):
            asteroid = Asteroid("asteroid" + str(randint(1, 6)))
            asteroid.pos = randint(0, world_width), -randint(0, world_height)
            self.asteroids.append(asteroid)
    
    def check_collision(self, actor: Actor) -> bool:
        for asteroid in self.asteroids:
            if asteroid.circle_collidecircle(actor):
                return True

        return False

    def update(self, points: int) -> int:
        for asteroid in self.asteroids:
            asteroid.update()
        
            if asteroid.top > self.world_height:
                asteroid.pos = randint(0, self.world_width), 0
                points += 1
        
        return points

    def draw(self):
        for asteroid in self.asteroids:
            asteroid.draw()

class Asteroid(Actor):
    def __init__(self, image: str):
        super().__init__(image)
        self.radius = self.width * 0.4
        self.rotation_speed = randint(-1, 1)
        self.movement_speed = random() + 1.5

    def update(self):
        self.angle += self.rotation_speed
        self.y += self.movement_speed
