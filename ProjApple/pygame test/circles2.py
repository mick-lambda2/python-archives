import pygame, math
import numpy as np

# PYGAME VARIABLES
pygame.init()
red = [255, 0, 0]
white = [255, 255, 255]
black = [0, 0, 0]

# FRAME VARIABLES
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
screen.fill(white)

nn = [[4], [4], [2]]
nn = [[4,4,4,4], [4,4,4,4], [2,2]]


struct = [10, 10, 10, 4]
xwidth = 100
ywidth = 50
xshift = 50
yshift = 50
y_dyn = 0
draw_lines = True
nn = []

# CONSTRUCT NETWORK = ABSOLUTE POSITIONS
for layer in range(len(struct)):
    nn.append([])
    x = (layer*xwidth) + xshift
    for node in range(struct[layer]):
        if layer == 0:
            if struct[layer] >= struct[layer + 1]:
                y_dyn = yshift
            else:
                y_dyn = (math.floor((struct[layer + 1] - struct[layer]) / 2) * yshift) + yshift
        elif layer == len(struct) - 1:
            y_dyn = (math.floor((struct[layer - 1] - struct[layer]) / 2) * yshift) + yshift
        elif layer > 0 and layer < len(struct) - 1:
            if struct[layer] >= struct[layer - 1]:
                y_dyn = yshift
            else:
                y_dyn = (math.floor((struct[layer - 1] - struct[layer]) / 2) * yshift) + yshift
        y = (node*ywidth) + y_dyn
        nn[layer].append((x,y))

print(nn)

# CREATE WEIGHTS for struct = [10, 10, 10, 4]
# column vector for each node...
w1 = 2 * np.random.random((struct[1], struct[0])) - 1
w2 = 2 * np.random.random((struct[2], struct[1])) - 1
w3 = 2 * np.random.random((struct[3], struct[2])) - 1
w_all = [w1, w2, w3]
print(w3)

# DRAW CIRCLES + LINES + APPLY WEIGHTS (COLOURS)
for layer in range(len(nn)):
    for node in range(len(nn[layer])):
        x = nn[layer][node][0]
        y = nn[layer][node][1]
        if layer == len(nn) - 1:
            draw_lines = False

        if draw_lines:
            for next_node in range(len(nn[layer + 1])):
                x2 = nn[layer + 1][next_node][0]
                y2 = nn[layer + 1][next_node][1]
                
                weight = w_all[layer][next_node][node]
                
                # lower weight = more blue = less activated
                # between 1 and -1 is good, gives us the 2 normalized ranges
                if weight >= 0:
                    colour = [0, weight*255, 0]
                else:
                    colour = [0, 0, -weight*255]

                pygame.draw.line(screen, colour, (x, y), (x2, y2), 2)
                
        # could just pass it the tuple here, instead of seperate x y
        pygame.draw.circle(screen, red, (x, y), 10)
         
                
        



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    clk = pygame.time.Clock()
    clk.tick(5)
    pygame.display.flip()
