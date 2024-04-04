from enum import Enum
from typing import Optional
from pgzero.builtins import Actor, mouse
from pgzero.screen import Screen
from ui import Button

class PauseActions(Enum):
    CONTINUE = 0
    EXIT = 1

class PauseMenu:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.frame = Actor('ui_window2', anchor=("center", "center"), pos=(window_width / 2, window_height / 2))
        
        self.continue_button = Button("continue", self.frame.centerx, self.frame.centery - 20)
        self.exit_button = Button("exit", self.frame.centerx, self.frame.centery + 20)

    def on_mouse_down(self, pos, button) -> Optional[int]:
        if button == mouse.LEFT:
            if self.continue_button.collidepoint(pos):
                return PauseActions.CONTINUE
            elif self.exit_button.collidepoint(pos):
                return PauseActions.EXIT
            else:
                return None
        return None

    def on_mouse_move(self, pos):
        self.continue_button.on_mouse_move(pos)
        self.exit_button.on_mouse_move(pos)

    def draw(self, screen: Screen):
        self.frame.draw()
        self.continue_button.draw(screen)
        self.exit_button.draw(screen)
        screen.draw.text("Pause", center=(self.frame.centerx, self.frame.top + 23), fontsize=28, fontname="kenny", color=(214, 221, 231))