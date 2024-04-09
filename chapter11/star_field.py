from random import random
from pgzero.screen import Screen

class StarField:
    AMOUNT = 1000

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.stars = []
        for _ in range(self.AMOUNT):
            x = random() * window_width
            y = random() * window_height
            r = random()
            z = r ** 4
            self.stars.append((x, y, z))

        self.stars.sort(key=lambda star: star[2])

    def draw(self, screen: Screen, speed = 0.5):
        stars = []
        for (x, y, z) in self.stars:
            y += z * speed
            if y > self.window_height:
                y = 0
            
            pos = (int(x), int(y))
            brightness = z * 128 + 10
            screen.draw.filled_circle(pos, 1, (brightness, brightness, brightness))

            stars.append((x, y, z))

        self.stars = stars
