from pgzero.builtins import Actor
from pgzero.screen import Screen

class Button(Actor):
    def __init__(self, text: str, x: int, y: int):
        super().__init__("ui_button", anchor=("center", "center"))
        self.text = text
        self.text_color = (50, 50, 50)
        self.x = x
        self.y = y

    def on_mouse_move(self, pos):
        if self.collidepoint(pos):
            self.image = "ui_button_hover"
            self.text_color = (250, 250, 250)
        else:
            self.image = "ui_button"
            self.text_color = (50, 50, 50)

    def draw(self, screen: Screen):
        super().draw()
        screen.draw.text(
            self.text, 
            center=(self.x, self.y), 
            fontsize=18, 
            fontname="kenny", 
            color=self.text_color
        )