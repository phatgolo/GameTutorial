from pgzero.builtins import Actor, keyboard
from pygame import Vector2
from pgzero.screen import Screen
from pgzhelper import *

MAX_VELOCITY = 5
MAX_FORCE = 3

class Player:
    def __init__(self, window_width: int, window_height: int):
        self.actor = Actor('player')
        self.actor.scale = 0.5
        self.actor.radius = self.actor.width * 0.3

        self.health = 6

        self.main_thruster = Actor("thruster", anchor=("center", "top"))
        self.main_thruster.scale = 0.5
        self.front_thruster = Actor("side_thruster", anchor=("center", "top"))
        self.front_thruster.angle = 180
        self.right_thruster = Actor("side_thruster", anchor=("center", "top"))
        self.right_thruster.angle = 90
        self.left_thruster = Actor("side_thruster", anchor=("center", "top"))
        self.left_thruster.angle = -90

        self.draw_thrusters = False

        self.actor.x = window_width / 2
        self.actor.y = window_height - self.actor.height
        self.acceleration = Vector2(0, 0)
        self.debug_acceleration = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.mass = 1
        self.window_width = window_width
        self.window_height = window_height

    def take_damage(self):
        self.health -= 1

    def print_vector(self, screen: Screen, text: str, vec: Vector2, left: int, top: int):
        screen.draw.text("{0}: ({1:.2f}, {2:.2f})".format(text, vec.x, vec.y), topleft=(left, top))

    def handle_input(self):
        if keyboard.a:
            self.force.x -= 1
        if keyboard.d:
            self.force.x += 1
        if keyboard.w:
            self.force.y -= 1
        if keyboard.s:
            self.force.y += 1
        if not keyboard.a and not keyboard.d and not keyboard.w and not keyboard.s:
            self.force = Vector2(0, 0)

    def position_player(self):
        self.actor.pos += self.velocity
        self.main_thruster.pos = self.actor.midbottom
        self.front_thruster.pos = self.actor.midtop + Vector2(0, 6)
        self.right_thruster.pos = self.actor.midright + Vector2(-6, 6)
        self.left_thruster.pos = self.actor.midleft + Vector2(6, 6)

        if self.actor.left < 0:
            self.actor.left = 0
            self.velocity.x = 0
        if self.actor.right > self.window_width:
            self.actor.right = self.window_width
            self.velocity.x = 0
        if self.actor.bottom > self.window_height:
            self.actor.bottom = self.window_height
            self.velocity.y = 0
        if self.actor.top < 0:
            self.actor.top = 0
            self.velocity.y = 0

    def update_physics(self):
        if self.force.magnitude() > 0:
            self.force.clamp_magnitude_ip(0, MAX_FORCE)

        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration

        if self.velocity.magnitude() > 0:
            self.velocity.clamp_magnitude_ip(0, MAX_VELOCITY)

        self.position_player()

        self.debug_acceleration = self.acceleration
        self.acceleration = Vector2(0, 0)
        self.velocity *= 0.92
        if self.velocity.magnitude() < 0.1:
            self.velocity = Vector2(0, 0)

    def update(self):
        self.handle_input()
        self.update_physics()

    def draw(self, screen: Screen, debug: bool = False):
        if self.force.y <= 0:
            self.main_thruster.animate()
            self.main_thruster.draw()

        if self.force.y > 0:
            self.front_thruster.draw()
        if self.force.y < 0:
            self.main_thruster.draw()

        if self.force.x < 0:
            self.right_thruster.draw()
        if self.force.x > 0:
            self.left_thruster.draw()

        self.actor.draw()

        if debug:
            self.print_vector(screen, "Force", self.force, 10, 10)
            self.print_vector(screen, "Acceleration", self.debug_acceleration, 10, 30)
            self.print_vector(screen, "Velocity", self.velocity, 10, 50)

def maprange(x: int, a: int, b: int, c: int, d: int):
    w =  (x-a) / (b-a)
    y = c + w * (d-c)
    return y