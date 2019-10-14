import pygame, sys
from enum import Enum

import random
from math import sin, cos

size = width, height = 420, 640

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
rect = pygame.Rect(0, 0, 100, 60)

# line below whitch we desiplay info and shit. blocks should not pass this line. 
borderLineHeight = height-100

SPAWN_POS = (width/2, 0)

## TETRONIMONES SIZES
BLOCK_SIZE = 20 ## Square. Change this to upsacle?

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

        if shape == Tetrominoes.I:
            self.points = [
                (SPAWN_POS[0]-((4*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((4*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((4*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]-((4*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
            ]
            self.cx = SPAWN_POS[0]
            self.cy = SPAWN_POS[1]+(BLOCK_SIZE/2)
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
                (SPAWN_POS[0]-((3*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((3*BLOCK_SIZE)/2), SPAWN_POS[1]),
                (SPAWN_POS[0]+((3*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]+((1*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]+((1*BLOCK_SIZE)/2), SPAWN_POS[1]+2*BLOCK_SIZE),
                (SPAWN_POS[0]-((1*BLOCK_SIZE)/2), SPAWN_POS[1]+2*BLOCK_SIZE),
                (SPAWN_POS[0]-((1*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
                (SPAWN_POS[0]-((3*BLOCK_SIZE)/2), SPAWN_POS[1]+BLOCK_SIZE),
            ]
            self.cx = SPAWN_POS[0]
            self.cy = abs(SPAWN_POS[1]-(SPAWN_POS[1]+2*BLOCK_SIZE))/2
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
    def move(self):
        if self.stuck: return
        moveBy = 20
        otherTetrosOnScreen = list(filter(lambda tetro: tetro!=self, tetrominoesOnScreen))

        for point in self.points: 
            heightTillBorder = abs(borderLineHeight - point[1])
            if heightTillBorder < 20:
                moveBy = heightTillBorder
                if heightTillBorder == 0:
                    self.stuck = True
                    ## DEBUG: spawn a new tetro
                    #tetrominoesOnScreen.append(Tetromino(Tetrominoes(random.randrange(6)+1)))
                    tetrominoesOnScreen.append(Tetromino(Tetrominoes.I))
                    break
        self.points = list(map(lambda point: (point[0], point[1] + moveBy), self.points))
        self.cy += moveBy
        
    def rotate(self):
        self.points = list(map(lambda point: (-(point[1] - self.cy) + self.cx , (point[0] - self.cx) +self.cy), self.points))



tetrominoesOnScreen = []

timeSiceLastMove = 0
def render():
    global timeSiceLastMove
    screen.fill((0, 0, 0))
    for tetro in tetrominoesOnScreen:
        if not tetro.stuck: 
            if (timeSiceLastMove > 1500):
                tetro.move()
                timeSiceLastMove = 0
                print(timeSiceLastMove)
            else:
                timeSiceLastMove += clock.get_time()
                print(timeSiceLastMove)
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
    for tetro in tetrominoesOnScreen:
        if tetro.stuck: pass
        else:
            tetro.rotate()
            #print(tetro.cx)
            #print(tetro.cy)
            break

#I = Tetromino(Tetrominoes(random.randrange(6)+1))
I = Tetromino(Tetrominoes.T)



tetrominoesOnScreen.append(I)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rotateKeyPressed()
    render()
    