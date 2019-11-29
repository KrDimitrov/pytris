import pygame, sys
from enum import Enum

import random
from math import sin, cos

import vmath
import collision
# 21x10
pygame.init()

## TETRONIMONES SIZES
BLOCK_SIZE = 30 ## Square. Change this to upsacle?
GRID_COLOR = (82, 78, 78)
size = width, height = 10*BLOCK_SIZE, (21*BLOCK_SIZE)+100
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
rect = pygame.Rect(0, 0, 100, 60)

# line below whitch we desiplay info and shit. blocks should not pass this line. 
borderLineHeight = height-100

SPAWN_POS = (5*BLOCK_SIZE, 0)

# Points to the current moving Tetromino
CurrentTetro = None

class Tetrominoes(Enum):
    I = 1
    O = 2
    T = 3
    J = 4
    L = 5
    S = 6
    Z = 7


class Tetromino:
    S = sin(90)
    C = cos(90)
    def __init__(self, shape):
        self.stuck = False
        self.vecs = []

        if shape == Tetrominoes.I:
            self.points = [
                (SPAWN_POS[0]-((4*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((4*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((4*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]-((4*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
            ]
            self.cx = SPAWN_POS[0]
            self.cy = SPAWN_POS[1]
        elif shape == Tetrominoes.O:
            self.points = [
                (SPAWN_POS[0]-((2*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((2*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((2*BLOCK_SIZE)/2), SPAWN_POS[1]+(2*BLOCK_SIZE)),
                (SPAWN_POS[0]-((2*BLOCK_SIZE)/2), SPAWN_POS[1]+(2*BLOCK_SIZE)),
            ]
            self.cx = SPAWN_POS[0]
            self.cy = SPAWN_POS[1]+(BLOCK_SIZE)
        elif shape == Tetrominoes.T:
            self.points = [
                (SPAWN_POS[0]-((2*BLOCK_SIZE)), SPAWN_POS[1]),
                (SPAWN_POS[0]+((1*BLOCK_SIZE)), SPAWN_POS[1]),
                (SPAWN_POS[0]+((1*BLOCK_SIZE)), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0], SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0], SPAWN_POS[1]+2*BLOCK_SIZE),
                (SPAWN_POS[0]-(1*BLOCK_SIZE), SPAWN_POS[1]+2*BLOCK_SIZE),
                (SPAWN_POS[0]-(1*BLOCK_SIZE), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]-(2*BLOCK_SIZE), SPAWN_POS[1]+BLOCK_SIZE),

            ]
            self.cx = SPAWN_POS[0]-(BLOCK_SIZE/2)
            self.cy = SPAWN_POS[1]+(BLOCK_SIZE/2)
            #self.cy = abs(SPAWN_POS[1]-(SPAWN_POS[1]+2*BLOCK_SIZE))/2
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
    def drop(self):
        # TODO add a fast drop function...
        if self.stuck: return
        moveBy = BLOCK_SIZE
        otherTetrosOnScreen = list(filter(lambda tetro: tetro!=self, tetrominoesOnScreen))

        for point in self.points: 
            heightTillBorder = abs(borderLineHeight - point[1])
            if heightTillBorder < 20:
                moveBy = heightTillBorder
                if heightTillBorder == 0:
                    self.stuck = True
                    Tetromino.spawn()
                    break
        self.points = list(map(lambda point: (point[0], point[1] + moveBy), self.points))
        
        self.cy += moveBy
        
        for otherTetro in otherTetrosOnScreen:
            if collision.checkCollision(self.points, otherTetro.points):
                print("COLLISIONNEN")
                self.stuck = True
                Tetromino.spawn()
    def rotate(self):
        newpoints = list(map(lambda point: (-(point[1] - self.cy) + self.cx , (point[0] - self.cx) +self.cy), self.points))
        #print(newpoints)
        #newpoints = list(map(lambda point: (round(point[0]/BLOCK_SIZE)*BLOCK_SIZE, round(point[1]/BLOCK_SIZE)*BLOCK_SIZE), newpoints))
       # print(newpoints)
        otherTetrosOnScreen = list(filter(lambda tetro: tetro!=self, tetrominoesOnScreen))
        
        for otherTetro in otherTetrosOnScreen:
            if collision.checkCollision(newpoints, otherTetro.points):
                return
        self.points = newpoints

    # does this make sense? or should we spawn tetros in the constructor?
    # spawning means the player takes controll over the movement
    # TODO add RNG
    @staticmethod
    def spawn():
        global CurrentTetro
        tetro = Tetromino(Tetrominoes.I)
        CurrentTetro = tetro
        tetrominoesOnScreen.append(tetro)
        


tetrominoesOnScreen = []

timeSiceLastMove = 0
def render():
    global timeSiceLastMove
    screen.fill((0, 0, 0))

    # draw grid
    for i in range(0, width, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (i, 0), (i, borderLineHeight))
    for i in range(0, borderLineHeight, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, i), (width, i))


    # draw tetros
    for tetro in tetrominoesOnScreen:
        if not tetro.stuck: 
            if (timeSiceLastMove > 1500):
                tetro.drop()
                timeSiceLastMove = 0
            else:
                timeSiceLastMove += clock.get_time()
        #for rect in tetro.rects:
            #pygame.draw.rect(screen, (0, 0, 255), rect)
        pygame.draw.polygon(screen, (0,255,0), tetro.points)
        #print(tetro.cx, tetro.cy, sep=" , ")
        pygame.draw.circle(screen, (255, 0, 0), (int(tetro.cx), int(tetro.cy)), 4)
    pygame.draw.line(screen, (255, 255, 255), (0, borderLineHeight), (width, borderLineHeight)) 
    pygame.display.flip()
    clock.tick(60)
    pass



def rotateKeyPressed():
    global CurrentTetro
    CurrentTetro.rotate()
#I = Tetromino(Tetrominoes(random.randrange(6)+1))
I = Tetromino(Tetrominoes.T)
CurrentTetro = I


Tetromino.spawn()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rotateKeyPressed()
    render()
    
