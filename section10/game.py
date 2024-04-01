import pgzrun

from hud import draw_healtbar, draw_score
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

    asteroid = asteroid_field.check_collision(player.actor)
    if asteroid:
        player.take_damage()
        asteroid_field.remove_asteroid(asteroid)

        if player.health <= 0:
            print("Game Over")
            print("Score: ", points)
            quit()

def draw():
    screen.clear()

    asteroid_field.draw()
    player.draw(screen, False)

    draw_healtbar(screen, 10, 10, player.health)
    draw_score(screen, points, WIDTH - 10, 10)

pgzrun.go()