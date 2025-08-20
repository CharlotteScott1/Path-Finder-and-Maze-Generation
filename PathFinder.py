import pygame
import random
pygame.init()

def sort(openList):
    sorted = False
    switch = 0
    while sorted == False:    
        count = 0
        for i in range(0,len(openList)-1):
            if openList[i][5] > openList[i+1][5]:
                switch = openList[i]
                openList[i] = openList[i+1]
                openList[i+1] = switch
                count = count + 1
        if count == 0:
            sorted = True


def mazeGeneration(grid, gridSize,screenWidth,clock,screen):
    adjacent = [1,0],[-1,0],[0,1],[0,-1]
    count =0
    mazeSize = int((screenWidth/gridSize)) - 2
    mazed = False
    count = 2
    removeBorder = 0,0
    joined = []
    for x in range(1,mazeSize+1):
        for y in range(1,mazeSize+1):
            if x %2 ==0 and y%2 == 0:
                grid[x][y] = "b"
            elif x % 2 == 0 or y %2 == 0:
                grid[x][y]= 1
            else:
                grid[x][y]= count
            count= count + 1

    count = 0
    for x in range(0,int(screenWidth/gridSize)):
        for y in range(0,int(screenWidth/gridSize)):
            grid[x][0]= "b"
            grid[x][mazeSize+1]="b"
            grid[0][y] = "b"
            grid[mazeSize+1][y] = "b"


    while mazed == False:
        pygame.event.pump()
        validBorder = True
        removeBorder = 0,0
        while grid[removeBorder[0]][removeBorder[1]] != 1:
            removeBorder = random.randrange(1,mazeSize+1),random.randrange(1,mazeSize+1)
        switched = False
        x = removeBorder[0]
        y = removeBorder[1]
        checked = False
        switch = 0,0
        linkCheck= 0
        for i in adjacent:
            if grid[x+i[0]][y+i[1]]!=1 and grid[x+i[0]][y+i[1]]!="b" :
                if checked == False:
                    linkCheck = grid[x+i[0]][y+i[1]]
                    checked = True
                else:
                    if linkCheck == grid[x+i[0]][y+i[1]]:
                        validBorder = False
        if validBorder == True:
            for i in adjacent:
                if grid[x+i[0]][y+i[1]]!=1 and grid[x+i[0]][y+i[1]]!="b" :
                    if switched == False:
                        switched = True
                        
                        grid[x][y] = grid[x+i[0]][y+i[1]]

                    else:
                        switch = grid[x+i[0]][y+i[1]]
                        for q in range(1,mazeSize + 1):
                           for w in range(1,mazeSize+1):
                               if grid[q][w] ==  switch:
                                   grid[q][w] = grid[x][y]
                        grid[x+i[0]][y+i[1]]=grid[x][y]

        mazed = True
        checker = grid[1][1]
        for x in range(1,mazeSize+1):
            for y in range(1,mazeSize+1):
                if grid[x][y] != 1 and grid[x][y] !="b":
                    if checker != grid[x][y]:
                        mazed = False
                        break


        xCount = 0
        for x in range(0,screenWidth,gridSize):
            yCount =0
            for y in range(0,screenWidth, gridSize):
         
                if grid[yCount][xCount] == 1 or grid[yCount][xCount] == "b":
                    pygame.draw.rect(screen, (0,0,0),(x,y,gridSize-1,gridSize-1))
           
                else:
                    pygame.draw.rect(screen, (255,255,255),(x,y,gridSize-1,gridSize-1))

                yCount = yCount + 1
            xCount = xCount + 1      

        #clock.tick(90)
        pygame.display.flip()

    print(grid)
    return grid


clock=pygame.time.Clock()
print("\n Right click - place barrior \n Left click - remove barrior \n Right click + s - place start point \n Right click + e - place end point \n m - generate maze \n space - run path finder \n backspace - clear grid")
screenWidth = 500
screenHeight = 500
gridSize =25
screen = pygame.display.set_mode((screenWidth, screenHeight))

white = (255,255,255)
grey = (171, 171, 171)
black = (0,0,0)
green = (32, 171, 53)
red = (224, 33, 11)
yellow = (222, 216, 38)
blue = (57, 96, 204)
purple = (150, 57, 204)
failColour = (250, 135, 135)

backgroundColour = white

barriors = []
adjacentNodes = ([1,0],[-1,0],[0,1],[0,-1])
leftMousePressed = False
rightMousePressed = False
LEFT = 1
RIGHT = 3
UP = 5
DOWN = 4
canDraw = True
sDown = False
eDown = False
sDefined = False
eDefined = False
startX = 0
startY = 0
endX = 0
endY = 0
activated = False

#lists = [parent,position,g,h,f]
openList = []
closedList = []
path = []

grid = []

for x in range(0,50):
    grid.append([0])
    for y in range(0,50):
        grid[x].extend([0])
running = True

while running:
    gridChange =0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                leftMousePressed = True
            elif event.button == RIGHT:
                rightMousePressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT:
                leftMousePressed = False
            if event.button == RIGHT:
                rightMousePressed = False
            if event.button == DOWN:
                if gridSize < 30:
                    gridSize = gridSize + 1
            elif event.button == UP:
                if gridSize >10:
                    gridSize = gridSize -1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                sDown = True
            elif event.key == pygame.K_e:
                eDown = True

            elif event.key == pygame.K_SPACE:
                activated = True
                openList.append([[startNumX,startNumY],startNumX,startNumY,0,0,0])
                found = False

            elif event.key == pygame.K_BACKSPACE:
                activated = False
                grid.clear()
                for x in range(0,50):
                    grid.append([0])
                    for y in range(0,50):
                        grid[x].extend([0])
                barriors.clear()
                sDefined = False
                eDefined = False
                openList.clear()
                closedList.clear()
                path.clear()
                backgroundColour = white
            elif event.key == pygame.K_m:
                grid = mazeGeneration(grid, gridSize,screenWidth,clock,screen)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                sDown = False
            elif event.key == pygame.K_e:
                eDown = False



    screen.fill(backgroundColour)

     


    if activated == False:
        if leftMousePressed == True:
            canDraw = True
            countX = 0
            mouseX, mouseY = pygame.mouse.get_pos()
            for x in range(0,screenWidth,gridSize):            
                countY = 0
                for y in range(0,screenHeight,gridSize):
                    if grid[countY][countX] == "s" and sDown == True:
                        grid[countY][countX] = 0

                    elif grid[countY][countX] == "e" and eDown == True:
                        grid[countY][countX] = 0

                    if x<=mouseX and y<=mouseY:
                        if x+gridSize >mouseX and y+gridSize > mouseY:
                            if sDown == False and eDown == False:
                                for i in barriors:
                                    if i[0] == countX and i[1] == countY:
                                        canDraw = False
                                if sDefined == True:
                                    if x == startX and y == startY:
                                        canDraw = False
                                if eDefined == True:
                                    if x == endX and y == endY:
                                        canDraw = False
                                if canDraw == True:
                                    if [countX,countY] in barriors:
                                        pass
                                    else:
                                        barriors.append([countX,countY])
                                        grid[countY][countX] = 1
                            elif sDown == True and eDown == False and (x != endX or y != endY):
                                startX = x
                                startY = y
                                startNumX = countX
                                startNumY = countY
                                sDefined = True
                                grid[countY][countX]= "s"
                            elif sDown == False and eDown == True and (x != startX or y != startY):
                                endX = x
                                endY = y
                                eDefined = True
                                endNumX = countX
                                endNumY = countY
                                grid[countY][countX]= "e"

                    countY = countY + 1
                countX = countX + 1

        elif rightMousePressed == True:
            mouseX, mouseY = pygame.mouse.get_pos()
            xCount = 0
            for x in range(0,screenWidth,gridSize):
                yCount = 0
                for y in range(0,screenHeight,gridSize):
                    if x<=mouseX and y<=mouseY:
                        if x+gridSize >mouseX and y+gridSize > mouseY:
                            if [xCount,yCount] in barriors:
                                barriors.remove([xCount,yCount])
                                grid[yCount][xCount] = 0
                    yCount = yCount + 1
                xCount = xCount +1
                                    




    xCount = 0
    for x in range(0,screenWidth,gridSize):
        pygame.draw.rect(screen,grey,(x,0,1,screenHeight))
        pygame.draw.rect(screen,grey,(0,x,screenWidth,1))
        yCount =0
        for y in range(0,screenHeight, gridSize):
            if grid[yCount][xCount] == "p":
                pygame.draw.rect(screen, yellow,(x,y,gridSize-1,gridSize-1))
            elif grid[yCount][xCount] == "u":
                pygame.draw.rect(screen, purple,(x,y,gridSize-1,gridSize-1))
            elif grid[yCount][xCount] == "x":
                pygame.draw.rect(screen, blue,(x,y,gridSize-1,gridSize-1))

            if grid[xCount][yCount] == 1 or grid[xCount][yCount]=="b":
                grid[xCount][yCount] = 1
                pygame.draw.rect(screen, black,(y,x,gridSize-1,gridSize-1))

                if [yCount,xCount] in barriors:
                    pass
                else:
                    barriors.append([yCount,xCount])



            yCount = yCount + 1
        xCount = xCount + 1
    #for x in barriors:
     #   grid[x[1]][x[0]]= 1

    if sDefined == True:
        if startNumX < screenWidth/gridSize and startNumY <screenHeight/gridSize:
            pygame.draw.rect(screen, green,(startNumX*gridSize, startNumY*gridSize, gridSize, gridSize))
    if eDefined == True:
        if endNumX < screenWidth/gridSize and endNumY <screenHeight/gridSize:
            pygame.draw.rect(screen, red,(endNumX*gridSize, endNumY*gridSize, gridSize,gridSize))


    if activated == True:
        #lists = [parent,position,position,g,h,f]
        if len(openList) > 0:
            if found == False:

                sort(openList)
                currentNode = openList[0]
                openList.pop(0)
                closedList.append(currentNode)
                grid[currentNode[2]][currentNode[1]] = "x"
                for x in adjacentNodes:
                    if (currentNode[1] + x[0] >= 0 and currentNode[1] + x[0] < screenWidth/gridSize) and (currentNode[2] + x[1] >= 0  and currentNode[2] + x[1] < screenHeight/gridSize):
                        
                        ignore = False
                        for i in closedList:
                            if currentNode[1] + x[0] ==i[1] and currentNode[2] + x[1] == i[2]:
                                ignore = True
                                if grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "e" and grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "s":
                                    grid[i[2]][i[1]] = "x"
                        for i in openList:
                            if currentNode[1] + x[0] ==i[1] and currentNode[2] + x[1] == i[2]:
                                if i[3] > currentNode[3]+1:
                                    i[0]= [currentNode[1],currentNode[2]]
                                    i[3] = currentNode[3] +1
                                    i[5] = i[3] + i[4]


                        if grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  == 1 or grid[currentNode[2]+x[1]][currentNode[1]+x[0]] =="x":
                            ignore == True
                        elif grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "u" and grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "x"and grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "s":
                            g = currentNode[3] + 1
                            h = (((currentNode[1] + x[0])-endNumX)**2)+(((currentNode[2] + x[1])-endNumY)**2)
                            f = g + h
                            openList.append([[currentNode[1],currentNode[2]],currentNode[1] + x[0],currentNode[2] + x[1],g,h,f])
                            if grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "e" and grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  != "s":
                                grid[currentNode[2] + x[1]][currentNode[1] + x[0]] = "u"


                        if grid[currentNode[2]+x[1]][currentNode[1]+x[0]]  == "e":
                            found = True
                            parentg = currentNode[3]
                            parent = currentNode[1],currentNode[2]

            elif found == True:
                for i in range(0,parentg):
                    path.append([parent[0],parent[1]])
                    grid[parent[1]][parent[0]] = "p"
                    for j in closedList:
                        if j[1] == parent[0] and j[2] == parent[1]:
                            parent = j[0]
                activated = False
        else:
            backgroundColour = failColour








    clock.tick(30)
    pygame.display.flip()

pygame.quit()
