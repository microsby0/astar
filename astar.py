import pygame, sys, math, time
from pygame.locals import *
import pprint

def getDataFromFile():
    mapfile = open(FILE_NAME,'r')
    lines=[]
    BOX_ROWS=0
    for line in mapfile:
        BOX_ROWS+=1
        lines.append(line)
    #increase each by 2 for buffer
    BOX_COLS=len(line)+1
    BOX_ROWS+=2
    return {"lines":lines,"BOX_ROWS":BOX_ROWS,"BOX_COLS":BOX_COLS}

def createGrid(lines,BOX_ROWS,BOX_COLS):
    grid=[[0 for x in range(BOX_COLS)] for x in range(BOX_ROWS)]
    currentRow=1
    currentCol=1
    for line in lines:
        for letter in line:
            if letter == "o":
                box=grid[currentRow][currentCol]=Box(currentRow,currentCol,0,0,0,"obstacle","")
                pygame.draw.rect(window,blue,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),0)
                pygame.draw.rect(window,white,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),1)
            elif letter == "e":
                box=grid[currentRow][currentCol]=Box(currentRow,currentCol,0,0,0,"empty","")
                pygame.draw.rect(window,black,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),0)
                pygame.draw.rect(window,white,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),1)
            currentCol+=1
        currentRow+=1
        currentCol=1
    box=grid[START_ROW][START_COL]
    pygame.draw.rect(window,green,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),0)
    pygame.draw.rect(window,white,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),1)

    box=grid[END_ROW][END_COL]
    pygame.draw.rect(window,red,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),0)
    pygame.draw.rect(window,white,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),1)

    return grid

def drawArrow(box):
    text = "->"
    font = pygame.font.Font(None, 30)
    arrowSurface = font.render(text, 0, white)

    if(box.row < box.parentBox.row):
        if(box.col==box.parentBox.col): #down
            arrowSurface = pygame.transform.rotate(arrowSurface,-90)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
        elif(box.col<box.parentBox.col): #down right
            arrowSurface = pygame.transform.rotate(arrowSurface,-40)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
        else: #down left
            arrowSurface = pygame.transform.rotate(arrowSurface,-140)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
    if(box.row==box.parentBox.row):
        if(box.col<box.parentBox.col): #right
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
        else:
            arrowSurface = pygame.transform.rotate(arrowSurface,180) #left
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
    if(box.row>box.parentBox.row):
        if(box.col==box.parentBox.col): #up
            arrowSurface = pygame.transform.rotate(arrowSurface,90)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
        elif(box.col < box.parentBox.col): #up right
            arrowSurface = pygame.transform.rotate(arrowSurface,40)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))
        else: #up left
            arrowSurface = pygame.transform.rotate(arrowSurface,140)
            window.blit(arrowSurface,((box.col)*BOX_WIDTH+(int(BOX_WIDTH/2)-10),(box.row)*BOX_HEIGHT+(int(BOX_HEIGHT/2)-15)))

def visit(box):
    calculateF(box)
    if(noFont==False):
        #Draw outline on screen
        pygame.draw.rect(window,green,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),2)
        font = pygame.font.Font(None, 17)
        #H value
        text = font.render(str(box.hvalue), 0, white)
        window.blit(text,(box.col*BOX_WIDTH+35,box.row*BOX_HEIGHT+35))
        #G value
        text = font.render(str(box.gvalue), 0, white)
        window.blit(text,(box.col*BOX_WIDTH+5,box.row*BOX_HEIGHT+35))
        #F value
        text = font.render(str(box.fvalue), 0, white)
        window.blit(text,(box.col*BOX_WIDTH+5,box.row*BOX_HEIGHT+5))

        #Parent arrow
        drawArrow(box)

    pygame.display.update()

def addToClosedList(box):
    openList.remove(box)
    closedList.append(box)
    pygame.draw.rect(window,blue,(box.col*BOX_WIDTH,box.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),2)
    pygame.display.update()
    time.sleep(speed)

def addToOpenList(box,parentBox):
    openList.append(box)
    box.parentBox=parentBox
    visit(box)

def calculateG(box,parentBox):
    row_diff = math.fabs(parentBox.row - box.row)
    col_diff = math.fabs(parentBox.col - box.col)
    if row_diff==1 and col_diff==1:
        return 14+parentBox.gvalue
    else:
        return 10+parentBox.gvalue

def calculateF(box):
    #H value
    col_diff = math.fabs(END_COL-box.col)
    row_diff = math.fabs(END_ROW-box.row)
    box.hvalue = int(10*(col_diff+row_diff))

    #G value
    box.gvalue=calculateG(box,box.parentBox)

    #F value
    box.fvalue = box.gvalue + box.hvalue

def addNeighborsToOpenList(box):
    #top and bottom rows
    if(box==grid[START_ROW][START_COL]):
        openList.append(box)
    for i in range(-1,2):
        #top 3 neighbors
        if(grid[box.row-1][box.col+i]!=0): #check its not a buffer square
            if(grid[box.row-1][box.col+i].state!="obstacle" and grid[box.row-1][box.col+i] not in closedList): #check its not an obstacle or in the closed list
                if(grid[box.row-1][box.col+i] in openList): #check for gvalue update if in open list
                    if(calculateG(grid[box.row-1][box.col+i],box)<grid[box.row-1][box.col+i].gvalue):
                        grid[box.row-1][box.col+i].parentBox=box
                else: #add to open list
                    if (i==1):
                        if(grid[box.row-1][box.col].state!="obstacle" and grid[box.row][box.col+1].state!="obstacle"):
                            addToOpenList(grid[box.row-1][box.col+i],box)
                    elif(i == -1):
                        if(grid[box.row-1][box.col].state!="obstacle" and grid[box.row][box.col-1].state!="obstacle"):
                            addToOpenList(grid[box.row-1][box.col+i],box)
                    else:
                        addToOpenList(grid[box.row-1][box.col+i],box)
        #bottom 3 neighbors
        if(grid[box.row+1][box.col+i]!=0):
            if(grid[box.row+1][box.col+i].state!="obstacle" and grid[box.row+1][box.col+i] not in closedList):
                if(grid[box.row+1][box.col+i] in openList):
                    if(calculateG(grid[box.row+1][box.col+i],box)<grid[box.row+1][box.col+i].gvalue):
                        grid[box.row+1][box.col+i].parentBox=box
                else:
                    if(i==1):
                        if(grid[box.row+1][box.col].state!="obstacle" and grid[box.row][box.col+1].state!="obstacle"):
                            addToOpenList(grid[box.row+1][box.col+i],box)
                    elif(i == -1):
                        if(grid[box.row+1][box.col].state!="obstacle" and grid[box.row][box.col-1].state!="obstacle"):
                            addToOpenList(grid[box.row+1][box.col+i],box)
                    else:
                        addToOpenList(grid[box.row+1][box.col+i],box)
    #two side boxes
    if(grid[box.row][box.col-1]!=0):
        if(grid[box.row][box.col-1].state!="obstacle" and grid[box.row][box.col-1] not in closedList):
            if(grid[box.row][box.col-1] in openList):
                    if(calculateG(grid[box.row][box.col-1],box)<grid[box.row][box.col-1].gvalue):
                        grid[box.row][box.col-1].parentBox=box
            else:
                addToOpenList(grid[box.row][box.col-1],box)
    if(grid[box.row][box.col+1]!=0):
        if(grid[box.row][box.col+1].state!="obstacle"  and grid[box.row][box.col+1] not in closedList):
            if(grid[box.row][box.col+1] in openList):
                    if(calculateG(grid[box.row][box.col+1],box)<grid[box.row][box.col+1].gvalue):
                        grid[box.row][box.col+1].parentBox=box
            else:
                addToOpenList(grid[box.row][box.col+1],box)

def createFinalMessage(steps):
    font = pygame.font.Font(None, 38)
    if(steps==0):
        text = font.render("Could not find the end", 0, white)
    else:
        text = font.render("Steps to end: " + str(steps), 0, white)
    window.blit(text,(int(window.get_width()/2)-150,window.get_height()-35))

class Box:
    def __init__(self,row,col,fvalue,gvalue,hvalue,state,parentBox):
        self.row=row
        self.col=col
        self.fvalue=fvalue
        self.gvalue=gvalue
        self.hvalue=hvalue
        self.state=state
        self.parentBox=parentBox

#Start/Finish Variables
START_COL=int(sys.argv[2])+1
START_ROW=int(sys.argv[4])+1
END_COL=int(sys.argv[6])+1
END_ROW=int(sys.argv[8])+1
FILE_NAME = sys.argv[10]

#Shape Variables
if("big" in sys.argv):
    noFont=True
    BOX_WIDTH=10
    BOX_HEIGHT=10
else:
    noFont=False
    BOX_WIDTH=50
    BOX_HEIGHT=50

fileData = getDataFromFile()

#Lists
openList=[]
closedList=[]

#Speed of animation
speed=0.5

#pygame variables
pygame.init()
window = pygame.display.set_mode((BOX_WIDTH*fileData["BOX_COLS"],BOX_HEIGHT*fileData["BOX_ROWS"]))
red = pygame.Color(255,0,0)
blue = pygame.Color(0,0,255)
lightblue = pygame.Color(0,0,100)
green = pygame.Color(0,255,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
yellow = pygame.Color(255,255,0)

grid=createGrid(fileData["lines"],fileData["BOX_ROWS"],fileData["BOX_COLS"])

#Actual search for end point
done=True
while done:
    if(len(openList)==0):
        addNeighborsToOpenList(grid[START_ROW][START_COL])
        addToClosedList(grid[START_ROW][START_COL])
    else:
        currentBox=openList[len(openList)-1]
        for box in openList:
            if(box.fvalue < currentBox.fvalue):
                currentBox=box
        addNeighborsToOpenList(currentBox)
        addToClosedList(currentBox)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if(speed>0.2):
                        speed-=0.1
                    print(speed)
                if event.key == K_DOWN:
                    if(speed<5.0):
                        speed+=0.1

        if(currentBox==grid[END_ROW][END_COL] or len(openList)==0):
            done=False

#Trace and highlight path back to start
steps=0
while currentBox!=grid[START_ROW][START_COL] and len(openList)!=0:
    pygame.draw.rect(window,yellow,(currentBox.col*BOX_WIDTH,currentBox.row*BOX_HEIGHT,BOX_WIDTH,BOX_HEIGHT),2)
    currentBox=currentBox.parentBox
    pygame.display.update()
    steps+=1
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if(speed>0.2):
                    speed-=0.1
                print(speed)
            if event.key == K_DOWN:
                if(speed<5.0):
                    speed+=0.1
    time.sleep(speed)

createFinalMessage(steps)

pygame.display.update()

#sleep so grid stays up for a while
time.sleep(200)