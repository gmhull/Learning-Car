import numpy as np
import pyglet, sys, math
from pyglet.gl import *
from pyglet.window import key
from NewCar import Car
from NewTrack import *
import tensorflow as tf
import os
import TrainCar

# @game_window.event
# def on_mouse_press(x,y,button,modifiers):
#     game.draw_walls(x,y,button)

screen_width, screen_height = 1400, 700
training = False

score = 0

try:
    model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[1])
    print('models\\'+os.listdir('models\\')[1])
    print("ready to rock")
except:
    print('you messed up')

def test():
    game_window = pyglet.window.Window(screen_width,screen_height)
    # Keep track of the keys that are pressed in the window.  Saved as the variable 'keys'.
    keys = key.KeyStateHandler()
    game_window.push_handlers(keys)
    # keys = 0
    # Initialize the game, create the walls, create the car
    game = Game(screen_width, screen_height, keys)
    game.reset()

    @game_window.event
    def on_draw():
        game_window.clear()
        if game.car.alive == True:
            game.car.draw()
            game.car.show_walls()

    # This update is called every 1/120th of a second based on the schedule_interval
    # function below.  This will send the car the key pressed data to move.
    def update(dt):
        global score
        action = np.argmax(model.predict(np.array([game.car.SPACE_STATE,]))[0])
        game.car.SPACE_STATE, reward, done = game.step(action)
        score += reward
        if game.car.alive == False or done:
            game.reset()
            score = 0

    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()

def train(EPISODES, AGGREGATE_STATS_EVERY, MODEL):
    TrainCar.training(EPISODES, AGGREGATE_STATS_EVERY, MODEL)

def play():
    game_window = pyglet.window.Window(screen_width,screen_height)
    # Keep track of the keys that are pressed in the window.  Saved as the variable 'keys'.
    keys = key.KeyStateHandler()
    game_window.push_handlers(keys)

    # Initialize the game, create the walls, create the car
    game = Game(screen_width, screen_height, keys)
    game.reset()

    @game_window.event
    def on_draw():
        game_window.clear()
        if game.car.alive == True:
            game.car.draw()
            game.car.show_walls()

    # This update is called every 1/120th of a second based on the schedule_interval
    # function below.  This will send the car the key pressed data to move.
    def update(dt):
        game.car.player_control(keys)
        if game.car.alive == False:
            game.reset()

    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()

if __name__ == "__main__":
    EPISODES = 100
    AGGREGATE_STATS_EVERY = 1
    # train(EPISODES, AGGREGATE_STATS_EVERY, model)
    test()
    # play()
