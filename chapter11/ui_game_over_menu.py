from enum import Enum
from pgzero.builtins import Actor, mouse, animate
from pgzero.screen import Screen
from ui import Button

class GameOverMenuActions(Enum):
    NONE = 0
    RESTART = 1
    EXIT = 2

class GameOverMenu:
    def __init__(self, window_width: int, window_height: int):
        self.window_width = window_width
        self.window_height = window_height

        self.frame = Actor('ui_window2', anchor=("center", "center"), pos=(window_width / 2, window_height / 2))
        
        self.frame_show_y = self.frame.centery
        self.frame_hide_y = -(self.frame.height / 2)
        self.restart_button = Button("restart", self.frame.centerx, self.frame_show_y - 20)
        self.exit_button = Button("main menu", self.frame.centerx, self.frame_show_y + 20)


    def show(self, on_finished = None):
        for obj, y, duration in [
            (self.frame, 0, 0.5), 
            (self.restart_button, -20, 0.55),
            (self.exit_button, 20, 0.6)
        ]:
            obj.y = self.frame_hide_y + y
            animate(
                obj,
                tween="out_elastic",
                y=self.frame_show_y + y,
                duration=duration,
                on_finished=on_finished
            )

    def hide(self, on_finished = None):
        for obj, y, duration in [
            (self.frame, 0, 0.2), 
            (self.restart_button, -20, 0.21),
            (self.exit_button, 20, 0.22)
        ]:
            obj.y = self.frame_show_y + y
            animate(
                obj,
                tween="accelerate",
                y=self.frame_hide_y + y,
                duration=duration,
                on_finished=on_finished
            )

    def on_mouse_down(self, pos, button) -> GameOverMenuActions:
        if button == mouse.LEFT:
            if self.restart_button.collidepoint(pos):
                return GameOverMenuActions.RESTART
            elif self.exit_button.collidepoint(pos):
                return GameOverMenuActions.EXIT

        return GameOverMenuActions.NONE

    def on_mouse_move(self, pos):
        self.restart_button.on_mouse_move(pos)
        self.exit_button.on_mouse_move(pos)

    def draw(self, screen: Screen):
        self.frame.draw()
        self.restart_button.draw(screen)
        self.exit_button.draw(screen)
        screen.draw.text("Game Over", center=(self.frame.centerx, self.frame.top + 23), fontsize=28, fontname="kenny", color=(214, 221, 231))