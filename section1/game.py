import pgzrun
from pgzero.builtins import Actor

from pgzero.screen import Screen
screen: Screen

player = Actor("player")

def draw():
    player.draw()

pgzrun.go()