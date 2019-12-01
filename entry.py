import pygame, sys

import random
from math import sin, cos

import vmath
import collision

from tetromino import Tetromino
from tetromino import Tetrominoes
from tetromino import SPAWN_EVENT

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
            if (timeSiceLastMove > 500):
                tetro.drop(borderLineHeight)
                timeSiceLastMove = 0
            else:
                timeSiceLastMove += clock.get_time()
        #for rect in tetro.rects:
            #pygame.draw.rect(screen, (0, 0, 255), rect)
        #print(tetro.cx, tetro.cy, sep=" , ")
        for polygon in tetro.polygons:
            pygame.draw.polygon(screen, tetro.color, polygon.points)
        pygame.draw.circle(screen, (255, 0, 0), (tetro.rotationPoint.posX, tetro.rotationPoint.posY), 4)
    pygame.draw.line(screen, (255, 255, 255), (0, borderLineHeight), (width, borderLineHeight)) 
    pygame.display.flip()
    clock.tick(60)
    pass

def spawn():
    global CurrentTetro
    CurrentTetro = Tetromino(Tetrominoes(random.randrange(1, 3)), SPAWN_POS, tetrominoesOnScreen)
    tetrominoesOnScreen.append(CurrentTetro)
    

def rotateKeyPressed():
    global CurrentTetro
    CurrentTetro.rotate()


# -1 for left, 1 for right
def moveKeyPressed(direction):
    global CurrentTetro
    CurrentTetro.move(direction)
    pass

spawn()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rotateKeyPressed()
            elif event.key == pygame.K_a:
                moveKeyPressed(-1)
            elif event.key == pygame.K_d:
                moveKeyPressed(1)
        elif event.type == SPAWN_EVENT:
            print("SPAWN!!!!")
            spawn()
    render()
    
