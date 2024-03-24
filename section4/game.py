import pgzrun
from pgzero.builtins import Actor, keyboard
from pygame import Vector2

from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

MAX_FORCE = 5

player = Actor("player")
player_velocity = Vector2(0, 0)
player_acceleration = Vector2(0, 0)
player_force = Vector2(0, 0)


def update():
    global player_force
    global player_velocity
    global player_acceleration

    if keyboard.a and player_force.length() < MAX_FORCE:
        player_force.x -= 1
    elif keyboard.d and player_force.length() < MAX_FORCE:
        player_force.x += 1
    elif keyboard.w and player_force.length() < MAX_FORCE:
        player_force.y -= 1
    elif keyboard.s and player_force.length() < MAX_FORCE:
        player_force.y += 1
    else:
        player_force.x = 0

    player_acceleration += player_force / 3
    player_velocity += player_acceleration
    player.pos += player_velocity
    
    if player.left < 0:
        player.left = 0
        player_velocity = Vector2(0, 0)
    if player.right > WIDTH:
        player.right = WIDTH
        player_velocity = Vector2(0, 0)
    
    player_acceleration = Vector2(0, 0)
    
    player_velocity *= 0.9
    if player_velocity.magnitude() < 0.1:
        player_velocity = Vector2(0, 0)

def draw():
    global player_force
    global player_velocity
    global player_acceleration

    screen.clear()
    screen.draw.text("player_force: {vel}".format(vel = player_force.x), topleft=(10, 10))
    screen.draw.text("player_velocity: {vel}".format(vel = player_velocity.x), topleft=(10, 30))
    screen.draw.text("player_acceleration: {vel}".format(vel = player_acceleration.x), topleft=(10, 50))
    player.draw()

def place_player():
    player.x = WIDTH / 2
    player.y = HEIGHT - player.height

place_player()
pgzrun.go()