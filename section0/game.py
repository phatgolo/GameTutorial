import pgzrun
from pgzero.screen import Screen
screen: Screen

def draw():
    screen.draw.text("Hello world!", topleft=(10, 10))
    screen.draw.line((400, 300), (800, 600), (255, 255, 255))
    screen.draw.line((400, 300), (800, 0), (255, 255, 255))
    screen.draw.line((400, 300), (0, 600), (255, 255, 255))
    screen.draw.line((400, 300), (0, 0), (255, 255, 255))

pgzrun.go()