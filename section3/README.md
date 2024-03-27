# Section 3 (Move the player)

## About

In this section we will start looking into how to control the player from the keyboard.

## The update function

As mentioned in the previous section we are using a special function called `draw`, that pgzero calls 60 times per second. There is also a concept of an `update` function built in. Use the update function if you want to update things in the game. To add it, type the following directly over the draw function:

```python
def update():
    pass
```

The keyword `pass` means that we don't want to do anything here yet. We will soon replace it with some code though. But first we need to import a keyboard controller.

At the top of the document we already import `Actor` (`from pgzero.builtins import Actor`), directly to the right of Actor, on the same line, type `, keyboard` like so:

```python
from pgzero.builtins import Actor, keyboard
```

With the new keyboard imported, we can add some logic to the update function. We want to control the player with `WASD` on the keyboard. If you press `A`, we want to player to move to the left. Let's add that:


```python
def update():
    if keyboard.a:
        player.x -= 1
```

Remember, similarly to the draw function, the update function is called around 60 times per second. So as long as a is pressed, we will move the player to the left by 1 pixel per frame. `-=` means set the value `player.x` of it's current value minus what ever comes after, in this case 1. You can also write `+=`, `*=` and `/=`. Another way of writing this is `player.x = player.x - 1`, which would be the same thing.

▶️ **Run the game and see that it works (press `F5`)**, you should be able to move to the left by pressing `A` on your keyboard. But something is off.

<img src="../.docs/image13.png">

The spaceship is drawn on top of the old one. Perhaps a cool effect but we need to clear the window every frame to solve this.

In the `draw` function add `screen.clear()`:

```python
def draw():
    screen.clear()
    player.draw()
```

▶️ **Run the game and see that it works (press `F5`)**, now you should **not** see a trail of ships when you move the player to the left.

Ok, so let's add right as well:

```python
def update():
    if keyboard.a:
        player.x -= 1

    if keyboard.d:
        player.x += 1
```

▶️ **Run the game and see that it works (press `F5`)**, you should be able to move to the left and right by pressing `A` and `D` on your keyboard.

One problem is that we can move the player off screen, let's limit it to the sides of the screen. We can do that by updating the `update` function like this:

```python
def update():
    if keyboard.a:
        player.x -= 1
    if keyboard.d:
        player.x += 1

    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
```

So if the player is to the left of the window, we set the left side of the player to be 0. If the player is to the right of the window, we set the right side of the player to be the width of the window.

This will limit the players movement to the right and left side of the window.

▶️ **Run the game and see that it works (press `F5`)**, you should be able to move the player with your `A` and `D` keys on the keyboard.

<img src="../.docs/section3.png">

### ✏️ Try on your own

> 📋 Can you change the how quickly the player moves?

## Stuck?

If you get stuck, you can find the complete code here:
* [game.py](./game.py)

## Next

Next up, [Section 4 (Player physics)](../section4)