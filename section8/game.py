import pgzrun
from player import Player
from asteroids import Asteroids
from draw import draw_healtbar

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
        dead = player.take_damage(10)
        if dead:
            quit()


    player.update()

def draw():
    global score
    screen.clear()
    asteroids.draw()
    player.draw()
    screen.draw.text("Score: {score}".format(score = score), topright=(WIDTH - 10, 10))
    # screen.draw.text("Health: {health}".format(health = player.health), topleft=(10, 10))
    draw_healtbar(screen, player.health, player.max_health)

pgzrun.go()