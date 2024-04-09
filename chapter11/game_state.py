from enum import Enum
from pgzero.screen import Screen

from pgzero.builtins import keys

from asteriod_field import AsteroidField
from player import Player
from star_field import StarField

from ui_hud import draw_healtbar, draw_score
from ui_main_menu import MainMenu, MainMenuActions
from ui_pause_menu import PauseMenu, PauseMenuActions
from ui_game_over_menu import GameOverMenu, GameOverMenuActions

class GameState(Enum):
    MAIN_MENU = 0,
    PAUSE_MENU = 1,
    GAME = 2,
    GAME_OVER = 3,
    RESTART = 4,

class Game:
    def __init__(self, window_width: int, window_height: int):
        self.state = GameState.MAIN_MENU

        self.window_width = window_width
        self.window_height = window_height
        
        self.player = Player(window_width, window_height)
        self.asteroid_field = AsteroidField(window_width, window_height)
        self.star_field = StarField(window_width, window_height)

        self.main_menu = MainMenu(window_width, window_height)
        self.pause_menu = PauseMenu(window_width, window_height)
        self.game_over_menu = GameOverMenu(window_width, window_height)
        
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

                        if self.player.dead:
                            self.update_state(GameState.GAME_OVER)

                    for projectile in self.player.projectiles:
                        if projectile.colliderect(asteroid):
                            self.asteroid_field.remove_asteroid(asteroid)
                            self.player.projectiles.remove(projectile)
            case GameState.GAME_OVER:
                self.asteroid_field.update(0)
                self.player.update()
            case _:
                pass

    def draw(self, screen: Screen):
        screen.clear()
        
        match self.state:
            case GameState.MAIN_MENU:
                self.star_field.draw(screen)
                self.main_menu.draw(screen)
            case GameState.PAUSE_MENU:
                self.star_field.draw(screen, 0)
                self.asteroid_field.draw()
                self.player.draw()

                self.pause_menu.draw(screen)
            case GameState.GAME:
                self.star_field.draw(screen)
                self.asteroid_field.draw()
                self.player.draw()

                draw_healtbar(screen, 10, 10, self.player.health)
                draw_score(screen, self.score, self.window_width - 10, 10)
            case GameState.GAME_OVER:
                self.star_field.draw(screen)
                self.asteroid_field.draw()
                self.player.draw()

                self.game_over_menu.draw(screen)

    def update_state(self, new_state: GameState):
        match self.state:
            case GameState.MAIN_MENU:
                self.main_menu.hide(lambda: self.set_state(new_state))
            case GameState.PAUSE_MENU:
                self.pause_menu.hide(lambda: self.set_state(new_state))
            case GameState.GAME_OVER:
                self.game_over_menu.hide(lambda: self.set_state(new_state))
            case _:
                self.set_state(new_state)

    def set_state(self, new_state: GameState):
        self.state = new_state
        match new_state:
            case GameState.MAIN_MENU:
                self.main_menu.show()
            case GameState.PAUSE_MENU:
                self.pause_menu.show()
            case GameState.GAME_OVER:
                self.game_over_menu.show()
            case GameState.RESTART:
                self.player = Player(self.window_width, self.window_height)
                self.asteroid_field = AsteroidField(self.window_width, self.window_height)
                self.score = 0
                self.update_state(GameState.GAME)
            case GameState.GAME:
                pass

    def on_mouse_down(self, pos, button):
        match self.state:
            case GameState.MAIN_MENU:
                action = self.main_menu.on_mouse_down(pos, button)
                match action:
                    case MainMenuActions.START_GAME:
                        self.update_state(GameState.RESTART)
                    case MainMenuActions.QUIT:
                        quit()
            case GameState.PAUSE_MENU:
                action = self.pause_menu.on_mouse_down(pos, button)
                match action:
                    case PauseMenuActions.CONTINUE:
                        self.update_state(GameState.GAME)
                    case PauseMenuActions.EXIT:
                        self.update_state(GameState.MAIN_MENU)
            case GameState.GAME_OVER:
                action = self.game_over_menu.on_mouse_down(pos, button)
                match action:
                    case GameOverMenuActions.RESTART:
                        self.update_state(GameState.RESTART)
                    case GameOverMenuActions.EXIT:
                        self.update_state(GameState.MAIN_MENU)
            case _:
                pass

    def on_mouse_move(self, pos):
        match self.state:
            case GameState.MAIN_MENU:
                self.main_menu.on_mouse_move(pos)
            case GameState.PAUSE_MENU:
                self.pause_menu.on_mouse_move(pos)
            case GameState.GAME_OVER:
                self.game_over_menu.on_mouse_move(pos)
            case _:
                pass

    def on_key_down(self, key):
        match self.state:
            case GameState.GAME:
                self.player.handle_key_down(key)
                if key == keys.ESCAPE:
                    self.update_state(GameState.PAUSE_MENU)
            case GameState.PAUSE_MENU:
                if key == keys.ESCAPE:
                    self.update_state(GameState.GAME)
            case _:
                pass