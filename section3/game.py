import pgzrun
from pgzero.builtins import Actor, keyboard
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

def update():
    if keyboard.a and player.left > 0:
        player.x -= 1
    if keyboard.d and player.right < WIDTH:
        player.x += 1

def draw():
    screen.clear()
    player.draw()

scale_and_place_player()
pgzrun.go()