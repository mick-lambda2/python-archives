# import the pygame module, so you can use it
import pygame, time, random, copy
import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plot
from scipy.special import expit as activ_fn

# initialize the pygame module
pygame.init()

# load and set the logo
#logo = pygame.image.load("logo32x32.png")
#pygame.display.set_icon(logo)
pygame.display.set_caption("minimal program")

# create a surface on screen that has the size of 240 x 180
frame_width = 600
frame_height = 600
menu_height = 100
screen = pygame.display.set_mode((frame_width, frame_height + menu_height))

# DRAW WHITE BACKGROUND
white = [255, 255, 255]
black = [0,0,0]
red = [255,0,0]
blue = [0,0,255]
green = [0,255,0]
grey = [220,220,220]
screen.fill(white)

# CREATE FONT - is this needed here?
font = pygame.font.Font('freesansbold.ttf', 8)
# text = font.render('Hello', True, black, red)
# textRect = text.get_rect()
# textRect.center = (400,400)
xyTextCenter = (100,frame_height+50)

# SNAKE VARIABLES
masterSize = 60
snakeWidth = masterSize
snakeHeight = masterSize
startX = masterSize
startY = masterSize
step_x = masterSize
step_y = masterSize
snakeRect = pygame.Rect(startX, startY, snakeWidth, snakeHeight)
pygame.draw.rect(screen,black,snakeRect)

curSnake = [[startX, startY]]
prevSnake = [[]]

moveRight = True
moveLeft = False
moveUp = False
moveDown = False
collide_wall = False
apple_here = False
eventPrev = pygame.K_RIGHT
score = 0
checkDist = False
pointer = [0,0]
distWall = {"N":0,"NE":0,"E":0,"SE":0,"S":0,"SW":0,"W":0,"NW":0}
distApple = {"N":0,"NE":0,"E":0,"SE":0,"S":0,"SW":0,"W":0,"NW":0}


# UPDATE DISPLAY (both do the same thing)
pygame.display.update()
#pygame.display.flip()

# NEURAL NETWORK DEFINITION
class NeuralNetwork:
    def __init__(self,inodes,onodes,hnodes,learn_rate):
        # MAIN INPUTS TO CLASS - others like the boundaries are extrapolations
        self.inodes = inodes
        self.onodes = onodes
        self.hnodes = hnodes
        self.learn_rate = learn_rate
        self.create_wmatrix()

    # always pass self into def fn of a class
    def create_wmatrix(self):
        bound1 = 1 / np.sqrt(self.inodes)
        bound2 = 1 / np.sqrt(self.hnodes)

        # WEIGHTS MATRIX -- THIS COULD ALL BE INSIDE INIT FUNCTION
        # self means we can use wih and who elsewhere now
        Xih = truncated_normal(mean=2, sd=1, low=-bound1, upp=bound1)
        Xho = truncated_normal(mean=2, sd=1, low=-bound2, upp=bound2)
        self.wih = Xih.rvs((self.hnodes, self.inodes))
        self.who = Xho.rvs((self.onodes, self.hnodes))

    def train(self):
        pass

    def run(self, ivec):
        # TURN IVEC INTO COLUMN VECTOR
        ivec =np.array(ivec,ndmin=2).T
        # STAGE 1
        ovec = np.dot(self.wih,ivec)
        ovec = activ_fn(ovec)
        # STAGE 2 - FINAL OUTPUT
        ovec = np.dot(self.who,ovec)
        ovec = activ_fn(ovec)
        return ovec


def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


# NETWORK MATRICES - MIGHT CHANGE THIS
inodes = 24
hnodes = 24
onodes = 4
ivec = []
nwork = NeuralNetwork(inodes,onodes,hnodes,0.1)

# RUN THE NETWORK WITH INITIAL WEIGHTS IN IVEC
#output = nwork.run(ivec)


# define a variable to control the main loop
running = True

# main loop
while running:
    # REFRESH SCREEN (DELETE ALL SMILEYS)
    screen.fill(white)
    for x in range(0,frame_width,snakeWidth):
        for y in range(0,frame_height,snakeWidth):
            gridRect = pygame.Rect(x, y, snakeWidth, snakeHeight)
            pygame.draw.rect(screen, black, gridRect,1)

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


    # UPDATE PREV POS
    # deepcopy needed as its a list of lists
    prevSnake = copy.deepcopy(curSnake)

    # MOVE HEAD TO NEXT POSITION
    if (moveRight):
        curSnake[0][0] += step_x
    elif (moveLeft):
        curSnake[0][0] -= step_x
    elif (moveUp):
        curSnake[0][1] -= step_y
    elif (moveDown):
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
    distWall["S"] = abs((frame_height-snakeHeight) - curSnake[0][1])
    distWall["W"] = abs(0 - curSnake[0][0])
    distWall["E"]= abs((frame_width-snakeWidth) - curSnake[0][0])


    for key in distWall:
        if key == "NE":
            if distWall["N"] > distWall["E"]:
                distWall["NE"] = 2*distWall["E"]
            else:
                distWall["NE"] = 2*distWall["N"]
        if key == "SE":
            if distWall["S"] > distWall["E"]:
                distWall["SE"] = 2*distWall["E"]
            else:
                distWall["SE"] = 2*distWall["S"]
        if key == "SW":
            if distWall["S"] > distWall["W"]:
                distWall["SW"] = 2*distWall["W"]
            else:
                distWall["SW"] = 2*distWall["S"]
        if key == "NW":
            if distWall["N"] > distWall["W"]:
                distWall["NW"] = 2*distWall["W"]
            else:
                distWall["NW"] = 2*distWall["N"]


    # CALCULATE DISTANCE TO BODY
    # OR CHECK IF BODY IS IN LOS (BINARY)


    # CHECK FOR WALL COLLISION
    if (curSnake[0][0] <= -1):
        collide_wall = True
    if ((curSnake[0][0] + snakeWidth) >= frame_width + 1):
        collide_wall = True
    if (curSnake[0][1] <= -1):
        collide_wall = True
    if ((curSnake[0][1] + snakeHeight) >= frame_height + 1):
        collide_wall = True

    # BODY COLLISION
    # -- clean up this code --
    for i in range(1,len(curSnake)):
        if curSnake[i][0] == curSnake[0][0]:
            if curSnake[i][1] == curSnake[0][1]:
                collide_wall = True
                break

    if (collide_wall == True):
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
        for x in range(0,frame_width,snakeWidth):
            grid.append([x,y])

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

    # if x value is the same
    if apple[0] == curSnake[0][0]:
        # if y val is lesser (above)
        if apple[1] < curSnake[0][1]:
            distApple["N"] = 1
        elif apple[1] > curSnake[0][1]:
            distApple["S"] = 1
    # if y value is the same
    elif apple[1] == curSnake[0][1]:
        # if x val is lesser (to the left)
        if apple[0] < curSnake[0][0]:
            distApple["W"] = 1
        elif apple[0] > curSnake[0][0]:
            distApple["E"] = 1

    # only set the value in the case that is true, reset vals every frame = one hot binary
    posX = curSnake[0][0]
    posY = curSnake[0][1]
    appleLoop = True

    # start at x or Y edge - cant be NE
    if posX == frame_width - snakeWidth or posY == 0:
        appleLoop = False

    # now begin search NEwards....
    while appleLoop == True:
        posX = posX + snakeWidth
        posY = posX + snakeHeight

        # found apple case
        if posX == apple[0] and posY == apple[1]:
            distApple["NE"] = 1
            break
        elif posX == frame_width - snakeWidth or posY == 0:
            break

    # SE
    posX = curSnake[0][0]
    posY = curSnake[0][1]
    appleLoop = True

    # start at x or Y edge
    if posX == frame_width - snakeWidth or posY == frame_height - snakeHeight:
        appleLoop = False

    # now begin search
    while appleLoop == True:
        posX = posX + snakeWidth
        posY = posX - snakeHeight

        # found apple case
        if posX == apple[0] and posY == apple[1]:
            distApple["SE"] = 1
            break
        elif posX == frame_width - snakeWidth or posY == frame_height - snakeHeight:
            break

    # SW
    posX = curSnake[0][0]
    posY = curSnake[0][1]
    appleLoop = True

    # start at x or Y edge
    if posX == 0 or posY == :
        appleLoop = False

    # now begin search ##############################
    while appleLoop == True:
        posX = posX - snakeWidth
        posY = posX - snakeHeight

        # found apple case
        if posX == apple[0] and posY == apple[1]:
            distApple["Sw"] = 1
            break
        elif posX == frame_width - snakeWidth or posY == frame_height - snakeHeight:
            break


    for y in range(ysteps):
        for x in range(xsteps):
            if apple[0] == curSnake[0][0] + snakeWidth*xsteps

    # DRAW FUNCTION
    for i in range(len(curSnake)):
        colour = blue
        if i == 0:
            colour = red
        pygame.draw.rect(screen, colour, pygame.Rect(curSnake[i][0], curSnake[i][1], snakeWidth, snakeHeight))
        pygame.draw.rect(screen, red, pygame.Rect(curSnake[i][0], curSnake[i][1], snakeWidth, snakeHeight),1)


    # DRAW SCORE TEXT
    # Put these in a list and loop through all text to draw in one spot
    pygame.draw.rect(screen, grey, pygame.Rect(0,frame_height, frame_width, menu_height))

    # xyText = font.render("x,y = "+ str(curSnake[0][0]) + "," + str(curSnake[0][1]), True, black, red)
    # xyRect = xyText.get_rect()
    # xyRect.center = xyTextCenter
    # screen.blit(xyText,xyRect)
    #
    # scoreText = font.render("score = " + str(score), True, black, red)
    # scoreRect = scoreText.get_rect()
    # scoreRect.center = (300,650)    # TODO
    # screen.blit(scoreText,scoreRect)

    xs = 0
    ys = 600
    for key in distWall:
        distText = font.render(key + ":" + str(distWall[key]), True, black)
        screen.blit(distText,(xs,ys))
        ys += 20
        if (ys == 680):
            xs = 100
            ys = 600

    # SLOW DOWN SNAKE - BETTER WAY?
    time.sleep(0.15)

    # UPDATE SCREEN
    pygame.display.flip()


