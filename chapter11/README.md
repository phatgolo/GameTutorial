# Chapter 11 (Game over and restart)

## About

In this chapter we are going to add a game over screen and a way to restart the game.

## Game over

Currently the game just quits when the player dies. We can do better and show a game over screen.

Let's start by adding a new game over screen. Make a copy of `ui_pause_menu.py`, change the name to `ui_game_over_menu.py` change the following code:

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

The game should now run, when you die you should see a game over screen. If you hit restart, you will get back to the game. Though, the game will not restart, it will just continue from where you died with no health. In order to fix this we need to add a RESTART state to the game. More on that later.

### Explosion

When the player dies, we can add an explosion effect, let's start with the assets.

I've used assets again from [Tanks Pack](https://kenney.nl/assets/tanks) for this.

Copy the images to your `images` directory. And name them the following:
* ![Explosion images](images/fire_explosion1.png) `fire_explosion1.png`
* ![Explosion images](images/fire_explosion2.png) `fire_explosion2.png`
* ![Explosion images](images/fire_explosion3.png) `fire_explosion3.png`
* ![Explosion images](images/fire_explosion4.png) `fire_explosion4.png`

We will be able to re-use most of our `Explosion` class we created in [Chapter 9](../chapter09/README.md#explosions). The only thing we need to change is the images.

Your explosion class should look like this. We see that we are using the `gray_explosion` images, but we want to use the `fire_explosion` images instead.

```python
from pgzero.actor import Actor
from pgzhelper import *

class Explosion(Actor):
    def __init__(self, actor: Actor):
        super().__init__("gray_explosion1", (actor.x, actor.y))
        self.images = ["gray_explosion1", "gray_explosion2", "gray_explosion3", "gray_explosion4", "gray_explosion4"]
        self.fps = 10

    def animate_once(self) -> bool:
        frame = self.animate()
        done = frame == len(self.images) - 1
        return done
```

We could do this by changing the `__init__` method to use the `fire_explosion` images instead. But that would mean that the asteroids would also use the `fire_explosion` images. We don't want that. Instead we can add a new parameter to the `__init__` method that specifies which images to use.

```python
from typing import List
...

class Explosion(Actor):
    def __init__(self, actor: Actor, images: List[str]):
        super().__init__(images[0], (actor.x, actor.y))
        self.images = images
        self.fps = 10
```

To simplify things, we can also add two new classes that extends the `Explosion` class. One for the player and one for the asteroids.

```python
...

class PlayerExplosion(Explosion):
    def __init__(self, actor: Actor):
        super().__init__(actor, ["fire_explosion1", "fire_explosion2", "fire_explosion3", "fire_explosion4", "fire_explosion4"])

class AsteroidExplosion(Explosion):
    def __init__(self, actor: Actor):
        super().__init__(actor, ["gray_explosion1", "gray_explosion2", "gray_explosion3", "gray_explosion4", "gray_explosion4"])
```

Now we can use the new `AsteroidExplosion` class in the `AsteroidField` class.

```python
...
from explosion import AsteroidExplosion
...

class AsteroidField:
    ...
    
    def remove_asteroid(self, asteroid: Asteroid):
        self.explosions.append(AsteroidExplosion(asteroid))
        ...
```

▶️ **Run the game and see that it works (press `F5`)**, you should still see the asteroid explosions.

Now it's time to add the explosion to the player, when the player dies.

```python
...

class Player:
    def __init__(self, window_width: int, window_height: int):
        ...

        self.explosion = None
        self.dead = False
```

We start by adding a member variable to the `Player` class that will hold the explosion. We also add a `dead` member variable that will be used to check if the player is dead.

Next we add a new method we can call to explode the player. Let's also update the `take_damage` method to check if the player has exploded.

```python
...

class Player:
    ...

    def explode(self):
        self.dead = True
        self.explosion = PlayerExplosion(self.actor)

    def take_damage(self):
        if self.dead:
            return
        
        self.health -= 1

        if self.health <= 0:
            self.explode()

```

In the `take_damage` method we start by checking if the player is dead. If that is the case, we just return. `return` is a keyword that is used to return something from the method or function, in this case we just want to use that to exit the method early.
Next we decrease the health of the player by one. If the health is less than or equal to zero, we call the `explode` method.

We don't want the player to be able to move if dead, so we need to change the update method a bit, this is also the place where we can animate the explosion:

```python
...

class Player:
    ...

    def update(self):
        if not self.dead:
            self.handle_input()
            self.update_physics()

        if self.explosion:
            if self.explosion.animate_once():
                self.explosion = None
        ...
```

Let's also update the draw method to draw the explosion:

```python
...

class Player:
    ...

    def draw(self, screen: Screen, debug: bool = False):
        for projectile in self.projectiles:
            projectile.draw()

        if self.dead:
            if self.explosion:
                self.explosion.draw()
        else:
            if self.force.y <= 0:
                self.main_thruster.animate()
                self.main_thruster.draw()

            if self.force.y > 0:
                self.front_thruster.draw()
            if self.force.y < 0:
                self.main_thruster.draw()

            if self.force.x < 0:
                self.right_thruster.draw()
            if self.force.x > 0:
                self.left_thruster.draw()

            self.actor.draw()
```

This looks a bit messy, let's clean it up a bit. We can move the drawing of the player to a new method called `draw_alive`. We can also move the drawing of the explosion to a new method called `draw_dead`. Let's also remove the `debug` parameter, we don't need that anymore. This also means that we don't need `screen` either.

```python
...

class Player:
    ...

    def draw_alive(self):
        if self.force.y <= 0:
            self.main_thruster.animate()
            self.main_thruster.draw()

        if self.force.y > 0:
            self.front_thruster.draw()
        if self.force.y < 0:
            self.main_thruster.draw()

        if self.force.x < 0:
            self.right_thruster.draw()
        if self.force.x > 0:
            self.left_thruster.draw()

        self.actor.draw()

    def draw_dead(self):
        if self.explosion:
            self.explosion.draw()

    def draw(self):
        for projectile in self.projectiles:
            projectile.draw()

        if self.dead:
            self.draw_dead()
        else:
            self.draw_alive()
```

...and remove `screen` and `False` from the `draw` method of the `Game` class:

```python
...

class Game:
    def draw(self, screen: Screen):
        ...
        
        match self.state:
            ...
            case GameState.PAUSE_MENU:
                ...
                self.player.draw()

                ...
            case GameState.GAME:
                ...
                self.player.draw()

                ...
            case GameState.GAME_OVER:
                ...
                self.player.draw()

                ...

```

Now in order to hook this all up, we need to make more changes to the `Game` class. In the update method we can change the check for player health to check if the player is dead instead.

```python
...

class Game:
    ...

    def update(self):
        ...
        match self.state:
            case GameState.GAME:
                ...

                for asteroid in self.asteroid_field.asteroids:
                    if asteroid.circle_collidecircle(self.player.actor):
                        ...

                        if self.player.dead:
                            self.update_state(GameState.GAME_OVER)
        ...
```

We want the player and asteroids to update also when the game over screen shows. Let's make a case for that in the `update` method:

```python
...

class Game:
    ...

    def update(self):
        ...
        match self.state:
            ...
            case GameState.GAME_OVER:
                self.asteroid_field.update(0)
                self.player.update()
        ...
```

We need to pass in `0` to the `update` method of the asteroid_field since we don't want the asteroids to increese the score when the player is dead.

▶️ **Run the game and see that it works (press `F5`)**, you should now see the player exploding when health goes to zero.

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
