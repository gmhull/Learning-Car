import pyglet
from pyglet.gl import *
from NewCar import Car


class Boundary(object):
    def __init__(self,p1,p2):
        self.a = p1
        self.b = p2
        self.color = [255, 0, 0]
    def show(self):
        pyglet.graphics.draw(2,GL_LINES,
            ('v2f',(self.a[0],self.a[1],self.b[0],self.b[1])),
            ('c3B', self.color * 2))

class Point(object):
    def __init__(self,pt):
        self.pt = pt
        self.color = [0, 200, 0]
    def show(self):
        pyglet.graphics.draw(1,GL_POINTS,
            ('v2f',(self.pt[0],self.pt[1])))

class Game(object):
    """docstring for Game."""
    RETURN_IMAGES = True
    MOVE_PENALTY = 1
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 100
    OBSERVATION_SPACE_VALUES = 8
    ACTION_SPACE_SIZE = 6

    def __init__(self, screen_width, screen_height, keys):
        self.width = screen_width
        self.height = screen_height
        self.keys = keys
        self.O_BORDER = 50
        self.I_BORDER = 130
        self.walls_drawn = False
        self.inner_walls = []
        self.outer_walls = []
        self.car = None

        self.count = 0

    def create_walls(self):
        walls = []
        if len(self.outer_walls) < 5:
            self.outer_walls = (
                [self.O_BORDER,self.O_BORDER*4],
                [self.O_BORDER,self.height-4*self.O_BORDER],
                [2*self.O_BORDER,self.height-2*self.O_BORDER],
                [4*self.O_BORDER,self.height-self.O_BORDER],
                [self.width-4*self.O_BORDER,self.height-self.O_BORDER],
                [self.width-2*self.O_BORDER,self.height-2*self.O_BORDER],
                [self.width-self.O_BORDER,self.height-4*self.O_BORDER],
                [self.width-self.O_BORDER,4*self.O_BORDER],
                [self.width-2*self.O_BORDER,2*self.O_BORDER],
                [self.width-4*self.O_BORDER,self.O_BORDER],
                [4*self.O_BORDER,self.O_BORDER],
                [2*self.O_BORDER,2*self.O_BORDER])

        if len(self.inner_walls) < 5:
            self.inner_walls = (
                [1.25*self.I_BORDER,self.I_BORDER*2],
                [1.25*self.I_BORDER,self.height-2*self.I_BORDER],
                [1.5*self.I_BORDER,self.height-1.5*self.I_BORDER],
                [2.5*self.I_BORDER,self.height-self.I_BORDER],
                [self.width-2.5*self.I_BORDER,self.height-self.I_BORDER],
                [self.width-1.5*self.I_BORDER,self.height-1.5*self.I_BORDER],
                [self.width-1.25*self.I_BORDER,self.height-2*self.I_BORDER],
                [self.width-1.25*self.I_BORDER,2*self.I_BORDER],
                [self.width-1.5*self.I_BORDER,1.5*self.I_BORDER],
                [self.width-2.5*self.I_BORDER,self.I_BORDER],
                [2.5*self.I_BORDER,self.I_BORDER],
                [1.5*self.I_BORDER,1.5*self.I_BORDER])

        for i in range(len(self.outer_walls)):
            walls.append(Boundary(self.outer_walls[i-1],self.outer_walls[i]))
            walls[i].show()
        for i in range(len(self.inner_walls)):
            walls.append(Boundary(self.inner_walls[i-1],self.inner_walls[i]))
            walls[i].show()

        self.car.walls = walls

    def draw_walls(self, x, y, button):
        if self.walls_drawn == True:
            print("The walls have already been set.")
            return
        if button == mouse.LEFT:
            if self.count == 0:
                self.inner_walls.append([x,y])
                print('Inner - ''X: ', x, ', Y: ', y)
            if self.count == 1:
                self.outer_walls.append([x,y])
                print('Outer - ', 'X: ', x, ', Y: ', y)
        if button == mouse.RIGHT:
            if self.count == 0:
                print("right",self.count)
            elif self.count == 1:
                print("right",self.count)
                self.walls_drawn = True
            self.count += 1

        if self.walls_drawn == True:
            if len(self.inner_walls) < 5 and len(self.outer_walls) < 5:
                self.inner_walls = None
                self.outer_walls = None
            self.create_walls()

    def create_checkpoints(self):
        checkpoints = []
        points = (
            ((self.I_BORDER*1.25,self.height/2),(self.O_BORDER,self.height/2)),
            ((self.width-self.I_BORDER*1.25,self.height/2),(self.width-self.O_BORDER,self.height/2)),
            ((self.width/2,self.height-self.O_BORDER),(self.width/2,self.height-self.I_BORDER)),
            ((self.width/2+125,self.height-self.O_BORDER),(self.width/2+100,self.height-self.I_BORDER)),
            ((self.width/2-125,self.height-self.O_BORDER),(self.width/2-100,self.height-self.I_BORDER)),
            ((self.width/2+125,self.O_BORDER),(self.width/2+100,self.I_BORDER)),
            ((self.width/2-125,self.O_BORDER),(self.width/2-100,self.I_BORDER)),
            ((self.width/2,self.O_BORDER),(self.width/2,self.I_BORDER)))
        for i in range(len(self.inner_walls)):
            checkpoints.append(Boundary(self.inner_walls[i],self.outer_walls[i]))
        for i in range(len(points)):
            checkpoints.append(Boundary(points[i][0],points[i][1]))

        self.car.checkpoints = checkpoints

    def reset(self):
        # self.car.alive = False
        if self.car:
            self.car.delete()
        self.car = Car()
        self.create_walls()
        self.create_checkpoints()
        self.episode_step = 0

        return self.car.look()

    def step(self, action, training=False):
        self.episode_step += 1
        self.car.auto_controls(action)

        if training:
            if not self.car.alive:
                reward = -self.CRASH_PENALTY
            elif self.car.update_score():
                reward = self.CHECKPOINT_REWARD
            else:
                reward = -self.MOVE_PENALTY
        else:
            reward = 0

        done = False
        if self.car.alive == False:
            done = True
        elif training == True and self.episode_step >= 500:
            done = True
        return self.car.SPACE_STATE, reward, done
