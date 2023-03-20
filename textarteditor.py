import timeit
import os

#Necesseties (LOCKED):
#  - Creating and editing Text Art
#  - Cursor controls for editing art
#  - Drawing lines and shapes like circle,square,polygon
#  - Saving as image


def createCanvas(width,height,fillval = 0):
    c = []
    for i in range(height):
        c.append([fillval]*width)
    return c

def setPixel(c,x,y,val):
    c[y][x] = val

def getPixel(c,x,y,val):
    return c[y][x]

def getOutput(c):
    out = ''
    for row in c:
        for col in row:
            out += chr(col)
        out+='\n'
    return out

def drawSquare(c,x,y,width,height,fillval = 0):
    for i in range(x,x+width):
        for j in range(y,y+height):
            c[j][i] = fillval

def drawVerticalLine(c,x,y,height,fillval = 0):
    for i in range(y,y+height):
        c[i][x] = fillval

def drawHorizontalLine(c,x,y,width,fillval = 0):
    for i in range(x,x+width):
        c[y][i] = fillval



def editingSession(canvas,width,height):
    running = True
    cursor = [0,0]
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(getOutput(canvas))
        command = input('>>')
        if command == 'd':
            cursor[0] += 1
        elif command == 'a':
            cursor[0] -= 1
        elif command == 's':
            cursor[1] += 1
        elif command == 'w':
            cursor[1] -= 1
        elif command.startswith('p'):
            setPixel(canvas,*cursor,ord(command[1]))
            
        
        


canvas = createCanvas(20,10,65)
editingSession(canvas,20,10)

    
