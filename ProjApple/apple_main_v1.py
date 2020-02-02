# import the pygame module, so you can use it
import pygame, time


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
screen.fill(white)


# DRAW RECT
rectWidth = 60
rectHeight = 60
startX = 60
startY = 60
snakeRect = pygame.Rect(startX,startY,rectWidth,rectHeight)
pygame.draw.rect(screen,black,snakeRect)

step_x = 60
step_y = 60

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


    # check if the smiley is still on screen, if not change direction
    # if xpos > width - 64 or xpos < 0:
    #     step_x = -step_x
    # if ypos > height - 64 or ypos < 0:
    #     step_y = -step_y

    # update the position of the smiley
    # xpos += step_x  # move it to the right
    # ypos += step_y  # move it down

    if (moveRight):
        snakeRect.x += step_x
    elif (moveLeft):
        snakeRect.x -= step_x
    elif (moveUp):
        snakeRect.y -= step_y
    elif (moveDown):
        snakeRect.y += step_y

    # DRAW SMILEY
    #screen.blit(smiley, (xpos, ypos))
    # snakeRect.x = xpos
    # snakeRect.y = ypos

    if (snakeRect.x <= -1):
        collisionXLeft = True
        snakeRect.x = startX
        snakeRect.y = startY
    if ((snakeRect.x + snakeRect.width) >= frame_width + 1):
        collisionXRight = True
        snakeRect.x = startX
        snakeRect.y = startY
    if (snakeRect.y <= -1):
        collisionYUp = True
        snakeRect.x = startX
        snakeRect.y = startY
    if ((snakeRect.y + snakeRect.height) >= frame_height + 1):
        collisionYDown = True
        snakeRect.x = startX
        snakeRect.y = startY

    # if (collisionXLeft or collisionXRight or collisionYUp or collisionYDown):
    #     print("RESET POSITION")
    #     snakeRect.x = startX
    #     snakeRect.y = startY

    pygame.draw.rect(screen, black, snakeRect,1)
    #print(snakeRect.x,snakeRect.y,snakeRect.centerx,snakeRect.centery)

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
