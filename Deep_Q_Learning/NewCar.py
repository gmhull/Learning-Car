import numpy as np
import pyglet, sys, math
from pyglet.gl import *
from pyglet.window import key

car_img = pyglet.resource.image("Car.JPG")
car_img.anchor_x = car_img.width/2
car_img.anchor_y = car_img.height/2

class Car(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(img=car_img, *args, **kwargs)
        self.x, self.y = 400, 100       # Position of the car
        self.vel_x, self.vel_y = 0, 0   # Linear velocity of the car
        self.acceleration = 8           # Linear acceleration of the car
        self.drag = 0.95                 # How fast the car will slow down
        self.rotation = 0               # Angle of the car
        self.angular_vel = 0            # Speed that the car is rotating
        self.turn_speed = 1.7           # How quickly the car can turn
        self.angular_drag = 0.8         # How fast the car will stop spinning

        self.FORWARDS = False            #
        self.BACKWARDS = False            #
        self.LEFT    = False            #
        self.RIGHT   = False            #
        self.dir = 1

        self.walls = None               # Initialize the walls variable.  This is set in the game function when the walls are created
        self.checkpoints = None         # Initialize the checkpoints variable.  This is set in the game function when the checkpoints are created
        self.checkpoints_collected = []
        self.reward = 0

        self.color = (255,0,255)        # Set the color of the car
        self.alive = True

        self.rays = []
        for angle in [-40,-20,0,20,40]:
            self.rays.append(Ray((self.x,self.y),angle-90))

    def __str__(self):
        return f"{self.x}, {self.y}"

    def player_control(self, keys):
        pt = self.check_collision(self.walls)
        if pt:
            self.alive = False
        ob = self.check_collision(self.checkpoints)
        if ob:
            self.update_score()

        # This controls the physics of the car
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x *= self.drag
        self.vel_y *= self.drag
        self.rotation += self.angular_vel
        self.angular_vel *= self.angular_drag

        speed = np.sqrt(np.square(self.vel_x)+np.square(self.vel_y))

        if keys[key.W]:
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle = -math.radians(self.rotation)

            self.vel_x = math.cos(angle) * self.acceleration
            self.vel_y = math.sin(angle) * self.acceleration

            self.dir = 1
        if keys[key.A] and self.dir == 1:
            self.angular_vel -= self.turn_speed * speed / (self.acceleration * self.drag)
        if keys[key.D] and self.dir == 1:
            self.angular_vel += self.turn_speed * speed / (self.acceleration * self.drag)
        if keys[key.S]:
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle = -math.radians(self.rotation)

            self.vel_x = math.cos(angle) * -self.acceleration
            self.vel_y = math.sin(angle) * -self.acceleration

            self.dir = -1
        if keys[key.A] and self.dir == -1:
            self.angular_vel += self.turn_speed * speed / (self.acceleration * self.drag)
        if keys[key.D] and self.dir == -1:
            self.angular_vel -= self.turn_speed * speed / (self.acceleration * self.drag)
        if keys[key.E]:
            print('Howdy')

        self.check_bounds()

    def auto_controls(self, action):
        self.FORWARDS  = False
        self.BACKWARDS = False
        self.LEFT      = False
        self.RIGHT     = False

        if action == 0:
            self.FORWARDS = True
        elif action == 1:
            pass
            # self.BACKWARDS = True
        elif action == 2:
            if self.vel_x == 0 and self.vel_y == 0:
                self.FORWARDS = True
            self.LEFT = True
        elif action == 3:
            if self.vel_x == 0 and self.vel_y == 0:
                self.FORWARDS = True
            self.RIGHT = True
        elif action == 4:
            self.FORWARDS = True
            self.LEFT = True
        elif action == 5:
            self.FORWARDS = True
            self.RIGHT = True
        # elif action == 6:
        #     self.BACKWARDS = True
        #     self.LEFT = True
        # elif action == 7:
        #     self.BACKWARDS = True
        #     self.RIGHT = True
        # elif action == 8:
        #     pass

        self.move()
        self.look()
        object = self.check_collision(self.walls)
        if object:
            self.alive = False

    def move(self):
        # This controls the physics of the car
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x *= self.drag
        self.vel_y *= self.drag
        self.rotation += self.angular_vel
        self.angular_vel *= self.angular_drag

        speed = np.sqrt(np.square(self.vel_x)+np.square(self.vel_y))

        if self.FORWARDS == True:
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle = -math.radians(self.rotation)

            self.vel_x = math.cos(angle) * self.acceleration
            self.vel_y = math.sin(angle) * self.acceleration

            self.dir = 1
        if self.LEFT == True and self.dir == 1:
            self.angular_vel -= self.turn_speed * speed / (self.acceleration * self.drag)
        if self.RIGHT == True and self.dir == 1:
            self.angular_vel += self.turn_speed * speed / (self.acceleration * self.drag)
        if self.BACKWARDS == True:
            # Note: pyglet's rotation attributes are in "negative degrees"
            angle = -math.radians(self.rotation)

            self.vel_x = math.cos(angle) * -self.acceleration
            self.vel_y = math.sin(angle) * -self.acceleration

            self.dir = -1
        if self.LEFT == True and self.dir == -1:
            self.angular_vel += self.turn_speed * speed / (self.acceleration * self.drag)
        if self.RIGHT == True and self.dir == -1:
            self.angular_vel -= self.turn_speed * speed / (self.acceleration * self.drag)

        self.check_bounds()

    def check_bounds(self):
        global width, height
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 1400 + self.image.width / 2 # Need to set this width to be equal to the screen width
        max_y = 700 + self.image.height / 2
        if self.x < min_x: self.x = max_x
        if self.x > max_x: self.x = min_x
        if self.y < min_y: self.y = max_y
        if self.y > max_y: self.y = min_y

    def look(self):
        FURTHEST_CHECK = 300
        self.SPACE_STATE = []
        for ray in self.rays:
            ray.pos = (self.x, self.y)
            ray.update_angle(math.radians(self.rotation))
            CLOSEST_WALL = FURTHEST_CHECK
            for wall in self.walls:
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
            self.SPACE_STATE.append(CLOSEST_WALL / FURTHEST_CHECK)
        self.SPACE_STATE.append(self.vel_x)
        self.SPACE_STATE.append(self.vel_y)
        self.SPACE_STATE.append(self.angular_vel)
        return self.SPACE_STATE

    def check_collision(self, obstacles):
        if obstacles == None:
            return

        pt_found = False
        for wall in obstacles:
            if pt_found: break
            x1 = wall.a[0]
            y1 = wall.a[1]
            x2 = wall.b[0]
            y2 = wall.b[1]
            hypot = math.hypot(self.width/2,self.height/2)
            angle = math.radians(self.rotation)
            tan = math.atan(self.width/self.height)
            for i in ([hypot*math.sin(angle+tan), hypot*math.cos(angle+tan), hypot*math.sin(angle-tan), hypot*math.cos(angle-tan)],
                      [hypot*math.sin(angle-tan), hypot*math.cos(angle-tan), hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi)],
                      [hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi), hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi)],
                      [hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi), hypot*math.sin(angle+tan), hypot*math.cos(angle+tan)]):
                x3 = self.x + i[0]
                y3 = self.y + i[1]
                x4 = self.x + i[2]
                y4 = self.y + i[3]

                den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
                if den == 0:
                    continue
                t =  ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
                u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den
                if t > 0 and t < 1 and u > 0 and u < 1:
                    pt = [0,0]
                    pt[0] = int(x1 + t * (x2 - x1))
                    pt[1] = int(y1 + t * (y2 - y1))
                    pt_found = True
                    return wall # , 'pt' if you want the specific point
                else:
                    continue

    def show_outline(self):
        hypot = math.hypot(self.width/2,self.height/2)
        angle = math.radians(self.rotation)
        tan = math.atan(self.width/self.height)
        for i in ([hypot*math.sin(angle+tan), hypot*math.cos(angle+tan), hypot*math.sin(angle-tan), hypot*math.cos(angle-tan)],
                  [hypot*math.sin(angle-tan), hypot*math.cos(angle-tan), hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi)],
                  [hypot*math.sin(angle+tan-math.pi), hypot*math.cos(angle+tan-math.pi), hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi)],
                  [hypot*math.sin(angle-tan+math.pi), hypot*math.cos(angle-tan+math.pi), hypot*math.sin(angle+tan), hypot*math.cos(angle+tan)]):
            x3 = self.x + i[0]
            y3 = self.y + i[1]
            x4 = self.x + i[2]
            y4 = self.y + i[3]
            pyglet.graphics.draw(2, GL_LINES, ('v2f', (x3, y3, x4, y4)))

    def show_walls(self):
        for wall in self.walls:
            wall.show()

    def show_checkpoints(self):
        if self.checkpoints:
            for wall in self.checkpoints:
                wall.show()

    def update_score(self):
        gate = self.check_collision(self.checkpoints)
        if gate not in self.checkpoints_collected:
            self.checkpoints_collected.append(gate)
            # self.reward += 100
            if len(self.checkpoints_collected) == 20:
                self.checkpoints_collected = []
            return True
        return False

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
