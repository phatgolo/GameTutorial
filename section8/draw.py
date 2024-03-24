from pgzero.screen import Screen
from pygame.rect import Rect
from pygame.color import Color

def draw_healtbar(
    screen: Screen, 
    value: int, 
    max_value: int, 
    # world_width: int, world_height: int
):
    width = int((value / max_value) * 100.0)
    print(width)
    color = Color(127, 127, 127)
    
    if width <= 50:
        color = Color(127, 127, 0)

    if width <= 25:
        color = Color(127, 0, 0)
        
    screen.draw.rect(Rect(8, 8, 104, 24), Color(127, 127, 127))
    screen.draw.filled_rect(Rect(10, 10, width, 20), color)
    screen.draw.text("{health}%".format(health = width), center=(60, 20))