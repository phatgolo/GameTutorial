from enum import Enum
from typing import Optional
from pgzero.builtins import Actor, mouse
from pgzero.screen import Screen
from ui import Button

class MenuActions(Enum):
    NONE = 0
    START_GAME = 1
    QUIT = 2

class Menu:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.frame = Actor('ui_window1', anchor=("center", "center"), pos=(window_width / 2, window_height / 2))
        
        self.play_button = Button("start", self.frame.centerx, self.frame.centery - 20)
        self.quit_button = Button("quit", self.frame.centerx, self.frame.centery + 20)

    def on_mouse_down(self, pos, button) -> MenuActions:
        if button == mouse.LEFT:
            if self.play_button.collidepoint(pos):
                return MenuActions.START_GAME
            elif self.quit_button.collidepoint(pos):
                return MenuActions.QUIT

        return MenuActions.NONE

    def on_mouse_move(self, pos):
        self.play_button.on_mouse_move(pos)
        self.quit_button.on_mouse_move(pos)

    def draw(self, screen: Screen):
        self.frame.draw()

        self.play_button.draw(screen)
        self.quit_button.draw(screen)

        screen.draw.text(
            "Game Name", 
            center=(self.frame.centerx, self.frame.top + 23), 
            fontsize=28, 
            fontname="kenny", 
            color=(214, 221, 231)
        )