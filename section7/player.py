from random import randint
from pgzero.builtins import Actor, keyboard
from pygame import Vector2

class Player:
    MAX_FORCE = 5
    
    def __init__(self, world_width: int, world_height: int):
        self.ship = Actor("player")
        self.main_thruster = Actor("thruster", anchor=("center", "top"))
        self.right_thruster = Actor("thruster_right", anchor=("left", "center"))
        self.left_thruster = Actor("thruster_left", anchor=("right", "center"))

        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.mass = 3
        self.world_width = world_width
        self.world_height = world_height

    def change_pos(self, delta: Vector2):
        self.set_pos(self.ship.pos + delta)

    def set_pos(self, pos: Vector2):
        self.ship.pos = pos
        self.main_thruster.pos = self.ship.midbottom
        self.right_thruster.pos = self.ship.midright
        self.left_thruster.pos = self.ship.midleft
    
    def place(self):
        self.set_pos(Vector2(self.world_width / 2, self.world_height - self.ship.height))

    def update(self):
        if self.force.length() < self.MAX_FORCE:
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
        
        else:
            self.force = Vector2(0, 0)

        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration
        self.change_pos(self.velocity)
        
        if self.ship.left < 0:
            self.ship.left = 0
            self.velocity = Vector2(0, 0)

        if self.ship.right > self.world_width:
            self.ship.right = self.world_width
            self.velocity = Vector2(0, 0)

        if self.ship.bottom > self.world_height:
            self.ship.bottom = self.world_height
            self.velocity = Vector2(0, 0)

        if self.ship.top < self.world_height / 2:
            self.ship.top = self.world_height / 2
            self.velocity = Vector2(0, 0)
        
        self.acceleration = Vector2(0, 0)
        
        self.velocity *= 0.9
        if self.velocity.magnitude() < 0.1:
            self.velocity = Vector2(0, 0)

    def draw(self):
        if self.force.y < 0:
            self.main_thruster.draw()
        
        if self.force.x < 0:
            self.right_thruster.draw()

        if self.force.x > 0:
            self.left_thruster.draw()
        
        self.main_thruster.draw()
        self.ship.draw()