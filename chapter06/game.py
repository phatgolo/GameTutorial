import pgzrun

from player import Player
from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

player = Player(WIDTH, HEIGHT)

def update():
    player.update()

def draw():
    screen.clear()
    player.draw(screen, True)

pgzrun.go()