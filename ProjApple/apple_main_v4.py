# import the pygame module, so you can use it
import pygame, time, random


# initialize the pygame module
pygame.init()

# load and set the logo
#logo = pygame.image.load("logo32x32.png")
#pygame.display.set_icon(logo)
pygame.display.set_caption("minimal program")

# create a surface on screen that has the size of 240 x 180
frame_width = 600
frame_height = 600
screen = pygame.display.set_mode((frame_width, frame_height))

# DRAW WHITE BACKGROUND
white = [255, 255, 255]
black = [0,0,0]
red = [255,0,0]
green = [0,255,0]
screen.fill(white)


# DRAW RECT
snakeWidth = 60
snakeHeight = 60
startX = 60
startY = 60
snakeRect = pygame.Rect(startX, startY, snakeWidth, snakeHeight)
pygame.draw.rect(screen,black,snakeRect)

snake = [snakeRect]

step_x = 60
step_y = 60
appleX = 0
appleY = 0
apple = False

moveRight = False
moveLeft = False
moveUp = False
moveDown = False
collisionXLeft = False
collisionXRight = False
collisionYUp = False
collisionYDown = False

# UPDATE DISPLAY (both do the same thing)
pygame.display.update()
#pygame.display.flip()

# define a variable to control the main loop
running = True

# main loop
while running:

    # REFRESH SCREEN (DELETE ALL SMILEYS)
    screen.fill(white)

    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFT")
                #xpos -= step_x
                moveRight = False
                moveLeft = True
                moveUp = False
                moveDown = False
            if event.key == pygame.K_RIGHT:
                print("RIGHT")
                # xpos += step_x
                moveRight = True
                moveLeft = False
                moveUp = False
                moveDown = False
            if event.key == pygame.K_UP:
                print("UP")
                #ypos -= step_y
                moveRight = False
                moveLeft = False
                moveUp = True
                moveDown = False
            if event.key == pygame.K_DOWN:
                print("DOWN")
                #ypos += step_y
                moveRight = False
                moveLeft = False
                moveUp = False
                moveDown = True
            if event.key == pygame.K_0:
                ## append with same coord as last element. pos of head will be updated
                s = len(snake) - 1
                snake.append(pygame.Rect(snake[s].x, snake[s].y, snakeWidth, snakeHeight))


    # check if the smiley is still on screen, if not change direction
    # if xpos > width - 64 or xpos < 0:
    #     step_x = -step_x
    # if ypos > height - 64 or ypos < 0:
    #     step_y = -step_y

    # update the position of the smiley
    # xpos += step_x  # move it to the right
    # ypos += step_y  # move it down

    if (moveRight):
        snake[0].x += step_x
    elif (moveLeft):
        snake[0].x -= step_x
    elif (moveUp):
        snake[0].y -= step_y
    elif (moveDown):
        snake[0].y += step_y

    # DRAW SMILEY
    #screen.blit(smiley, (xpos, ypos))
    # snakeRect.x = xpos
    # snakeRect.y = ypos

    if (snake[0].x <= -1):
        collisionXLeft = True
        for i in range(len(snake)-1,0,-1):
            snake.remove(snake[i])
        snake[0].x = startX
        snake[0].y = startY
    if ((snake[0].x + snake[0].width) >= frame_width + 1):
        collisionXRight = True
        for i in range(len(snake)-1,0,-1):
            snake.remove(snake[i])
        snake[0].x = startX
        snake[0].y = startY
    if (snake[0].y <= -1):
        collisionYUp = True
        for i in range(len(snake)-1,0,-1):
            snake.remove(snake[i])
        snake[0].x = startX
        snake[0].y = startY
    if ((snake[0].y + snake[0].height) >= frame_height + 1):
        collisionYDown = True
        for i in range(len(snake)-1,0,-1):
            snake.remove(snake[i])
        snake[0].x = startX
        snake[0].y = startY

    # if (collisionXLeft or collisionXRight or collisionYUp or collisionYDown):
    #     print("RESET POSITION")
    #     snakeRect.x = startX
    #     snakeRect.y = startY


    gridX = []
    gridY = []
    for i in range(0, 600, 60):
        gridX.append(i)
        gridY.append(i)
        print(i)

    if apple == False:
        # APPLE FUNCTION
        apple = True

        for part in snake:
            if part.x in gridX:
                gridX.remove(part.x)
                print("remove x")
            if part.y in gridY:
                gridY.remove(part.y)
                print("remove y")

        appleX = random.choice(gridX)
        appleY = random.choice(gridY)
        print("apple", appleX, appleY)
        appleRect = pygame.Rect(appleX, appleY, snakeWidth, snakeHeight)

    if apple == True:
        pygame.draw.rect(screen, green, appleRect, 5)

    # EAT APPLE, SET IT TO TRUE
    if snake[0].x == appleX and snake[0].y == appleY:
        apple = False
        s = len(snake) - 1
        if s == 0:
            if (moveRight):
                snake.append(pygame.Rect(snake[s].x - snakeWidth, snake[s].y, snakeWidth, snakeHeight))
            elif (moveLeft):
                snake.append(pygame.Rect(snake[s].x + snakeWidth, snake[s].y, snakeWidth, snakeHeight))
            elif (moveUp):
                snake.append(pygame.Rect(snake[s].x, snake[s].y - snakeHeight, snakeWidth, snakeHeight))
            elif (moveDown):
                snake.append(pygame.Rect(snake[s].x, snake[s].y + snakeHeight, snakeWidth, snakeHeight))
        else:
            snake.append(pygame.Rect(snake[s].x, snake[s].y, snakeWidth, snakeHeight))
        # head is drawn over it anyway

    for i in range(len(snake) - 1, -1, -1):
        if i == 0:
            pygame.draw.rect(screen, red, snake[i])
            break
        snake[i].x = snake[i - 1].x
        snake[i].y = snake[i - 1].y
        pygame.draw.rect(screen, black, snake[i])
    # print(snakeRect.x,snakeRect.y,snakeRect.centerx,snakeRect.centery)

    # SLOW DOWN SNAKE - BETTER WAY?
    time.sleep(0.15)

    # UPDATE SCREEN
    pygame.display.flip()

#def move(direction):

def wallCollide(x1,y1):
    if (x1 == frame_width or x1 == 0):
        return True
    elif (y1 == frame_height or y1 == 0):
        return True
    else:
        return False

# def calcCorners(topLeft,rectWidth,rectHeight):
    # topRight = [topLeft.]
