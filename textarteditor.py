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
	for i in range(x,x+width,-1 if width<0 else 1):
		for j in range(y,y+height,-1 if height<0 else 1):
			c[j][i] = fillval

def drawShape(c,shape,points):
	if shape == 1:
		drawSquare(canvas,*points[0],points[1][0]-points[0][0],points[1][1]-points[0][1],penchar)

def drawVerticalLine(c,x,y,height,fillval = 0):
	for i in range(y,y+height):
		c[i][x] = fillval

def drawHorizontalLine(c,x,y,width,fillval = 0):
	for i in range(x,x+width):
		c[y][i] = fillval

def blitTo(c1,c2,dims):
	for x in range(dims[0]):
		for y in range(dims[1]):
			c2[y][x] = c1[y][x]
	
def clamp(n,x,y):
	return min(y,max(x,n))
	
def editingSession(canvas,width,height):
	running = True
	cursor = [0,0]
	penchar = 65
	shape = 0
	points = []
	screen = createCanvas(width,height,0)
	while running:
		os.system('cls' if os.name == 'nt' else 'clear')
		blitTo(canvas,screen,[width,height])
		setPixel(screen,*cursor,94)
		print(getOutput(screen))
		print(f"Pen : {chr(penchar)}")
		command = input('>>')
		if command == 'd':
			cursor[0] += 1
		elif command == 'a':
			cursor[0] -= 1
		elif command == 's':
			cursor[1] += 1
		elif command == 'w':
			cursor[1] -= 1
		elif command.startswith("c"):
			penchar = ord(command[1])
		elif len(command) == 0:
			if shape > 0:
				points.append(cursor)
			if shape == 1:
				if len(points) == 2:
					drawSquare(canvas,*points[0],points[1][0]-points[0][0],points[1][1]-points[0][1],penchar)
					points = []
					shape = 0
				
				setPixel(canvas,*cursor,penchar)
			
		cursor[0] = clamp(cursor[0],0,width-1)
		cursor[1] = clamp(cursor[1],0,height-1)

width = 20
height = 10
canvas = createCanvas(width,height,65)
editingSession(canvas,width,height)
