import numpy as np
import pyglet, sys, math
from pyglet.gl import *
from pyglet.window import key
import NeuralNetwork as NN

# from Files import test

class Car(pyglet.sprite.Sprite):
    def __init__(self,*args, **kwargs):
        super().__init__(img=car_img, *args, **kwargs)
        self.vel_x, self.vel_y = 0, 0
        self.acc = 200
        self.speed = 0
        self.color = (255,0,255)
        self.turn_speed = 150
        self.colr = ('c3B',(255,0,0, 255,0,0))
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]
        self.score = 0
        self.genes = []
        self.checkpoints = []
        # self.visible = False
        self.alive = True

        self.Net = None

        self.rays = []
        for angle in [-50,-25,0,25,50]:
            self.rays.append(Ray((self.x,self.y),angle-90))

    def update(self, dt):
        if self.alive == False:
            # self.get_score()
            return

        """
        The check_walls function happens outside of this, but before this happens

        """
        turn_rate = self.Net.feed_forward(self.DISTANCES)
        self.rotation += turn_rate * self.turn_speed * dt

        angle = -math.radians(self.rotation)
        self.speed += self.acc * dt
        MAX_VEL = 200
        if self.speed > MAX_VEL: self.speed = MAX_VEL
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed


        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        self.check_bounds()

    def player_control(self):
        # For player control of the car
        if self.key_handler[key.W]:
            if self.key_handler[key.A]:
                self.rotation -= self.turn_speed * dt
            if self.key_handler[key.D]:
                self.rotation += self.turn_speed * dt
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle = -math.radians(self.rotation)
            self.speed += self.acc * dt
            MAX_VEL = 200
            if self.speed > MAX_VEL: self.speed = MAX_VEL
            self.vel_x = math.cos(angle) * self.speed
            self.vel_y = math.sin(angle) * self.speed
        elif self.key_handler[key.S]:
            self.vel_x = 0
            self.vel_y = 0
        elif self.key_handler[key.E]:
            print('Howdy')

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 1000 + self.image.width / 2
        max_y = 700 + self.image.height / 2
        if self.x < min_x: self.x = max_x
        if self.x > max_x: self.x = min_x
        if self.y < min_y: self.y = max_y
        if self.y > max_y: self.y = min_y

    def check_walls(self, walls):
        FURTHEST_CHECK = 200
        self.DISTANCES = []
        for ray in self.rays:
            ray.pos = (self.x, self.y)
            ray.update_angle(math.radians(self.rotation))
            CLOSEST_WALL = FURTHEST_CHECK
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    dist = math.dist(pt, ray.pos)
                    if dist < CLOSEST_WALL:
                        CLOSEST_WALL = dist
                        CLOSEST_POINT = pt
            if CLOSEST_WALL == FURTHEST_CHECK:
                CLOSEST_POINT = [self.x + FURTHEST_CHECK*ray.dir[0],
                                 self.y + FURTHEST_CHECK*ray.dir[1]]
            ray.show(CLOSEST_POINT)
            self.DISTANCES.append(CLOSEST_WALL / FURTHEST_CHECK)
        return self.DISTANCES

    def check_collision(self, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]
        hypot = math.hypot(self.width/2,self.height/2)
        angle = -math.radians(self.rotation)
        tan = math.atan(self.width/self.height)
        for i in ([hypot*math.sin(angle+tan), hypot*math.cos(angle+tan), hypot*math.sin(angle-tan), hypot*math.cos(angle-tan)],
                  [hypot*math.sin(angle-tan), hypot*math.cos(angle-tan), hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi)],
                  [hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi), hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi)],
                  [hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi), hypot*math.sin(angle+tan), hypot*math.cos(angle+tan)]):
            x3 = self.x + i[0]
            y3 = self.y + i[1]
            x4 = self.x + i[2]
            y4 = self.y + i[3]
            # pyglet.graphics.draw(2, GL_LINES, ('v2f', (x3, y3, x4, y4)))

            den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
            if den == 0:
                continue
            t =  ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
            u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den
            if t > 0 and t < 1 and u > 0 and u < 1:
                pt = [0,0]
                pt[0] = int(x1 + t * (x2 - x1))
                pt[1] = int(y1 + t * (y2 - y1))
                return pt
            else:
                continue

    def update_score(self, gate):
        if gate not in self.checkpoints:
            self.checkpoints.append(gate)
            # print(len(self.checkpoints))
        if len(self.checkpoints) == 20:
            self.checkpoints = []
            self.score += 20

    def get_genes(self, DNA):
        self.genes = DNA
        self.Net = NN.NeuralNet(self.genes, [1,1,1,1,1]) # Fix this
        # self.x = 500
        # self.y = 85
        # self.rotation = 0


class Ray(object):
    def __init__(self,pos,angle):
        self.pos = [pos[0],pos[1]]
        self.angle = -math.radians(angle)
        self.newAngle = 0
        self.dir = [math.sin(self.angle),math.cos(self.angle)]

    def show(self,end):
        pyglet.graphics.draw(2,GL_LINES,('v2f',(self.pos[0],self.pos[1],end[0],end[1])))

    def update_angle(self,angle):
        self.newAngle = self.angle + angle
        self.dir = [math.sin(self.newAngle),math.cos(self.newAngle)]

    def cast(self,wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]
        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if den == 0:
            return
        t =  ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den
        if t > 0 and t < 1 and u > 0:
            pt = [0,0]
            pt[0] = int(x1 + t * (x2 - x1))
            pt[1] = int(y1 + t * (y2 - y1))
            return pt
        else:
            return


class Boundary(object):
    def __init__(self,p1,p2):
        self.a = p1
        self.b = p2
    def show(self):
        pyglet.graphics.draw(2,GL_LINES,
            ('v2f',(self.a[0],self.a[1],self.b[0],self.b[1])))


def create_track(width,height):
    # This function creates the track that is driven on and creates checkpoints
    # along the track to incentivise travel.
    O_BORDER = 50
    I_BORDER = 130
    walls = []
    outer_border = ([O_BORDER,O_BORDER*4],[O_BORDER,height-4*O_BORDER],
        [2*O_BORDER,height-2*O_BORDER],[4*O_BORDER,height-O_BORDER],
        [width-4*O_BORDER,height-O_BORDER],[width-2*O_BORDER,height-2*O_BORDER],
        [width-O_BORDER,height-4*O_BORDER],[width-O_BORDER,4*O_BORDER],
        [width-2*O_BORDER,2*O_BORDER],[width-4*O_BORDER,O_BORDER],
        [4*O_BORDER,O_BORDER],[2*O_BORDER,2*O_BORDER])
    for i in range(len(outer_border)):
        walls.append(Boundary(outer_border[i-1],outer_border[i]))
    inner_border = ([1.25*I_BORDER,I_BORDER*2],[1.25*I_BORDER,height-2*I_BORDER],
        [1.5*I_BORDER,height-1.5*I_BORDER],[2.5*I_BORDER,height-I_BORDER],
        [width-2.5*I_BORDER,height-I_BORDER],[width-1.5*I_BORDER,height-1.5*I_BORDER],
        [width-1.25*I_BORDER,height-2*I_BORDER],[width-1.25*I_BORDER,2*I_BORDER],
        [width-1.5*I_BORDER,1.5*I_BORDER],[width-2.5*I_BORDER,I_BORDER],
        [2.5*I_BORDER,I_BORDER],[1.5*I_BORDER,1.5*I_BORDER])
    for i in range(len(outer_border)):
        walls.append(Boundary(inner_border[i-1],inner_border[i]))

    checkpoints = []
    points = (((I_BORDER*1.25,height/2),(O_BORDER,height/2)),
        ((width-I_BORDER*1.25,height/2),(width-O_BORDER,height/2)),
        ((width/2,height-O_BORDER),(width/2,height-I_BORDER)),
        ((width/2+125,height-O_BORDER),(width/2+100,height-I_BORDER)),
        ((width/2-125,height-O_BORDER),(width/2-100,height-I_BORDER)),
        ((width/2+125,O_BORDER),(width/2+100,I_BORDER)),
        ((width/2-125,O_BORDER),(width/2-100,I_BORDER)),
        ((width/2,O_BORDER),(width/2,I_BORDER)))
    for i in range(len(inner_border)):
        checkpoints.append(Boundary(inner_border[i],outer_border[i]))
    for i in range(len(points)):
        checkpoints.append(Boundary(points[i][0],points[i][1]))
    return walls, checkpoints

car_img = pyglet.resource.image("Car.JPG")
car_img.anchor_x = car_img.width/2
car_img.anchor_y = car_img.height/2

if __name__ == '__main__':
    width, height = 1000, 700
    game_window = pyglet.window.Window(width,height)
    walls, checkpoints = create_track(width,height)

    neuron_shape = (5,4,3,1)
    GA = NN.GeneticAlgorithm(1, 0.01)
    GA.create_population(GA.pop_size, neuron_shape)

    # car = Car(x=500,y=85)
    # for handler in car.event_handlers:
    #     game_window.push_handlers(handler)

    @game_window.event
    def on_draw():
        game_window.clear()
        # car.visible = True
        for car in GA.pop:
            for wall in walls:
                wall.show()
                pt = car[1].check_collision(wall)
                if pt: car[1].alive = False
            car[1].check_walls(walls)
            for gate in checkpoints:
                pt = car[1].check_collision(gate)
                if pt:
                    car[1].update_score(gate)
            car[1].draw()

            stopped_cars = 0
            for car in GA.pop:
                # print("Stopped Cars", stopped_cars)
                if car[1].alive == False:
                    stopped_cars += 1

                if stopped_cars == GA.pop_size:
                    GA.calc_fitness()
                    GA.evolve()

    for car in GA.pop:
        pyglet.clock.schedule_interval(car[1].update, 1 / 120.0)

    pyglet.app.run()
