import pygame

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
struct = [4, 4, 2]


xwidth = 100
ywidth = 50
xshift = 50
yshift = 50
draw_lines = True

nn = []
for layer in range(len(struct)):
    nn.append([])
    x = (layer*xwidth) + xshift
    for node in range(struct[layer]):
        y = (node*ywidth) + yshift
        nn[layer].append((x,y))

print(nn)
x = input()


for layer in range(len(nn)):
    x = (layer*xwidth) + xshift
    for node in range(len(nn[layer])):
        if layer == len(nn) - 1:
            yshift = 100
            draw_lines = False
        y = (node*ywidth) + yshift
        pygame.draw.circle(screen, red, (x, y), 10)
        
        if draw_lines:
            for next_node in range(len(nn[layer + 1])):
                if layer == len(nn) - 2:
                    yshift = 100
                next_layer = layer + 1
                x2 = (next_layer*xwidth) + xshift
                y2 = (next_node*ywidth) + yshift
                pygame.draw.line(screen, black, (x, y), (x2, y2), 2)
                yshift = 50
        



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    clk = pygame.time.Clock()
    clk.tick(5)
    pygame.display.flip()
