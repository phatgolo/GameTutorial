import pgzrun
from pgzero.builtins import Actor, keyboard

from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

player = Actor("player")

def update():
    if keyboard.a and player.left > 0:
        player.left -= 2
    if keyboard.d and player.right < WIDTH:
        player.left += 2

def draw():
    screen.clear()
    player.draw()

def place_player():
    player.x = WIDTH / 2
    player.y = HEIGHT - player.height

place_player()
pgzrun.go()