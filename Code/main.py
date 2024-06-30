import pygame as pg,sys
from pygame.locals import *
import pygame.gfxdraw
import time
import aStar
import asyncio
import random
import time
from pygame.math import Vector2
import math

#initialize global variables
width = 924
height = 1024
black = (50, 50, 50)
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height),0,32)
pg.display.set_caption("Maze")
screen.fill(black)
NODES = []
WEIGHT = []
N = 39
START = None
END = None


button = pg.image.load('data/image/PathFind.png')
button = pg.transform.scale(button, (130,60))
button2 = pg.image.load('data/image/PathMaze.png')
button2 = pg.transform.scale(button2, (130,60))
button3 = pg.image.load('data/image/GenerateMaze.png')
button3 = pg.transform.scale(button3, (130,60))
screen.fill(black)
selection = screen.blit(button,(10,945))
selection2 = screen.blit(button2,(785,945))
selection3 = screen.blit(button3,(390,945))
pygame.draw.rect(screen, (0,0,0), (0, width - 2, width, 5))

async def main():
    generateMaze()
    global WEIGHT
    global NODES
    global N
    global START
    global END
    start = False
    path = []
    while(True):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x,y = pg.mouse.get_pos()
                if selection.collidepoint(x,y):
                    path.clear()
                    try:
                        ai = aStar
                        clist = ai.populateCities(NODES, WEIGHT)
                        t,s = ai.aSearch([clist[START[0]], 0], clist, NODES[END[0]])
                        for i in t:
                            pygame.draw.rect(screen, (0,255,0), ((width/N*i[0].coord[1]) + ((width/N)-2)/4,(width/N*i[0].coord[0]) + ((width/N)-2)/4,((width/N)-2)/2,((width/N)-2)/2))
                            path.append(((width/N*i[0].coord[1]) + ((width/N)-2)/4,(width/N*i[0].coord[0]) + ((width/N)-2)/4,((width/N)-2)/2,((width/N)-2)/2))
                    except:
                        pygame.draw.rect(screen, black, (0, width, width, height-width))
                        font = pygame.font.Font('freesansbold.ttf', 32)
                        text = font.render('No Path Found', True, (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (width / 2, 980)
                        screen.blit(text, textRect)
                        pg.display.update()        
                        await asyncio.sleep(0)
                        time.sleep(2)
                        pygame.draw.rect(screen, black, (0, width, width, height-width))
                        screen.blit(button,(10,945))
                        screen.blit(button2,(785,945))
                        screen.blit(button3,(390,945))
                        pygame.draw.rect(screen, (0,0,0), (0, width - 2, width, 5))
                elif selection2.collidepoint(x,y):
                    path.clear()
                    await generateValidMaze()
                elif selection3.collidepoint(x,y):
                    path.clear()
                    generateMaze()
                elif not start:
                    prev = START
                    START = findNode(math.trunc(x/(width/N)), math.trunc(y/(width/N)))
                    if START is not None:
                        for spot in path:
                            pygame.draw.rect(screen, (255,0,0), spot)
                        path.clear()
                        pygame.draw.rect(screen, (255,0,0), (width/N*prev[1][1],width/N*prev[1][0],(width/N)-2,(width/N)-2))
                        pygame.draw.rect(screen, (255,0,255), ((math.trunc(x/(width/N)))*(width/N),(math.trunc(y/(width/N)))*(width/N),(width/N)-2,(width/N)-2))
                        start = True
                else:
                    prev = END
                    END = findNode(math.trunc(x/(width/N)), math.trunc(y/(width/N)))
                    if END is not None:
                        for spot in path:
                            pygame.draw.rect(screen, (255,0,0), spot)
                        path.clear()
                        pygame.draw.rect(screen, (255,0,0), (width/N*prev[1][1],width/N*prev[1][0],(width/N)-2,(width/N)-2))
                        pygame.draw.rect(screen, (0,0,255), ((math.trunc(x/(width/N)))*(width/N),(math.trunc(y/(width/N)))*(width/N),(width/N)-2,(width/N)-2))
                        start = False
                
                await asyncio.sleep(0)
                pygame.event.clear()

        pg.display.update()
        await asyncio.sleep(0)
        CLOCK.tick(fps)

def findNode(x,y):
    for i in NODES:
        if i[1] == [y,x]:
            return i
        
def generateMaze():
    global NODES
    global N
    global WEIGHT
    global START
    global END
    screen.fill(black)
    screen.blit(button,(10,945))
    screen.blit(button2,(785,945))
    screen.blit(button3,(390,945))
    pygame.draw.rect(screen, (0,0,0), (0, width - 2, width, 5))
    NODES = []
    WEIGHT = []
    maze = []
    count = 0
    for i in range(N):
        new = []
        for j in range(N):
            max = 1
            if j > 0 and i > 0 and (new[j-1] == 1 or maze[i-1][j] == 1):
                max = 2
            if random.randint(0,max) >= 1 or (j == 0 and i == 0) or (j == N-1 and i == N-1):
                pygame.draw.rect(screen, (255,0,0), (width/N*i,width/N*j,(width/N)-2,(width/N)-2))
                NODES.append([count, [j,i]])
                if j == N-1 and i == N-1:
                    END = NODES[len(NODES) - 1]
                if j == 0 and i == 0:
                    START = NODES[len(NODES) - 1]
                WEIGHT.append([])
                for k in range(len(WEIGHT)):
                    if k != len(WEIGHT) - 1:
                        if NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] and NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] - 1 or NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] and NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] - 1:
                            WEIGHT[k].append(1)
                        else:
                            WEIGHT[k].append(0)
                    if NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] and NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] - 1 or NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] and NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] - 1:
                        WEIGHT[len(WEIGHT) - 1].append(1)
                    else:
                        WEIGHT[len(WEIGHT) - 1].append(0)
                count += 1
            new.append(random.randint(0,1))
        maze.append(new)
            
    
    pygame.draw.rect(screen, (255,0,255), (0,0,(width/N)-2,(width/N)-2))
    pygame.draw.rect(screen, (0,0,255), (width/N*(N-1),width/N*(N-1),(width/N)-2,(width/N)-2))

async def generateValidMaze():
    global NODES
    global N
    global WEIGHT
    global START
    global END
    t = None
    while t is None:
        try:
            screen.fill(black)
            screen.blit(button,(10,945))
            screen.blit(button2,(785,945))
            screen.blit(button3,(390,945))
            pygame.draw.rect(screen, (0,0,0), (0, width - 2, width, 5))
            NODES = []
            WEIGHT = []
            maze = []
            count = 0
            for i in range(N):
                new = []
                for j in range(N):
                    max = 1
                    if j > 0 and i > 0 and (new[j-1] == 1 or maze[i-1][j] == 1):
                        max = 2
                    if random.randint(0,max) >= 1 or (j == 0 and i == 0) or (j == N-1 and i == N-1):
                        pygame.draw.rect(screen, (255,0,0), (width/N*i,width/N*j,(width/N)-2,(width/N)-2))
                        NODES.append([count, [j,i]])
                        if j == N-1 and i == N-1:
                            END = NODES[len(NODES) - 1]
                        if j == 0 and i == 0:
                            START = NODES[len(NODES) - 1]
                        WEIGHT.append([])
                        for k in range(len(WEIGHT)):
                            if k != len(WEIGHT) - 1:
                                if NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] and NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] - 1 or NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] and NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] - 1:
                                    WEIGHT[k].append(1)
                                else:
                                    WEIGHT[k].append(0)
                            if NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] and NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] - 1 or NODES[k][1][1] == NODES[len(WEIGHT) - 1][1][1] and NODES[k][1][0] == NODES[len(WEIGHT) - 1][1][0] - 1:
                                WEIGHT[len(WEIGHT) - 1].append(1)
                            else:
                                WEIGHT[len(WEIGHT) - 1].append(0)
                        count += 1
                    new.append(random.randint(0,1))
                maze.append(new)
                    
            
            pygame.draw.rect(screen, (255,0,255), (0,0,(width/N)-2,(width/N)-2))
            pygame.draw.rect(screen, (0,0,255), (width/N*(N-1),width/N*(N-1),(width/N)-2,(width/N)-2))
            pg.display.update()
            await asyncio.sleep(0)
            ai = aStar
            clist = ai.populateCities(NODES, WEIGHT)
            t,s = ai.aSearch([clist[START[0]], 0], clist, NODES[END[0]])
        except:
            pass

asyncio.run(main())