import pyglet
from pyglet.gl import *

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
    # outer_border = ([1,250],[1,150],[width/6,150],[width/2,250],[5*width/6,150],[width-1,150],[width-1,250])
    outer_border = ([O_BORDER,O_BORDER*4],[O_BORDER,height-4*O_BORDER],
        [2*O_BORDER,height-2*O_BORDER],[4*O_BORDER,height-O_BORDER],
        [width-4*O_BORDER,height-O_BORDER],[width-2*O_BORDER,height-2*O_BORDER],
        [width-O_BORDER,height-4*O_BORDER],[width-O_BORDER,4*O_BORDER],
        [width-2*O_BORDER,2*O_BORDER],[width-4*O_BORDER,O_BORDER],
        [4*O_BORDER,O_BORDER],[2*O_BORDER,2*O_BORDER])
    for i in range(len(outer_border)):
        walls.append(Boundary(outer_border[i-1],outer_border[i]))
    # inner_border = ([1,1],[width/6,1],[width/2,100],[5*width/6,1],[width-1,1])
    inner_border = ([1.25*I_BORDER,I_BORDER*2],[1.25*I_BORDER,height-2*I_BORDER],
        [1.5*I_BORDER,height-1.5*I_BORDER],[2.5*I_BORDER,height-I_BORDER],
        [width-2.5*I_BORDER,height-I_BORDER],[width-1.5*I_BORDER,height-1.5*I_BORDER],
        [width-1.25*I_BORDER,height-2*I_BORDER],[width-1.25*I_BORDER,2*I_BORDER],
        [width-1.5*I_BORDER,1.5*I_BORDER],[width-2.5*I_BORDER,I_BORDER],
        [2.5*I_BORDER,I_BORDER],[1.5*I_BORDER,1.5*I_BORDER])
    for i in range(len(inner_border)):
        walls.append(Boundary(inner_border[i-1],inner_border[i]))
        # print(i)

    checkpoints = []
    # points = (((10,1),(10,height-1)),
    #     ((50,1),(50,height-1)),
    #     ((100,1),(100,height-1)),
    #     ((150,1),(150,height-1)),
    #     ((200,1),(200,height-1)),
    #     ((250,1),(250,height-1)),
    #     ((300,1),(300,height-1)),
    #     ((350,1),(350,height-1)),
    #     ((400,1),(400,height-1)),
    #     ((450,1),(450,height-1)),
    #     ((500,1),(500,height-1)),
    #     ((550,1),(550,height-1)),
    #     ((600,1),(600,height-1)),
    #     ((650,1),(650,height-1)),
    #     ((700,1),(700,height-1)),
    #     ((750,1),(750,height-1)),
    #     ((800,1),(800,height-1)),
    #     ((850,1),(850,height-1)),
    #     ((900,1),(900,height-1)))
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
