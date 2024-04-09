from typing import List
from pgzero.builtins import Actor
from random import randint, random
from explosion import AsteroidExplosion
from pgzhelper import *

class Asteroid(Actor):
    def __init__(self, image: str):
        super().__init__(image)
        self.radius = self.width * 0.4
        self.rotation_speed = randint(-1, 1)
        self.movement_speed = random() + 1.5

    def update(self):
        self.angle += self.rotation_speed
        self.y += self.movement_speed

class AsteroidField:
    AMOUNT = 15

    def __init__(self, world_width: int, world_height: int):
        self.explosions: List[Exception] = []
        self.asteroids: List[Asteroid] = []
        self.world_width = world_width
        self.world_height = world_height
        for _ in range(self.AMOUNT):
            asteroid = Asteroid("asteroid" + str(randint(1, 6)))
            asteroid.pos = randint(0, world_width), -randint(0, world_height)
            self.asteroids.append(asteroid)
    
    def remove_asteroid(self, asteroid: Asteroid):
        self.explosions.append(AsteroidExplosion(asteroid))
        self.asteroids.remove(asteroid)

    def update(self, score: int) -> int:
        for explosion in self.explosions:
            if explosion.animate_once():
                self.explosions.remove(explosion)
        
        for asteroid in self.asteroids:
            asteroid.update()
        
            if asteroid.top > self.world_height:
                asteroid.pos = randint(0, self.world_width), 0
                score += 1
        
        return score

    def draw(self):
        for explosion in self.explosions:
            explosion.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
