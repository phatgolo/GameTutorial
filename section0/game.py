import pgzrun
import pgzero
screen: pgzero.screen.Screen

def draw():
    screen.draw.text("Hello world!", topleft=(10, 10))

pgzrun.go()