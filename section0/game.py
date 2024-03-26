import pgzrun
from pgzero.screen import Screen
screen: Screen

def draw():
    screen.draw.text("Hello world!", topleft=(10, 10))

pgzrun.go()