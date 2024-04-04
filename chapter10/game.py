import pgzrun
from pgzero.screen import Screen
screen: Screen

from game_state import Game

WIDTH  = 800
HEIGHT = 600

game = Game(WIDTH, HEIGHT)

def update():
    game.update()

def draw():
    game.draw(screen)

def on_key_down(key):
    game.on_key_down(key)

def on_mouse_move(pos):
    game.on_mouse_move(pos)

def on_mouse_down(pos, button):
    game.on_mouse_down(pos, button)

pgzrun.go()