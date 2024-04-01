import pgzrun
from pgzero.builtins import Actor, keyboard
from pygame import Vector2

from pgzhelper import *
from pgzero.screen import Screen
screen: Screen

WIDTH  = 800
HEIGHT = 600

MAX_FORCE = 3
MAX_VELOCITY = 10


player = Actor("player")
player_acceleration = Vector2(0, 0)
player_debug_acceleration = Vector2(0, 0)
player_velocity = Vector2(0, 0)
player_force = Vector2(0, 0)
player_mass = 2

def scale_and_place_player():
    player.scale = 0.5
    player.x = WIDTH / 2
    player.y = HEIGHT - player.height

def update():
    global player_force, player_acceleration, player_debug_acceleration, player_velocity

    if keyboard.a:
        player_force.x -= 1
    if keyboard.d:
        player_force.x += 1
    if keyboard.w:
        player_force.y -= 1
    if keyboard.s:
        player_force.y += 1
    
    if not keyboard.a and not keyboard.d and not keyboard.w and not keyboard.s:
        player_force = Vector2(0, 0)

    if player_force.magnitude() > 0:
        player_force.clamp_magnitude_ip(0, MAX_FORCE)

    player_acceleration += player_force / player_mass
    player_velocity += player_acceleration
    
    if player_velocity.magnitude() > 0:
        player_velocity.clamp_magnitude_ip(0, MAX_VELOCITY)
    
    player.pos += player_velocity
    
    if player.left < 0:
        player.left = 0
        player_velocity.x = 0
    if player.right > WIDTH:
        player.right = WIDTH
        player_velocity.x = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        player_velocity.y = 0
    if player.top < 0:
        player.top = 0
        player_velocity.y = 0
    
    player_debug_acceleration = player_acceleration
    player_acceleration = Vector2(0, 0)
    
    player_velocity *= 0.92
    if player_velocity.magnitude() < 0.1:
        player_velocity = Vector2(0, 0)

def draw():
    screen.clear()
    player.draw()

    print_vector("player_force", player_force, 10, 10)
    print_vector("player_acceleration", player_debug_acceleration, 10, 50)
    print_vector("player_velocity", player_velocity, 10, 30)

def print_vector(text: str, vec: Vector2, left: int, top: int):
    screen.draw.text(
        "{0}: ({1:.2f}, {2:.2f})".format(
            text, 
            vec.x,
            vec.y
        ), 
        topleft=(left, top)
    )


scale_and_place_player()
pgzrun.go()