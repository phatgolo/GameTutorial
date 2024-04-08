from enum import Enum
from pgzero.builtins import Actor, mouse, animate
from pgzero.screen import Screen
from ui import Button

class MainMenuActions(Enum):
    NONE = 0
    START_GAME = 1
    QUIT = 2

class MainMenu:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.frame = Actor('ui_window1', anchor=("center", "center"), pos=(window_width / 2, window_height / 2))
        
        self.frame_show_y = self.frame.centery
        self.frame_hide_y = window_height + (self.frame.height / 2)
        self.start_button = Button("start", self.frame.centerx, self.frame_show_y - 20)
        self.quit_button = Button("quit", self.frame.centerx, self.frame_show_y + 20)

    def show(self, on_finished = None):
        for obj, y in [
            (self.frame, 0), 
            (self.start_button, -20),
            (self.quit_button, 20)
        ]:
            obj.y = self.frame_hide_y + y
            animate(
                obj,
                tween="accelerate",
                y=self.frame_show_y + y,
                duration=0.2,
                on_finished=on_finished
            )
            
    def hide(self, on_finished = None):
        for obj, y in [
            (self.frame, 0), 
            (self.start_button, -20),
            (self.quit_button, 20)
        ]:
            obj.y = self.frame_show_y + y
            animate(
                obj,
                tween="accelerate",
                y=self.frame_hide_y + y,
                duration=0.2,
                on_finished=on_finished
            )

    def on_mouse_down(self, pos, button) -> MainMenuActions:
        if button == mouse.LEFT:
            if self.start_button.collidepoint(pos):
                return MainMenuActions.START_GAME
            elif self.quit_button.collidepoint(pos):
                return MainMenuActions.QUIT

        return MainMenuActions.NONE

    def on_mouse_move(self, pos):
        self.start_button.on_mouse_move(pos)
        self.quit_button.on_mouse_move(pos)

    def draw(self, screen: Screen):
        self.frame.draw()

        self.start_button.draw(screen)
        self.quit_button.draw(screen)

        screen.draw.text(
            "Game Name", 
            center=(self.frame.centerx, self.frame.top + 23), 
            fontsize=28, 
            fontname="kenny", 
            color=(214, 221, 231)
        )