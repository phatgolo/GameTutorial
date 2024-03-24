import pgzrun
from player import Player
from asteroids import Asteroids

from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

MAX_FORCE = 5

player = Player(WIDTH, HEIGHT)
asteroids = Asteroids(WIDTH, HEIGHT)
score = 0

def update():
    global score
    score = asteroids.update(score)
    if asteroids.collides(player.ship):
        quit()

    player.update()

def draw():
    global score
    screen.clear()
    asteroids.draw()
    player.draw()
    screen.draw.text("Score: {score}".format(score = score), topleft=(10, 10))

player.place()
pgzrun.go()