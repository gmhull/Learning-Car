import numpy as np
import pyglet, sys, math
from pyglet.gl import *
from pyglet.window import key
import GeneticAlgorithm as GA
from create_track import create_track # make sure this works

# 1. Create the GA and initialize the population
# 2. Drive the cars
# 3. Calculate the fitness of the cars after crashing
# 4. Generate children from the initial generaion of cars (Crossover and Mutate)
# 5. Delete the previous set of cars and drive the new generation

def reset_schedule():
    for car in GA.pop:
        pyglet.clock.unschedule(car.update)
        pyglet.clock.schedule_interval(car.update, 1 / 60.0)

if __name__ == '__main__':
    width, height = 1000, 700
    game_window = pyglet.window.Window(width,height)
    walls, checkpoints = create_track(width,height)

    neuron_shape = (5,3,3,1)
    GA = GA.GeneticAlgorithm(5, 0.03)
    GA.create_population(neuron_shape)

    @game_window.event
    def on_draw():
        game_window.clear()
        stopped_cars = 0
        for car in GA.pop:
            if car:
                car.draw()
                for wall in walls:
                    wall.show()
                    pt = car.check_collision(wall)
                    if pt: car.alive = False
                car.look(walls)
                for gate in checkpoints:
                    pt = car.check_collision(gate)
                    if pt:
                        car.update_score(gate)

                # resets the system when the cars are all stopped
                if car.alive == False:
                    stopped_cars += 1
                if stopped_cars == GA.pop_size:
                    GA.calc_score()
                    GA.evolve()
                    print("max", GA.maxScore)
                    print("best genes", GA.bestGenes)
                    reset_schedule()

    reset_schedule()

    pyglet.app.run()
