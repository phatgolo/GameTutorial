from pgzero.builtins import Actor, keyboard
from pygame import Vector2

class Player:
    MAX_FORCE = 5
    
    def __init__(self, world_width: int, world_height: int):
        self.actor = Actor("player")
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.world_width = world_width
        self.world_height = world_height

    def set_pos(self, x, y):
        self.actor.pos = x, y
    
    def place(self):
        self.set_pos(self.world_width / 2, self.world_height - self.actor.height)

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

        self.acceleration += self.force / 3
        self.velocity += self.acceleration
        self.actor.pos += self.velocity
        
        if self.actor.left < 0:
            self.actor.left = 0
            self.velocity = Vector2(0, 0)
        if self.actor.right > self.world_width:
            self.actor.right = self.world_width
            self.velocity = Vector2(0, 0)
        if self.actor.bottom > self.world_height:
            self.actor.bottom = self.world_height
        if self.actor.top < self.world_height / 2:
            self.actor.top = self.world_height / 2
        
        self.acceleration = Vector2(0, 0)
        
        self.velocity *= 0.9
        if self.velocity.magnitude() < 0.1:
            self.velocity = Vector2(0, 0)

    def draw(self):
        self.actor.draw()