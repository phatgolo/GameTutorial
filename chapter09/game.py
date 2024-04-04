import pgzrun

from player import Player
from asteriod_field import AsteroidField

from pgzero.screen import Screen
from pgzhelper import *

from hud import draw_healtbar, draw_score

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

    for asteroid in asteroid_field.asteroids:
        if asteroid.circle_collidecircle(player.actor):
            player.take_damage()
            asteroid_field.remove_asteroid(asteroid)

            if player.health <= 0:
                print("Game Over")
                print("Score: ", points)
                quit()

        for projectile in player.projectiles:
            if projectile.colliderect(asteroid):
                asteroid_field.remove_asteroid(asteroid)
                player.projectiles.remove(projectile)

def draw():
    screen.clear()

    asteroid_field.draw()
    player.draw(screen, False)

    draw_healtbar(screen, 10, 10, player.health)
    draw_score(screen, points, WIDTH - 10, 10)

def on_key_down(key):
    player.handle_key_down(key)

pgzrun.go()