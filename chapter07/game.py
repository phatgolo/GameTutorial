import pgzrun

from player import Player
from asteriod_field import AsteroidField
from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

points = 0

player = Player(WIDTH, HEIGHT)
asteroid_field = AsteroidField(WIDTH, HEIGHT)

def update():
    global points
    points = asteroid_field.update(points)
    player.update()

    if asteroid_field.check_collision(player.actor):
        print("Game over")
        print(f"Points: {points}")
        exit()

def draw():
    screen.clear()
    asteroid_field.draw()
    player.draw(screen, False)

    screen.draw.text(str(points), topright=(WIDTH - 10, 10), fontsize=32)

pgzrun.go()