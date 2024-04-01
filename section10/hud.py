from pgzero.screen import Screen

def draw_healtbar(
    screen: Screen,
    x: int,
    y: int,
    health: int,
):
    screen.blit("ui_glass_panel1", (x, y))
    for i in range(health):
        screen.blit("ui_health", (x + 6 + i * 21, y + 6))
    for i in range(6):
        screen.blit("ui_shadow", (x + 6 + i * 21, y + 6))
    
    screen.draw.text("health", (x + 2, y + 38), fontsize=11, fontname="kenny", color=(117, 151, 161))

def draw_score(
    screen: Screen,
    points: int,
    x: int,
    y: int,
):
    screen.blit("ui_glass_panel1", (x - 136, y))
    screen.draw.text(str(points), topright=(x, y), fontsize=32, fontname="kenny")

    screen.draw.text("score", topright=(x - 2, y + 38), fontsize=11, fontname="kenny", color=(117, 151, 161))