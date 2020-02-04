hitApple = hitWall = False
x = 0

while not (hitApple or hitWall):
    print(x)
    x += 1
    if x == 5: hitWall = True
