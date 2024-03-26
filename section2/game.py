import pgzrun
from pgzero.builtins import Actor
from pgzhelper import *
from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

player = Actor("player")

def scale_and_place_player():
    player.scale = 0.5
    player.x = WIDTH / 2
    player.y = HEIGHT - player.height

def draw():
    player.draw()

scale_and_place_player()
pgzrun.go()