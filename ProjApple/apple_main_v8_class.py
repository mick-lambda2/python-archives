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

class Snake:
    def __init__(self, start_x, start_y, step_size, width, height):
        self.body = [[start_x, start_y]]
        self.step_size = step_size
        self.width = width
        self.height = height
        self.menu_height = 200
        self.previous = [[]]
        self.score = 0

        self.distWall = {"N": 0, "NE": 0, "E": 0, "SE": 0, "S": 0, "SW": 0, "W": 0, "NW": 0}
        self.dirDict = {"N": [0, 1, 0, 0], "NE": [1, 1, 0, 0], "E": [1, 0, 0, 0], "SE": [1, -1, 0, 0], "S": [0, -1, 0, 0],
                   "SW": [-1, -1, 0, 0], "W": [-1, 0, 0, 0], "NW": [-1, 1, 0, 0]}

    def checkCollisions(self):
        collide = False

        # WALL COLLISION
        if self.body[0][0] <= -1:
            collide = True
        if (self.body[0][0] + self.step_size) >= self.step_size + 1:
            collide = True
        if self.body[0][1] <= -1:
            collide = True
        if (self.body[0][1] + self.step_size) >= self.step_size + 1:
            collide = True

        # BODY COLLISION
        for i in range(1, len(self.body)):
            if self.body[i][0] == self.body[0][0]:
                if self.body[i][1] == self.body[0][1]:
                    collide = True
                    break

        return collide

    def updateBody(self):
        x = 5

    def updateVision(self, apple):
        # WALL DISTANCE
        self.distWall["N"] = abs(0 - self.body[0][1])
        self.distWall["S"] = abs((self.height - self.step_size) - self.body[0][1])
        self.distWall["W"] = abs(0 - self.body[0][0])
        self.distWall["E"] = abs((self.width - self.step_size) - self.body[0][0])

        for key in self.distWall:
            if key == "NE":
                if self.distWall["N"] > self.distWall["E"]:
                    self.distWall["NE"] = 2 * self.distWall["E"]
                else:
                    self.distWall["NE"] = 2 * self.distWall["N"]
            if key == "SE":
                if self.distWall["S"] > self.distWall["E"]:
                    self.distWall["SE"] = 2 * self.distWall["E"]
                else:
                    self.distWall["SE"] = 2 * self.distWall["S"]
            if key == "SW":
                if self.distWall["S"] > self.distWall["W"]:
                    self.distWall["SW"] = 2 * self.distWall["W"]
                else:
                    self.distWall["SW"] = 2 * self.distWall["S"]
            if key == "NW":
                if self.distWall["N"] > self.distWall["W"]:
                    self.distWall["NW"] = 2 * self.distWall["W"]
                else:
                    self.distWall["NW"] = 2 * self.distWall["N"]

        # APPLE BINARY
        hitApple = hitWall = False
        for direct in self.dirDict:
            laserX = self.body[0][0]
            laserY = self.body[0][1]
            hitWall = False
            while not (hitApple or hitWall):
                # HIT APPLE = succeed, break out of loop
                if laserX == apple[0] and laserY == apple[1]:
                    self.dirDict[direct][2] = 1
                    hitApple = True  # does it exit here, or update laser first?
                # HIT WALL = skip to next dir
                if laserX >= self.width - self.step_size or laserX <= 0:
                    hitWall = True
                if laserY >= self.height - self.step_size or laserY <= 0:
                    hitWall = True
                # has to be subtract for y, or swap dict above
                laserX += self.dirDict[direct][0] * self.step_size
                laserY -= self.dirDict[direct][1] * self.step_size
            if hitApple == True:
                break

        # BODY BINARY
        hitBody = hitWall = False
        for direct in self.dirDict:
            laserX = self.body[0][0]
            laserY = self.body[0][1]
            hitBody = hitWall = False
            while not (hitBody or hitWall):
                # HIT BODY = set to 1, continue searching directions
                for part in range(1, len(self.body)):
                    if laserX == self.body[part][0] and laserY == self.body[part][1]:
                        hitBody = True
                        self.dirDict[direct][3] = 1
                # HIT WALL = skip to next dir
                if laserX >= self.width - self.step_size or laserX <= 0:
                    hitWall = True
                if laserY >= self.height - self.step_size or laserY <= 0:
                    hitWall = True
                # has to be subtract for y, or swap dict above
                laserX += self.dirDict[direct][0] * self.step_size
                laserY -= self.dirDict[direct][1] * self.step_size



class SnakeGame:
    def __init__(self):
        pygame.init()
        logo = pygame.image.load("logo1.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("PROJECT APPLE")

        self.width = 600
        self.height = 600
        self.step_size = 60     # Assuming a square snake
        self.menu_height = 100
        self.screen = pygame.display.set_mode((self.width, self.height + self.menu_height))
        self.font1 = pygame.font.Font('freesansbold.ttf', 10)

        self.move = 'right'
        self.prev_event = pygame.K_LEFT

        self.start_x = self.start_y = 60
        self.snake = Snake(self.start_x, self.start_y, self.step_size, self.width, self.height)

        self.grid = []
        for y in range(0, self.height, self.step_size):
            for x in range(0, self.width, self.step_size):
                self.grid.append([x, y])

        self.apple_here = False
        self.apple = 0


        self.collide = False

        self.running = True

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
        # MOVE HEAD
        if self.move == 'left':
            self.snake.body[0][0] += self.step_size
        if self.move == 'right':
            self.snake.body[0][0] -= self.step_size
        if self.move == 'up':
            self.snake.body[0][1] -= self.step_size
        if self.move == 'down':
            self.snake.body[0][1] += self.step_size

        # MOVE REST OF BODY
        if len(self.snake.body) > 1:
            for x in range(1, len(self.snake.body)):
                self.snake.body[x][0] = self.snake.previous[x - 1][0]
                self.snake.body[x][1] = self.snake.previous[x - 1][1]

    def checkCollisions(self):
        self.collide = self.snake.checkCollisions()

        # RESET SNAKE - add game finish code here
        if self.collide == True:
            for i in range(len(self.snake.body) - 1, 0, -1):
                self.snake.body.remove(self.snake.body[i])
            self.snake.body[0][0] = self.startX
            self.snake.body[0][1] = self.startY
            self.collide = False
            self.move = 'right'
            self.prev_event = pygame.K_RIGHT
            self.snake.score = 0

    def checkApple(self):
        # IF APPLE EATEN
        if self.apple_here == False:
            self.apple_here = True

            for i in self.snake.body:
                if i in self.grid:
                    self.grid.remove(i)
            self.apple = random.choice(self.grid)

        # DRAW APPLE
        if self.apple_here == True:
            appleRect = pygame.Rect(self.apple[0], self.apple[1], self.step_size, self.step_size)
            pygame.draw.rect(self.screen, green, appleRect)

        # EAT APPLE - append new tail to prev pos of last tail element
        if self.snake.body[0][0] == self.apple[0] and self.snake.body[0][1] == self.apple[1]:
            self.apple_here = False
            self.snake.score += 1
            self.snake.body.append(self.snake.previous[-1])

    def checkVision(self):
        self.snake.updateVision(self.apple)

    def drawSnake(self):
        for i in range(len(self.snake.body)):
            colour = blue
            if i == 0:
                colour = red
            pygame.draw.rect(self.screen, colour, pygame.Rect(self.snake.body[i][0], self.snake.body[i][1], self.width, self.step_size))
            pygame.draw.rect(self.screen, red, pygame.Rect(self.snake.body[i][0], self.snake.body[i][1], self.height, self.step_size), 1)

    def drawUI(self):
        pygame.draw.rect(self.screen, grey, pygame.Rect(0, self.height, self.width, self.menu_height))

        distText = self.font1.render(str(self.snake.distWall), True, black)
        self.screen.blit(distText, (0, 650))
        dirText = self.font1.render(str(self.snake.dirDict), True, black)
        self.screen.blit(dirText, (0, 680))

    def gameLoop(self):
        while (self.running):
            self.refreshScreen()
            self.eventHandle()
            self.snake.previous = copy.deepcopy(self.snake.body)
            self.moveSnake()
            self.snake.checkCollisions()
            self.checkApple()
            self.checkVision()
            self.drawSnake()
            self.drawUI()

            clk = pygame.time.Clock()
            clk.tick(5)
            pygame.display.flip()

app = SnakeGame()
app.gameLoop()
