import pgzrun
from pgzero.builtins import Actor

player = Actor("player")

def draw():
    player.draw()

pgzrun.go()