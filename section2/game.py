import pgzrun
from pgzero.builtins import Actor

WIDTH  = 800
HEIGHT = 600

player = Actor("player")

def draw():
    player.draw()

def place_player():
    player.x = WIDTH / 2
    player.y = HEIGHT - player.height

place_player()
pgzrun.go()