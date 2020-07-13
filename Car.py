import numpy as np
import pyglet, sys, math
from pyglet.gl import *
from pyglet.window import key
import NeuralNetwork as NN

car_img = pyglet.resource.image("Car.JPG")
car_img.anchor_x = car_img.width/2
car_img.anchor_y = car_img.height/2

class Car(pyglet.sprite.Sprite):
    def __init__(self,*args, **kwargs):
        super().__init__(img=car_img, *args, **kwargs)
        self.x, self.y = 500, 85
        self.vel_x, self.vel_y = 0, 0
        self.acc = 200
        self.speed = 0
        self.turn_speed = 150

        self.DISTANCES = [1,1,1,1,1] # Temporary Fix. Must come before update
        self.color = (255,0,255)

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.score = 0
        self.genes = []
        self.checkpoints = []
        self.alive = True

        # self.Net = None

        self.rays = []
        for angle in [-40,-20,0,20,40]:
            self.rays.append(Ray((self.x,self.y),angle-90))

    def update(self, dt):
        if self.alive == False:
            return

        # turn_rate = self.Net.feed_forward(self.DISTANCES)
        turn_rate = NN.feed_forward(self.genes, self.DISTANCES)
        # print("rate", turn_rate)
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

    def look(self, walls):
        FURTHEST_CHECK = 400
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
            # ray.show(CLOSEST_POINT)
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
            self.score += 1
            # print(len(self.checkpoints))
        if len(self.checkpoints) == 20:
            self.checkpoints = []
            # self.score += 20
        if self.score >= 29:
            self.alive = False

    def get_genes(self, nodes, genes=None):
        if genes == None:
            self.rand_genes(nodes)
        else:
            self.genes = genes
        self.alive = True
        # self.Net = NN.NeuralNet(self.genes, [1,1,1,1,1])
        # self.Net = NN.feed_forward(self.genes, [1,1,1,1,1]) # Fix this

    def rand_genes(self, nodes):
        self.genes = []
        weights = []
        biases = []
        # Weights
        for layer in range(len(nodes)-1):
            w = []
            for node1 in range(nodes[layer]):
                for node2 in range(nodes[layer+1]):
                    w.append(np.random.random()*10-5)
            weights.append(w)
        self.genes.append(weights)
        # Biases
        for i in nodes[1:]: # Should this only go until -1?
            b = []
            for node in range(i):
                b.append(np.random.random()*10-5)
            biases.append(b)
        self.genes.append(biases)
        print("Genes Created", self.genes)


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
