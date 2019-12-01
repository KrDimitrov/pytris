from enum import Enum
from math import inf

from pygame import event
from pygame import USEREVENT

# TODO choose where to handle collisio n!
import collision
from geometry import Polygon
from vmath import Vector
# An Enum of all Valid Tetromino shapes
class Tetrominoes(Enum):
    I = 1
    O = 3
    T = 2
    J = 4
    L = 5
    S = 6
    Z = 7

SPAWN_EVENT = USEREVENT+1

BLOCK_SIZE=30

# Tetrominoes are sometimes concave polygons
# which means, we need to split them into convex polygons, 
# so that your collision works!
class Tetromino:
    def __init__(self, shape, SPAWN_POS, otherTetrosOnScreen):
        self.otherTetrosOnScreen = otherTetrosOnScreen
        self.stuck = False
        self.vecs = []

        if shape == Tetrominoes.I:
            # should spawn position be the center?
            self.polygons = [Polygon(((SPAWN_POS[0]-2*BLOCK_SIZE), SPAWN_POS[1]), ((4*BLOCK_SIZE), BLOCK_SIZE))]

            self.rotationPoint = Vector(*SPAWN_POS)
            self.color = (173, 216, 230)
            
        elif shape == Tetrominoes.O:
            self.polygons = [Polygon((SPAWN_POS[0]-1*BLOCK_SIZE, SPAWN_POS[1]), (2*BLOCK_SIZE, 2*BLOCK_SIZE))]
            self.rotationPoint = Vector(SPAWN_POS[0], SPAWN_POS[1]+BLOCK_SIZE)
            self.color = (255,255,0)
        elif shape == Tetrominoes.T:
            # SORRY ! had to be
            SPAWN_POS = (SPAWN_POS[0]-BLOCK_SIZE*2, SPAWN_POS[1])
            self.polygons = [
                    Polygon(SPAWN_POS, (BLOCK_SIZE, BLOCK_SIZE)),
                    Polygon((SPAWN_POS[0]-BLOCK_SIZE, SPAWN_POS[1]+BLOCK_SIZE), (3*BLOCK_SIZE, BLOCK_SIZE))
            ]
    
            self.rotationPoint = Vector(*SPAWN_POS) + Vector(int(BLOCK_SIZE/2), int(BLOCK_SIZE/2))
            self.color = (128,0,128)

        elif shape == Tetrominoes.J:
            self.rects = [pygame.Rect(SPAWN_POS[0]-((3*BLOCK_SIZE)/2), SPAWN_POS[1], 3*BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(SPAWN_POS[0]+((1*BLOCK_SIZE)/2), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)]
        elif shape == Tetrominoes.L:
            self.rects = [pygame.Rect(SPAWN_POS[0]-((3*BLOCK_SIZE)/2), SPAWN_POS[1], 3*BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(SPAWN_POS[0]-((3*BLOCK_SIZE)/2), BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)]
        elif shape == Tetrominoes.S:
            self.rects = [pygame.Rect(SPAWN_POS[0]-((BLOCK_SIZE)/2), SPAWN_POS[1], 2*BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(SPAWN_POS[0]-(3*BLOCK_SIZE)/2, BLOCK_SIZE, 2*BLOCK_SIZE, BLOCK_SIZE)]
        elif shape == Tetrominoes.Z:
            self.rects = [pygame.Rect(SPAWN_POS[0]-(3*BLOCK_SIZE)/2, SPAWN_POS[1], 2*BLOCK_SIZE, BLOCK_SIZE),
            pygame.Rect(SPAWN_POS[0]-((BLOCK_SIZE)/2), BLOCK_SIZE, 2*BLOCK_SIZE, BLOCK_SIZE)]
        else:
            print("WHAT THE FUCK? INVALID TETROMINO!!!")
            raise Exception("INVALID TETROMINO SHAPE")
        
        #if len(self.rects) == 1:
            #self.WIDTH = self.rects[0].width
            #self.HEIGHT = self.rects[0].height
            ##self.cx = self.rects[0].x + (self.rects[0].width/2)
            #self.cy = self.rects[0].y + (self.rects[0].height/2)
        #else:
            #urect = self.rects[0].copy()
            #for i in range(1, len(self.rects)):
            #    urect.union_ip(self.rects[i])
            #self.WIDTH = urect.width
            #self.HEIGHT = urect.height
            #self.cx = urect.x + (urect.width/2)
            #self.cy = urect.y + (urect.height/2)
        #print(self.WIDTH)
        #print(self.HEIGHT)

    ## moves the tetro one tick down
    def drop(self, borderLineHeight):
        # TODO add a fast drop function...
        if self.stuck: return
        vector = Vector(0, BLOCK_SIZE)

        for polygon in self.polygons:
            polygon.move(vector) 

        
        self.rotationPoint += vector 

        # TODO find a better solution to this. we cant use infinity
        linePoints = [(-100, borderLineHeight), (10000, borderLineHeight)]
        for polygon in self.polygons:
            for point in polygon.points:
                pVec = Vector(*point)
                lVec = Vector(0, borderLineHeight)
                delta = pVec - lVec
                if abs(delta.posY)==0:
                    self.stuck = True
        # TODO fix unessecery filter
        otherTetros = list(filter(lambda tetro: tetro != self, self.otherTetrosOnScreen))
        print(otherTetros)
        for otherTetro in otherTetros:
            if collision.checkCollision(self, otherTetro):
                self.stuck = True
        if self.stuck: 
            event.post(event.Event(SPAWN_EVENT))

    def move(self,direction):
        vector = Vector(BLOCK_SIZE*direction, 0)
        for polygon in self.polygons:
            polygon.move(vector)
        self.rotationPoint += vector 

    def rotate(self):
        for polygon in self.polygons:
            polygon.rotate((self.rotationPoint.posX, self.rotationPoint.posY))

    # does this make sense? or should we spawn tetros in the constructor?
    # spawning means the player takes controll over the movement
    # TODO add RNG
    @staticmethod
    def spawn(SPAWN_POS, tetrominoesOnScreen):
        tetro = Tetromino(Tetrominoes.I, SPAWN_POS, tetrominoesOnScreen.copy())
        tetrominoesOnScreen.append(tetro)
