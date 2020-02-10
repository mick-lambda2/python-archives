import pygame, time, random, copy
import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plot
from scipy.special import expit as activ_fn

# GLOBALS
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
grey = [220, 220, 220]
font1 = pygame.font.Font('freesansbold.ttf', 10)

class Snake:
    def __init__(self, start_x, start_y):
        self.body = [[start_x, start_y]]
        self.score = 0

    def checkCollisions(self, width, height):
        x = 5

    def updateBody(self):
        x = 5

    def updateVision(self):
        x = 5

class SnakeGame:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load("logo1.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("PROJECT APPLE")

        self.width = 600
        self.height = 600
        self.step_size = 60
        menu_height = 100
        self.screen = pygame.display.set_mode((self.width, self.height + menu_height))

        self.move = 'right'
        self.prev_event = pygame.K_LEFT

        start_x = start_y = 60
        self.snake = Snake(start_x,start_y)

        self.running == True

    def refreshScreen(self):
        self.screen.fill(white)
        for x in range(0, self.width, self.step_size):
            for y in range(0, self.height, self.step_size):
                gridRect = pygame.Rect(x, y, self.step_size, self.step_size)
                pygame.draw.rect(self.screen, black, gridRect, 1)

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # STORE VALUE OF KEY SO WE CANT MOVE BACKWARDS
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    if self.prev_event == pygame.K_RIGHT:
                        pass
                    else:
                        self.move = 'left'
                        self.prev_event = pygame.K_LEFT

                elif event.key == pygame.K_RIGHT:
                    if self.prev_event == pygame.K_LEFT:
                        pass
                    else:
                       self.move = 'right'
                       self.prev_event = pygame.K_RIGHT

                elif event.key == pygame.K_UP:
                    if self.prev_event == pygame.K_DOWN:
                        pass
                    else:
                        self.move = 'up'
                        self.prev_event = pygame.K_UP

                elif event.key == pygame.K_DOWN:
                    if self.prev_event == pygame.K_UP:
                        pass
                    else:
                        self.move = 'down'
                        self.prev_event = pygame.K_DOWN

    def moveSnake(self):


    def gameLoop(self):
        while (self.running):
            self.refreshScreen()
            self.eventHandle()
            self.moveSnake()
            self.checkCollisions()
            self.checkApple()
            self.checkVision()
            self.drawSnake()
            self.drawUI()




        # SNAKE LOGIC


moveRight = True
moveLeft = False
moveUp = False
moveDown = False
collide_wall = False
apple_here = False
eventPrev = pygame.K_RIGHT
score = 0
checkDist = False
pointer = [0, 0]
distWall = {"N": 0, "NE": 0, "E": 0, "SE": 0, "S": 0, "SW": 0, "W": 0, "NW": 0}
dirDict = {"N": [0, 1, 0, 0], "NE": [1, 1, 0, 0], "E": [1, 0, 0, 0], "SE": [1, -1, 0, 0], "S": [0, -1, 0, 0],
           "SW": [-1, -1, 0, 0], "W": [-1, 0, 0, 0], "NW": [-1, 1, 0, 0]}

# UPDATE DISPLAY
pygame.display.update()

# define a variable to control the main loop
running = True

# main loop
while running:
    # REFRESH SCREEN (DELETE ALL SMILEYS)
    screen.fill(white)
    for x in range(0, frame_width, snakeWidth):
        for y in range(0, frame_height, snakeWidth):
            gridRect = pygame.Rect(x, y, snakeWidth, snakeHeight)
            pygame.draw.rect(screen, black, gridRect, 1)

    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

        # STORE VALUE OF KEY SO WE CANT MOVE BACKWARDS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if eventPrev == pygame.K_RIGHT:
                    moveLeft = False
                else:
                    moveRight = False
                    moveLeft = True
                    moveUp = False
                    moveDown = False
                    eventPrev = pygame.K_LEFT
            if event.key == pygame.K_RIGHT:
                if eventPrev == pygame.K_LEFT:
                    moveRight = False
                else:
                    moveRight = True
                    moveLeft = False
                    moveUp = False
                    moveDown = False
                    eventPrev = pygame.K_RIGHT
            if event.key == pygame.K_UP:
                if eventPrev == pygame.K_DOWN:
                    moveUp = False
                else:
                    moveRight = False
                    moveLeft = False
                    moveUp = True
                    moveDown = False
                    eventPrev = pygame.K_UP
            if event.key == pygame.K_DOWN:
                if eventPrev == pygame.K_UP:
                    moveDown = False
                else:
                    moveRight = False
                    moveLeft = False
                    moveUp = False
                    moveDown = True
                    eventPrev = pygame.K_DOWN

    # better way ?
    dirDict = {"N": [0, 1, 0, 0], "NE": [1, 1, 0, 0], "E": [1, 0, 0, 0], "SE": [1, -1, 0, 0], "S": [0, -1, 0, 0],
               "SW": [-1, -1, 0, 0], "W": [-1, 0, 0, 0], "NW": [-1, 1, 0, 0]}

    # UPDATE PREV POS
    # deepcopy needed as its a list of lists
    prevSnake = copy.deepcopy(curSnake)

    # MOVE HEAD TO NEXT POSITION
    if moveRight:
        curSnake[0][0] += step_x
    elif moveLeft:
        curSnake[0][0] -= step_x
    elif moveUp:
        curSnake[0][1] -= step_y
    elif moveDown:
        curSnake[0][1] += step_y

    # MOVE REST OF BODY (IF IT EXISTS)
    # (dont need if?)
    if len(curSnake) > 1:
        for x in range(1, len(curSnake)):
            curSnake[x][0] = prevSnake[x - 1][0]
            curSnake[x][1] = prevSnake[x - 1][1]


    # CALCULATE DISTANCE TO WALL
    # PUT ALL THIS INTO AN ARRAY AND NESTED LOOPS
    # north = up
    # do we use absolute numerals?? need to specify direction to neural net...
    distWall["N"] = abs(0 - curSnake[0][1])
    distWall["S"] = abs((frame_height - snakeHeight) - curSnake[0][1])
    distWall["W"] = abs(0 - curSnake[0][0])
    distWall["E"] = abs((frame_width - snakeWidth) - curSnake[0][0])

    for key in distWall:
        if key == "NE":
            if distWall["N"] > distWall["E"]:
                distWall["NE"] = 2 * distWall["E"]
            else:
                distWall["NE"] = 2 * distWall["N"]
        if key == "SE":
            if distWall["S"] > distWall["E"]:
                distWall["SE"] = 2 * distWall["E"]
            else:
                distWall["SE"] = 2 * distWall["S"]
        if key == "SW":
            if distWall["S"] > distWall["W"]:
                distWall["SW"] = 2 * distWall["W"]
            else:
                distWall["SW"] = 2 * distWall["S"]
        if key == "NW":
            if distWall["N"] > distWall["W"]:
                distWall["NW"] = 2 * distWall["W"]
            else:
                distWall["NW"] = 2 * distWall["N"]

    # CALCULATE DISTANCE TO BODY
    # OR CHECK IF BODY IS IN LOS (BINARY)

    # CHECK FOR WALL COLLISION
    if curSnake[0][0] <= -1:
        collide_wall = True
    if (curSnake[0][0] + snakeWidth) >= frame_width + 1:
        collide_wall = True
    if curSnake[0][1] <= -1:
        collide_wall = True
    if (curSnake[0][1] + snakeHeight) >= frame_height + 1:
        collide_wall = True

    # BODY COLLISION
    # -- clean up this code --
    for i in range(1, len(curSnake)):
        if curSnake[i][0] == curSnake[0][0]:
            if curSnake[i][1] == curSnake[0][1]:
                collide_wall = True
                break

    if collide_wall == True:
        for i in range(len(curSnake) - 1, 0, -1):
            curSnake.remove(curSnake[i])
        curSnake[0][0] = startX
        curSnake[0][1] = startY
        collide_wall = False
        moveRight = True
        moveLeft = False
        moveUp = False
        moveDown = False
        eventPrev = pygame.K_RIGHT
        score = 0
        # OUTPUT TEXT HERE SAYING COLLISION?

    # DEFINE THE GRID OF POSITIONS THE APPLE CAN TAKE
    # grid = [[0,0], [60,0], [120,0],
    #         [0,60], [60,60], [120,60]]
    grid = []
    for y in range(0, frame_width, snakeWidth):
        for x in range(0, frame_width, snakeWidth):
            grid.append([x, y])

    # APPLE FUNCTION
    if apple_here == False:
        apple_here = True

        for i in curSnake:
            # don't need if, because snake parts will always be inside grid?
            if i in grid:
                # print("apple vals removed: ", i)
                grid.remove(i)
        apple = random.choice(grid)
        appleRect = pygame.Rect(apple[0], apple[1], snakeWidth, snakeHeight)

    if apple_here == True:
        pygame.draw.rect(screen, green, appleRect)

    # EAT APPLE, SET IT TO TRUE
    # append new tail to prev pos of last tail element (ie the head if length = 1)
    if curSnake[0][0] == apple[0] and curSnake[0][1] == apple[1]:
        apple_here = False
        score += 1
        curSnake.append(prevSnake[-1])

    # CALCULATE DISTANCE TO APPLE
    # OR CHECK IF APPLE IS IN LOS (BINARY)
    # RESET THESE VALUES EVERY TIME?
    # can get stuck inside while loop here... be careful .. need better way to check this, or break out of if

    # APPLE LOOP
    hitApple = hitWall = False
    for direct in dirDict:
        laserX = curSnake[0][0]
        laserY = curSnake[0][1]
        hitWall = False
        while not (hitApple or hitWall):
            # HIT APPLE = succeed, break out of loop
            if laserX == apple[0] and laserY == apple[1]:
                dirDict[direct][2] = 1
                hitApple = True  # does it exit here, or update laser first?
            # HIT WALL = skip to next dir
            if laserX >= frame_width - snakeWidth or laserX <= 0:
                hitWall = True
            if laserY >= frame_height - snakeHeight or laserY <= 0:
                hitWall = True
            # has to be subtract for y, or swap dict above
            laserX += dirDict[direct][0] * snakeWidth
            laserY -= dirDict[direct][1] * snakeHeight
            # print(laserX,laserY)
        if hitApple == True:
            break

    # BODY LOOP
    hitBody = hitWall = False
    for direct in dirDict:
        laserX = curSnake[0][0]
        laserY = curSnake[0][1]
        hitBody = hitWall = False
        while not (hitBody or hitWall):
            # HIT BODY = set to 1, continue searching directions
            for part in range(1, len(curSnake)):
                if laserX == curSnake[part][0] and laserY == curSnake[part][1]:
                    hitBody = True
                    dirDict[direct][3] = 1
            # HIT WALL = skip to next dir
            if laserX >= frame_width - snakeWidth or laserX <= 0:
                hitWall = True
            if laserY >= frame_height - snakeHeight or laserY <= 0:
                hitWall = True
            # has to be subtract for y, or swap dict above
            laserX += dirDict[direct][0] * snakeWidth
            laserY -= dirDict[direct][1] * snakeHeight

    ## DRAW FUNCTION
    for i in range(len(curSnake)):
        colour = blue
        if i == 0:
            colour = red
        pygame.draw.rect(screen, colour, pygame.Rect(curSnake[i][0], curSnake[i][1], snakeWidth, snakeHeight))
        pygame.draw.rect(screen, red, pygame.Rect(curSnake[i][0], curSnake[i][1], snakeWidth, snakeHeight), 1)

    # DRAW SCORE TEXT
    # Put these in a list and loop through all text to draw in one spot
    pygame.draw.rect(screen, grey, pygame.Rect(0, frame_height, frame_width, menu_height))

    # xyText = font.render("x,y = "+ str(curSnake[0][0]) + "," + str(curSnake[0][1]), True, black, red)
    # xyRect = xyText.get_rect()
    # xyRect.center = xyTextCenter
    # screen.blit(xyText,xyRect)
    #
    # scoreText = font.render("score = " + str(score), True, black, red)
    # scoreRect = scoreText.get_rect()
    # scoreRect.center = (300,650)    # TODO
    # screen.blit(scoreText,scoreRect)

    # xs = 0
    # ys = 600
    # for key in distWall:
    #     distText = font.render(key + ":" + str(distWall[key]), True, black)
    #     screen.blit(distText,(xs,ys))
    #     ys += 20
    #     if (ys == 680):
    #         xs = 100
    #         ys = 600

    distText = font.render(str(distWall), True, black)
    screen.blit(distText, (0, 650))
    dirText = font.render(str(dirDict), True, black)
    screen.blit(dirText, (0, 680))

    # SLOW DOWN SNAKE - BETTER WAY?
    # time.sleep(0.15)

    clk = pygame.time.Clock()
    clk.tick(5)

    # UPDATE SCREEN
    pygame.display.flip()
