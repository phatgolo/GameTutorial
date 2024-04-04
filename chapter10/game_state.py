from enum import Enum
from pgzero.screen import Screen

from pgzero.builtins import keys

from asteriod_field import AsteroidField
from player import Player
from star_field import StarField

from ui_hud import draw_healtbar, draw_score
from ui_menu import Menu, MenuActions
from ui_pause_menu import PauseMenu, PauseActions

class GameState(Enum):
    MAIN_MENU = 0,
    PAUSE_MENU = 1,
    GAME = 2,

class Game:
    def __init__(self, window_width: int, window_height: int):
        self.state = GameState.MAIN_MENU

        self.window_width = window_width
        self.window_height = window_height
        
        self.player = Player(window_width, window_height)
        self.asteroid_field = AsteroidField(window_width, window_height)
        self.star_field = StarField(window_width, window_height)

        self.menu = Menu(window_width, window_height)
        self.pause_menu = PauseMenu(window_width, window_height)
        
        self.score = 0

    def update(self):
        match self.state:
            case GameState.GAME:
                self.score = self.asteroid_field.update(self.score)
                self.player.update()

                for asteroid in self.asteroid_field.asteroids:
                    if asteroid.circle_collidecircle(self.player.actor):
                        self.player.take_damage()
                        self.asteroid_field.remove_asteroid(asteroid)

                        if self.player.health <= 0:
                            print("Game Over")
                            print("Score: ", self.points)
                            quit()

                    for projectile in self.player.projectiles:
                        if projectile.colliderect(asteroid):
                            self.asteroid_field.remove_asteroid(asteroid)
                            self.player.projectiles.remove(projectile)
            case _:
                pass

    def draw(self, screen: Screen):
        screen.clear()
        
        match self.state:
            case GameState.MAIN_MENU:
                self.star_field.draw(screen)
                self.menu.draw(screen)
            case GameState.PAUSE_MENU:
                self.star_field.draw(screen, 0)
                self.asteroid_field.draw()
                self.player.draw(screen, False)

                self.pause_menu.draw(screen)
            case GameState.GAME:
                self.star_field.draw(screen)
                self.asteroid_field.draw()
                self.player.draw(screen, False)

                draw_healtbar(screen, 10, 10, self.player.health)
                draw_score(screen, self.score, self.window_width - 10, 10)

    def on_mouse_down(self, pos, button):
        match self.state:
            case GameState.MAIN_MENU:
                action = self.menu.on_mouse_down(pos, button)
                match action:
                    case MenuActions.START_GAME:
                        self.state = GameState.GAME
                    case MenuActions.QUIT:
                        quit()
            case GameState.PAUSE_MENU:
                action = self.pause_menu.on_mouse_down(pos, button)
                match action:
                    case PauseActions.CONTINUE:
                        self.state = GameState.GAME
                    case PauseActions.EXIT:
                        self.state = GameState.MAIN_MENU
            case _:
                pass

    def on_mouse_move(self, pos):
        match self.state:
            case GameState.MAIN_MENU:
                self.menu.on_mouse_move(pos)
            case GameState.PAUSE_MENU:
                self.pause_menu.on_mouse_move(pos)
            case _:
                pass

    def on_key_down(self, key):
        match self.state:
            case GameState.GAME:
                self.player.handle_key_down(key)
                if key == keys.ESCAPE:
                    self.state = GameState.PAUSE_MENU
            case _:
                pass