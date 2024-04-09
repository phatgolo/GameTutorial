# Chapter 11 (Game over and restart)

## About

In this chapter we are going to add a game over screen and a way to restart the game.

## Game over

Currently the game just quits when the player dies. We can do better and show a game over screen.

Let's start by adding a new game over screen. Make a copy of `ui_pause_menu.py`, change the name to `ui_game_over_menu.py` change the following following code:

```python
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
        ...
        self.restart_button = Button("restart", self.frame.centerx, self.frame_show_y - 20)
        ...


    def show(self, on_finished = None):
        for obj, y, duration in [
            ...
            (self.restart_button, -20, 0.55),
            ...
        ]:
            ...

    def hide(self, on_finished = None):
        for obj, y, duration in [
            ...
            (self.restart_button, -20, 0.21),
            ...
        ]:
            ...

    def on_mouse_down(self, pos, button) -> GameOverMenuActions:
        if button == mouse.LEFT:
            if self.restart_button.collidepoint(pos):
                return GameOverMenuActions.RESTART
            elif self.exit_button.collidepoint(pos):
                return GameOverMenuActions.EXIT

        return GameOverMenuActions.NONE

    def on_mouse_move(self, pos):
        self.restart_button.on_mouse_move(pos)
        ...

    def draw(self, screen: Screen):
        ...
        self.restart_button.draw(screen)
        ...
        screen.draw.text("Game Over", center=(self.frame.centerx, self.frame.top + 23), fontsize=28, fontname="kenny", color=(214, 221, 231))
```

Add the GameOverMenu to the game:

```python
...
from ui_game_over_menu import GameOverMenu, GameOverMenuActions

class GameState(Enum):
    ...
    GAME_OVER = 3,

class Game:
    def __init__(self):
        ...
        self.game_over_menu = GameOverMenu(window_width, window_height)
        ...

    def update(self):
        ...
        match self.state:
            case GameState.GAME:
                ...

                for asteroid in self.asteroid_field.asteroids:
                    if asteroid.circle_collidecircle(self.player.actor):
                        ...

                        if self.player.health <= 0:
                            self.update_state(GameState.GAME_OVER)
        ...

    def draw(self):
        ...
        match self.state:
            ...
            case GameState.GAME_OVER:
                self.star_field.draw(screen)
                self.asteroid_field.draw()
                self.player.draw(screen, False)

                self.game_over_menu.draw(screen)
        ...
    
    def update_state(self, new_state: GameState):
        match self.state:
            ...
            case GameState.GAME_OVER:
                self.game_over_menu.hide(lambda: self.set_state(new_state))
            ...
    
    def set_state(self, new_state: GameState):
        self.state = new_state
        match new_state:
            ...
            case GameState.GAME_OVER:
                self.game_over_menu.show()
    
    def on_mouse_down(self, pos, button):
        ...
        match self.state:
            ...
            case GameState.GAME_OVER:
                action = self.game_over_menu.on_mouse_down(pos, button)
                match action:
                    case GameOverMenuActions.RESTART:
                        self.update_state(GameState.GAME)
                    case GameOverMenuActions.EXIT:
                        self.update_state(GameState.MAIN_MENU)
            ...
    
    def on_mouse_move(self, pos):
        match self.state:
            ...
            case GameState.GAME_OVER:
                self.game_over_menu.on_mouse_move(pos)
            ...
```

So, making new menus is mostly copy paste at this point. The `GameOverMenu` is a bit different from the `PauseMenu` in that it doesn't have a `resume` button, but it has a `restart` button instead. It doesn't need to listen to the `escape` key either, so we can just skip that part.

▶️ **Run the game and see that it works (press `F5`)**

The game should now run, when you die you should see a game over screen. If you hit restart, you will get back to the game. Though, the game will not restart, it will just continue from where you died with no health. In order to fix this we need to add a RESTART state to the game.

## Restart

When the player dies, we need to reset the game. This means that we need to reset the player, the asteroids and the score.

Add a new state to the `GameState` enum:

```python
class GameState(Enum):
    MAIN_MENU = 0,
    PAUSE_MENU = 1,
    GAME = 2,
    GAME_OVER = 3,
    RESTART = 4,
```

Next we need to change the restart button in the game over screen to use this new state.

```python
class Game:
    def on_mouse_down(self, pos, button):
        ...
        match self.state:
            ...
            case GameState.GAME_OVER:
                ...
                match action:
                    case GameOverMenuActions.RESTART:
                        self.update_state(GameState.RESTART)
                    ...
            ...
```

...and add a new case to the `set_state` method:

```python
class Game:
    def set_state(self, new_state: GameState):
        ...
        match new_state:
            ...
            case GameState.RESTART:
                pass
            ...
```

Now in order to reset the player, asteroid field and the score, we can just re-create them in the `RESTART` state. Finally after we have done that, we can set the state to `GAME`.

```python
...

class Game:
    def set_state(self, new_state: GameState):
        ...
        match new_state:
            ...
            case GameState.RESTART:
                self.player = Player(
                    self.window_width, 
                    self.window_height
                )
                self.asteroid_field = AsteroidField(
                    self.window_width, 
                    self.window_height
                )
                self.score = 0
                self.update_state(GameState.GAME)
            ...
```

▶️ **Run the game and see that it works (press `F5`)**, you should now be able to restart the game when you die.

We have one last thing we can do. In the main menu, we can change the `START_GAME` action to set the state to `RESTART` instead of `GAME`.

```python
...

class Game:
    ...

    def on_mouse_down(self, pos, button):
        match self.state:
            case GameState.MAIN_MENU:
                ...
                match action:
                    case MainMenuActions.START_GAME:
                        self.update_state(GameState.RESTART)
                    ...
```

This way we always restart the game when we start it from the main menu.

▶️ **Run the game and see that it works (press `F5`)**, you should now be able to restart the game from the main menu as well.

### ✏️ Try on your own

> Can you add a continue button to the main menu that let's you continue if you have come to the main menu from the pause menu?

## Stuck?

If you get stuck, you can find the complete code here:

* [game_state.py](./game_state.py)
* [ui_game_over_menu.py](./ui_game_over_menu.py)

## Next

Next up, [Chapter 12 (Game levels)](../chapter12)
