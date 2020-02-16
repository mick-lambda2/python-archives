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


struct = [10, 10, 10, 3]
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
        if layer == len(struct) - 1:
            yshift = 100
        y = (node*ywidth) + yshift
        nn[layer].append((x,y))

print(nn)

for layer in range(len(nn)):
    for node in range(len(nn[layer])):
        x = nn[layer][node][0]
        y = nn[layer][node][1]
        if layer == len(nn) - 1:
            draw_lines = False
        # could just pass it the tuple here
        pygame.draw.circle(screen, red, (x, y), 10)
        
        if draw_lines:
            for next_node in range(len(nn[layer + 1])):
                x2 = nn[layer + 1][next_node][0]
                y2 = nn[layer + 1][next_node][1]
                pygame.draw.line(screen, black, (x, y), (x2, y2), 2)
        


scroll = [50,100,150,200,250,300]
i = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if i == 5: i = 0
    for layer in range(len(struct)):
        nn.append([])
        x = (layer*xwidth) + xshift
        for node in range(struct[layer]):
            if layer == len(struct) - 1:
                yshift = scroll[i]
                y = (node*ywidth) + yshift
                nn[layer].append((x,y))
            else:
                y = (node*ywidth) + yshift
                nn[layer].append((x,y))
    print(nn)
    i += 1
    yshift = 50

    for layer in range(len(nn)):
        for node in range(len(nn[layer])):
            x = nn[layer][node][0]
            y = nn[layer][node][1]
            if layer == len(nn) - 1:
                draw_lines = False
            # could just pass it the tuple here
            pygame.draw.circle(screen, red, (x, y), 10)
            
            if draw_lines:
                for next_node in range(len(nn[layer + 1])):
                    x2 = nn[layer + 1][next_node][0]
                    y2 = nn[layer + 1][next_node][1]
                    pygame.draw.line(screen, black, (x, y), (x2, y2), 2)
            


       
    clk = pygame.time.Clock()
    clk.tick(5)
    pygame.display.flip()
