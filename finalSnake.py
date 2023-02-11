from random import randint
import random
from pygame import *
import sys
import os

init()

# colors
White = (255, 255, 255)
lightGrey = (235, 235, 235)
Black = (0, 0, 0)
Blue = (0, 0, 255)
Red = (255, 50, 50)
Green = (30 , 163, 55)
DarkGreen = (0, 107, 20)

# fonts
font1 = font.Font('freesansbold.ttf', 9)
font2 = font.Font('freesansbold.ttf', 30)

#screen and cell sizes
#input your desired screen dimensions,border thickness , number of cells per row and column here
(screenWidth, screenHeight) = (800, 800)
numberOfCellsPerRow =10
numberOfCellsPerColumn = 10
borderThickness = 1

cellWidth = screenWidth/numberOfCellsPerRow
cellHeight = screenHeight/numberOfCellsPerColumn
snakeWidth = cellWidth-(cellWidth*0.2)
snakeHeight = cellHeight-(cellHeight *0.2)
snakeWidthOffset = (cellWidth*0.1)
snakeHeightOffset = (cellHeight *0.1)
borderColor = Black
snakeColor = Blue
snakeHeadColor = DarkGreen
appleColor = Red
appleWidth = cellWidth-(cellWidth*0.2)
appleHeight = cellHeight-(cellHeight *0.2)
appleWidthOffset = (cellWidth*0.1)
appleHeightOffset = (cellHeight *0.1)

FPS = time.Clock()

# transform to 1D list function 
def tranfsorm2Dto1D(tup2d):
    return (tup2d[0]+(tup2d[1]*numberOfCellsPerRow))
#  transform back to 2d vector 
def tranfsorm1Dto2D(tup1d):
    if(isinstance(tup1d , int)):
        return (tup1d % numberOfCellsPerRow, tup1d // numberOfCellsPerRow)
    else:
        return (tup1d[0] % numberOfCellsPerRow, tup1d[0] // numberOfCellsPerRow)

# y = 1 -> down, y = -1 -> up, y = 0 -> we are moving in x-axis >>>>> x = 1 -> right, x = -1 -> left, x = 0, we are moving in y-axis and so on
#inital snake direction
xDirect = 1
yDirect = 0

debug = False
GameOver = False
frames = 1

snakePos = [(0,0),(1,0),(2,0)]
applePos= ()
instructions = []
instructionsCounter = 0

chasingTail = False
snakePos1D = []

#generating graph for the algorithms
graph = {}

def createEdges(indexNumber):
    list = []
    #upper edge
    if not (indexNumber < numberOfCellsPerRow):
        list.append(indexNumber-numberOfCellsPerRow)
    #left edge
    if(indexNumber ) % numberOfCellsPerRow != 0:
        list.append(indexNumber-1)
    #right edge
    if(indexNumber + 1) % numberOfCellsPerRow != 0:
        list.append(indexNumber+1)
    #lower edge
    if indexNumber < ((numberOfCellsPerColumn*numberOfCellsPerRow)-numberOfCellsPerRow):
        list.append(indexNumber+numberOfCellsPerRow)
    print(len(list), end='')
    return tuple(list)

def generateGraph():
    global graph
    for i in range(0 ,numberOfCellsPerRow):
        for j in range(0 ,numberOfCellsPerColumn):
            graph[j+(i*numberOfCellsPerColumn)] = createEdges(j+(i*numberOfCellsPerColumn))

##################################################################################################
##########################################  algorithms  ##########################################
##################################################################################################
##################################### A* #####################################
# reconstruct the path returned from Astar algorithm
def reconstruct_path(path:dict, current):
    final_path = [current]
    while current in path.keys():
        current = path[current]
        final_path.append(current)
    return final_path

def Astar(graph, start, goal, occupiedBySnake):
    evaluated = []
    explored = [start]
    current = start
    path = {}
    gScore = 0
    hScore = 0
    fScore = 0

    while explored:
        fLowest = abs(explored[0][0] - start[0]) + abs(explored[0][1] + start[1]) + abs(explored[0][0] - goal[0]) + abs(explored[0][1] - goal[1])
        for i in range(len(explored)):
            if explored[i] not in occupiedBySnake:
                current = explored[i]
                break
        for i in explored:
            fTemp = abs(i[0] - start[0]) + abs(i[1] + start[1]) + abs(i[0] - goal[0]) + abs(i[1] - goal[1])
            if fTemp < fLowest and i not in occupiedBySnake:
                fLowest = fTemp
                current = i
                
        gScore = abs(current[0] - start[0]) + abs(current[1] + start[1])
        hScore = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        fScore = gScore + hScore

        if current == goal:
            return reconstruct_path(path, current)

        try:
            explored.remove(current)
        except:
            break
  
        evaluated.append(current)

        for i in graph[tranfsorm2Dto1D(current)]:
            i = tranfsorm1Dto2D(i)
            neighborGSCORE = abs(i[0] - start[0]) + abs(i[1] + start[1])
            neighborHSCORE = abs(i[0] - goal[0]) + abs(i[1] - goal[1])
            neighborFSCORE = neighborGSCORE + neighborHSCORE
            if i in evaluated:
                continue

            temp_gScore = gScore + abs(current[0] + i[0]) + abs(current[1] + i[1])

            if i not in explored:
                explored.append(i)
            elif temp_gScore > neighborGSCORE:
                continue

            path[i] = current
            neighborGSCORE = temp_gScore
            neighborFSCORE = neighborGSCORE + neighborHSCORE

##################################### Hamiltonian #####################################
def hamilton(graph, start, occupiedBySnake):
    size = len(graph)

    path = [start]

    previous_cell = path[0]
    previous_direction = None
    
    while len(path) < size:
        if  tranfsorm2Dto1D(previous_cell) in graph and tranfsorm2Dto1D((previous_cell[0] + 1, previous_cell[1])) in graph[tranfsorm2Dto1D(previous_cell)] and previous_direction != 'right' and (previous_cell[0] + 1, previous_cell[1]) not in path :
            path.append((previous_cell[0] + 1, previous_cell[1]))
            previous_cell = (previous_cell[0] + 1, previous_cell[1])
            previous_direction = 'left'
        elif tranfsorm2Dto1D(previous_cell) in graph and tranfsorm2Dto1D((previous_cell[0], previous_cell[1] + 1)) in graph[tranfsorm2Dto1D(previous_cell)] and previous_direction != 'down' and (previous_cell[0], previous_cell[1] + 1) not in path :
            path.append((previous_cell[0], previous_cell[1] + 1))
            previous_cell = (previous_cell[0], previous_cell[1] + 1)
            previous_direction = 'up'
        elif tranfsorm2Dto1D(previous_cell) in graph and tranfsorm2Dto1D((previous_cell[0] - 1, previous_cell[1])) in graph[tranfsorm2Dto1D(previous_cell)] and previous_direction != 'left' and (previous_cell[0] - 1, previous_cell[1]) not in path :
            path.append((previous_cell[0] - 1, previous_cell[1]))
            previous_cell = (previous_cell[0] - 1, previous_cell[1])
            previous_direction = 'right'
        elif tranfsorm2Dto1D(previous_cell) in graph and tranfsorm2Dto1D((previous_cell[0], previous_cell[1] - 1)) in graph[tranfsorm2Dto1D(previous_cell)] and previous_direction != 'up' and (previous_cell[0], previous_cell[1] - 1) not in path :
            path.append((previous_cell[0], previous_cell[1] - 1))
            previous_cell = (previous_cell[0], previous_cell[1] - 1)
            previous_direction = 'down'

    path.append(start)
    
    return path

######################### bfs algorithm ##############################
#graph => generated graph , start=>snakehead in 1d , goal => applePosition , occupiedBySnake =>list containing snake pos in 1d 
def BFS(graph, start, goal, occupiedBySnake , checkReverse = True  , isAfterApple = True ):
    global chasingTail
    global applePos
    
    explored = [ ]
    if(not isAfterApple):
        explored.append(tranfsorm2Dto1D(applePos))
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # If the desired node is
    # reached
    if start == goal:
        return queue
     
    # Loop to traverse the graph
    # with the help of the queue
    while len(queue)!= 0:
        path = queue.pop(-1)
        node = path[-1]

        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
            #make the snake aware of the changes happening to its body while it is following a path
            occupiedBySnakeForThisPath = list(occupiedBySnake)       
            for i in path :
                if(i not in occupiedBySnakeForThisPath):
                    occupiedBySnakeForThisPath.append(i)
                    occupiedBySnakeForThisPath.pop(0)
        
            # Loop to iterate over the
            # neighbours of the node            
            for neighbour in neighbours:  
                if(neighbour not in occupiedBySnakeForThisPath or (len(path) == 1 and neighbour == occupiedBySnakeForThisPath[0])):    
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.insert(0 , new_path)    

                    
                # Condition to check if the
                # neighbour node is the goal
                    if neighbour == goal:
                        
                        #check if there is reverse path in order not to get stuck
                        if(checkReverse):
                            occupiedBySnakeForThisPath = list(occupiedBySnake) 
                            bodyOffset = 1 if isAfterApple else 0
                            for i in range (0 , len(new_path)):
                                if(i>bodyOffset ):
                                    occupiedBySnakeForThisPath.pop(0)
                                occupiedBySnakeForThisPath.append(new_path[i])
                            if(BFS(graph , occupiedBySnakeForThisPath[-1] , occupiedBySnakeForThisPath[0] , occupiedBySnakeForThisPath , checkReverse = False , isAfterApple= isAfterApple ) != None):
                                print('chasing shortest path')
                                return list(new_path)
                            else:
                                #print('refused : ' + str(new_path))
                                if(not chasingTail)  :
                                    print('chasing tail')
                                    chasingTail = True
                                    return BFS(graph , start , occupiedBySnake[0] , occupiedBySnake , checkReverse = False , isAfterApple= False )
                                else:
                                    return None                                      
                        else:
                            return list(new_path)
                                        
            explored.append(node) 
    #what to do if we can't find a direct shortest path   
    return None
    
#########################dfs algorithm##############################
#graph => generated graph , start=>snakehead in 1d , goal => applePosition , occupiedBySnake =>list containing snake pos in 1d 
def DFS(graph, start, goal, occupiedBySnake , checkReverse = True  , isAfterApple = True ):
    global chasingTail
    global applePos
    
    explored = [ ]
    if(not isAfterApple):
        explored.append(tranfsorm2Dto1D(applePos))
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # If the desired node is
    # reached
    if start == goal:
        return queue
     
    # Loop to traverse the graph
    # with the help of the queue
    while len(queue)!= 0:
        path = queue.pop(-1)
        node = path[-1]
         
        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]
            #make the snake aware of the changes happening to its body while it is following a path
            occupiedBySnakeForThisPath = list(occupiedBySnake)       
            for i in path :
                if(i not in occupiedBySnakeForThisPath):
                    occupiedBySnakeForThisPath.append(i)
                    occupiedBySnakeForThisPath.pop(0)
        
            # Loop to iterate over the
            # neighbours of the node            
            for neighbour in neighbours:  
                if(neighbour not in occupiedBySnakeForThisPath or (len(path) == 1 and neighbour == occupiedBySnakeForThisPath[0])):    
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                # Condition to check if the
                # neighbour node is the goal
                    if neighbour == goal:
                        
                        #check if there is reverse path in order not to get stuck
                        if(checkReverse):
                            occupiedBySnakeForThisPath = list(occupiedBySnake) 
                            bodyOffset = 1 if isAfterApple else 0
                            for i in range (0 , len(new_path)):
                                if(i>bodyOffset ):
                                    occupiedBySnakeForThisPath.pop(0)
                                occupiedBySnakeForThisPath.append(new_path[i])
                            if(DFS(graph , occupiedBySnakeForThisPath[-1] , occupiedBySnakeForThisPath[0] , occupiedBySnakeForThisPath , checkReverse = False , isAfterApple= isAfterApple ) != None):
                                print('chasing shortest path')
                                return list(new_path)
                            else:
                                #print('refused : ' + str(new_path))
                                if(not chasingTail)  :
                                    print('chasing tail')
                                    chasingTail = True
                                    return DFS(graph , start , occupiedBySnake[0] , occupiedBySnake , checkReverse = False , isAfterApple= False )
                                else:
                                    return None                                      
                        else:
                            return list(new_path)
                                        
            explored.append(node) 
    #what to do if we can't find a direct shortest path   
    return None

###################################################################################################
###### updating snake information , apple information , taking and updating instructions ######
###################################################################################################
# reset instructions counter and replace instructions with the new one
def takeNewInstructions(instructionList):
    global instructions 
    global instructionsCounter
    instructionsCounter = 0
    instructions = instructionList

# procees every index in instructions list
def processInstructions():
    global instructionsCounter
    global instructions
    global xDirect
    global yDirect
    global GameOver
    global chasingTail
    try:
        xDirect = instructions[instructionsCounter][0]
        yDirect = instructions[instructionsCounter][1]
    except:
        makeNewInstructions()
    if (len(instructions) != 1):
        instructionsCounter+=1
    updateSnakePos()
   
def bfs_work():
    global graph
    global snakePos
    global applePos
    global instructions
    global GameOver
    global snakePos1D
    global chasingTail
    
    ### make moves list from bfs ###
    snakePose1D = [tranfsorm2Dto1D(cell) for cell in snakePos]
    arr = BFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), tranfsorm2Dto1D(applePos), snakePose1D , checkReverse=True , isAfterApple=True)
    if( chasingTail or arr == None):
            arr = None
            #we start testing random points based on their closeness to the apple
            allgraph = sorted( list(graph.keys()) , key=lambda x: abs(tranfsorm2Dto1D(applePos)-x) )
            for p in snakePose1D:
                allgraph.remove(p)
            while(arr == None and len(allgraph) !=0 and len(snakePos) != len(graph)-1):
                    chance = randint(0 , 4)
                    randomValue =  allgraph[0] if chance ==0 else allgraph[randint(0, len(allgraph)-1)]
                    allgraph.remove(randomValue)
                    arr = BFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), randomValue , snakePose1D , checkReverse=True , isAfterApple=False )

            if(arr == None):
                    #try chasing tail
                    arr = BFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), tranfsorm2Dto1D(snakePos[0]), snakePose1D , checkReverse=True , isAfterApple=False )
            for i in range(1 ,   (len(arr)-1)):
                arr.pop()    
            chasingTail = False
    
    movesList = []

    cellsList = [tranfsorm1Dto2D(place) for place in arr]
    if len(arr) == 1:
         movesList.append((cellsList[0][0] - snakePos[len(snakePos)-1][0], cellsList[0][1] - snakePos[len(snakePos)-1][1]))
    for i in range(len(cellsList)-1):
         movesList.append((cellsList[i+1][0] - cellsList[i][0], cellsList[i+1][1] - cellsList[i][1]))

    takeNewInstructions(movesList)


def A_star_work():
    global graph
    global snakePos
    global applePos
    
    movesList = []

    ### make moves list from A* algorithm ###
    AstartARR = Astar(graph, snakePos[len(snakePos)-1], applePos, snakePos)

    allgraph = sorted( list(graph.keys()) )
    while(AstartARR == None):
        if len(allgraph) !=0:
            randomValue =  tranfsorm1Dto2D(allgraph[randint(0, len(allgraph)-1)])
            allgraph.remove(tranfsorm2Dto1D(randomValue))
            AstartARR = Astar(graph, snakePos[len(snakePos)-1], randomValue , snakePos) 
        if(AstartARR == None):
            AstartARR = Astar(graph, snakePos[len(snakePos)-1], snakePos[0], snakePos)
        if(AstartARR == None):
            AstartARR = Astar(graph, snakePos[len(snakePos)-1], applePos, snakePos)

    for i in range(len(AstartARR)-2, -1, -1):
       movesList.append((AstartARR[i][0] - AstartARR[i+1][0], AstartARR[i][1] - AstartARR[i+1][1]))

    takeNewInstructions(movesList)

def hamiltonian_work():
    global graph
    global snakePos
    
    movesList = []

    # makes move list from hamiltonian algorithm
    HamiltonianARR = hamilton(graph, snakePos[len(snakePos) - 1], snakePos)
    for i in range(len(HamiltonianARR)-1):
        movesList.append((HamiltonianARR[i+1][0] - HamiltonianARR[i][0], HamiltonianARR[i+1][1] - HamiltonianARR[i][1]))

    takeNewInstructions(movesList)

def dfs_work():
    global graph
    global snakePos
    global applePos
    global instructions
    global GameOver
    global snakePos1D
    global chasingTail
    
    ### make moves list from dfs ###
    snakePose1D = [tranfsorm2Dto1D(cell) for cell in snakePos]
    arr = DFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), tranfsorm2Dto1D(applePos), snakePose1D , checkReverse=True , isAfterApple=True)
    if( chasingTail or arr == None):
            arr = None
            #we start testing random points based on their closeness to the apple
            allgraph = sorted( list(graph.keys()) , key=lambda x: abs(tranfsorm2Dto1D(applePos)-x) )
            for p in snakePose1D:
                allgraph.remove(p)
            while(arr == None and len(allgraph) !=0):
                if len(allgraph) !=0:
                    chance = randint(0 , 4)
                    randomValue =  allgraph[-1] if chance ==0 else allgraph[randint(0, len(allgraph)-1)]
                    allgraph.remove(randomValue)
                    arr = DFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), randomValue , snakePose1D , checkReverse=True , isAfterApple=False )

            if(arr == None):
                    #try chasing tail
                    arr = DFS(graph, tranfsorm2Dto1D(snakePos[len(snakePos)-1]), tranfsorm2Dto1D(snakePos[0]), snakePose1D , checkReverse=False , isAfterApple=False )
            for i in range(1 ,   (len(arr)-1)):
                arr.pop()    
            chasingTail = False
    
    movesList = []

    cellsList = [tranfsorm1Dto2D(place) for place in arr]
    if len(arr) == 1:
         movesList.append((cellsList[0][0] - snakePos[len(snakePos)-1][0], cellsList[0][1] - snakePos[len(snakePos)-1][1]))
    for i in range(len(cellsList)-1):
         movesList.append((cellsList[i+1][0] - cellsList[i][0], cellsList[i+1][1] - cellsList[i][1]))

    takeNewInstructions(movesList)

# variable to choose algorithm >>> 1- bfs,  2- A*, 3- hCycle, 4- dfs
algorithmChoice = 0

# function to call whenever we want to make new instructions list
def makeNewInstructions():
    global algorithmChoice
    
    if algorithmChoice == 1:
        bfs_work()
    elif algorithmChoice == 2:
        A_star_work()
    elif algorithmChoice == 3:
        hamiltonian_work()
    elif algorithmChoice == 4:
        dfs_work()

# generate new apple postion when the snake eat it
def generateNewApplePos():
    global applePos
    global algorithmChoice

    newApplePos = (randint(0,numberOfCellsPerRow-1),randint(0,numberOfCellsPerColumn-1))
    while(newApplePos in snakePos):
        newApplePos = (randint(0,numberOfCellsPerRow-1),randint(0,numberOfCellsPerColumn-1))
    applePos = newApplePos
    if algorithmChoice != 3:
        makeNewInstructions()

# update snake position for every frame
def updateSnakePos():
    global snakePos
    global xDirect
    global yDirect
    global GameOver

    #will eat apple
    if((snakePos[len(snakePos)-1][0]+xDirect ,snakePos[len(snakePos)-1][1]+yDirect) == applePos):  
        snakePos.append(applePos)
        # check if snake won >> game overs
        if(len(snakePos) == len(graph)):
            GameOver = True
            return
        generateNewApplePos()
        return   
    else:
        snakePos.pop(0)
        snakePos.append((snakePos[len(snakePos)-1][0]+xDirect ,snakePos[len(snakePos)-1][1]+yDirect))

    # collision detection
    if snakePos[len(snakePos)-1][0] >= numberOfCellsPerRow or snakePos[len(snakePos)-1][0] < 0:
        GameOver = True
    elif snakePos[len(snakePos)-1][1] >= numberOfCellsPerColumn or snakePos[len(snakePos)-1][1] < 0:
        GameOver = True
    for i in range(len(snakePos)-1):
        if snakePos[len(snakePos)-1] == snakePos[i]:
            GameOver = True 
   
#initialization
generateGraph()
applePos = (3,0)

############################################################
######################### all drawing ######################
############################################################
# pygame Screen
screen = display.set_mode((screenWidth, screenHeight))
display.set_caption(" Clever Snake ")
display.flip()

# drawing the screen grid , cells , border
def drawScreen():
    global debug
    for i in range(numberOfCellsPerRow):
        for j in range(numberOfCellsPerColumn):
            draw.rect(screen, borderColor, Rect(i*cellWidth, j*cellHeight, cellWidth, cellHeight), borderThickness)
            
            # press d to show cells tuples
            if debug == True:
                text = font1.render(str(tranfsorm2Dto1D((i,j))), True, Black)
                text.set_alpha(90)
                textRect = text.get_rect()
                textRect.center = (i*cellWidth+20, j*cellHeight+20)
                screen.blit(text, textRect)

# drawing the apple
def drawApple():
    global applePos
    draw.rect(screen, appleColor, Rect(applePos[0]*cellWidth+appleWidthOffset, applePos[1]*cellHeight+appleHeightOffset, appleWidth, appleHeight), 0)

#drawing the snake
def drawSnake():
    global snakePos

    #drawing tail
    draw.rect(screen, Black, Rect(snakePos[0][0]*cellWidth+snakeWidthOffset, snakePos[0][1]*cellHeight+snakeHeightOffset, snakeWidth, snakeHeight), 0)
    #drawing body
    for index in range(1 , len(snakePos)-1):
        draw.rect(screen, snakeHeadColor, Rect(snakePos[index][0]*cellWidth+snakeWidthOffset, snakePos[index][1]*cellHeight+snakeHeightOffset, snakeWidth, snakeHeight), 0)
    #drawing head  
    draw.rect(screen, snakeColor, Rect(snakePos[len(snakePos)-1][0]*cellWidth+snakeWidthOffset, snakePos[len(snakePos)-1][1]*cellHeight+snakeHeightOffset, snakeWidth, snakeHeight), 0)

# this function will update everything that needs to be updated every frame 
def updateScreen():
    global debug
    global GameOver
    global frames
    global snakePos
    global applePos
    global instructions
    global algorithmChoice
 
    # Key data handler
    for Event in event.get():
        if Event.type == QUIT:
            quit() 
            exit()       
        if Event.type == KEYDOWN:
            if Event.key == K_ESCAPE:
                quit()
                exit()
            if Event.key == K_d:
                if debug == False:
                    debug = True
                else:
                    debug = False
            if Event.key == K_1:
                algorithmChoice = 1
            if Event.key == K_2:
                algorithmChoice = 2
            if Event.key == K_3:
                algorithmChoice = 3
            if Event.key == K_4:
                algorithmChoice = 4
            
            # restart game to observe more details
            if Event.key == K_r and GameOver == True:
                algorithmChoice = 0
                snakePos = [(0,0),(1,0),(2,0)]
                instructions = []
                applePos = (3, 0)
                makeNewInstructions()
                frames = 1
                GameOver = False
                
            # keys to increase or decrease frame rate
            #slow down
            if Event.key == K_DOWN:
                if(frames > 10):
                    frames -= 1
            #speed up
            if Event.key == K_UP:
                frames+=10
           
            if Event.key == K_g:
                GameOver = True
    
    # checking gameover
    if not GameOver:
        # display menu or snake itself
        if algorithmChoice == 0:
            display.flip()
            screen.fill(White)
            text1 = font2.render('1 - BFS', True, Black)
            text1.set_alpha(90)
            textRect1 = text1.get_rect()
            textRect1.center = (screenWidth*0.25, screenHeight*0.25)
            screen.blit(text1, textRect1)
            text2 = font2.render('2 - A*', True, Black)
            text2.set_alpha(90)
            textRect2 = text2.get_rect()
            textRect2.center = (screenWidth*0.75, screenHeight*0.25)
            screen.blit(text2, textRect2)
            text3 = font2.render('3 - HCycle', True, Black)
            text3.set_alpha(90)
            textRect3 = text3.get_rect()
            textRect3.center = (screenWidth*0.25, screenHeight*0.75)
            screen.blit(text3, textRect3)
            text4 = font2.render('4 - DFS', True, Black)
            text4.set_alpha(90)
            textRect4 = text4.get_rect()
            textRect4.center = (screenWidth*0.75, screenHeight*0.75)
            screen.blit(text4, textRect4)
        else:
            screen.fill(lightGrey)
            drawScreen()
            drawSnake()  
            drawApple()       
    else: 
        drawApple()  
        text = font2.render('Game Over ... press r to restart', True, Black)
        text.set_alpha(90)
        textRect = text.get_rect()
        textRect.center = (screenWidth/2, screenHeight/2)
        screen.blit(text, textRect) 

    display.update()
    FPS.tick(frames)  

# Main Loop to call functions
while True: 
    updateScreen()
    if (not GameOver):
        if algorithmChoice != 0:
            if(instructionsCounter < len(instructions)-1 ):
                processInstructions()
            else:
                if algorithmChoice != 3:
                    makeNewInstructions()
                processInstructions()
