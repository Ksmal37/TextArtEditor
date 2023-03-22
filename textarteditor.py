import timeit
import os
from PIL import Image,ImageDraw,ImageFont

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
    out = '\n'.join([''.join([chr(i) for i in row]) for row in c])
    return out

def drawSquare(c,x,y,width,height,fillval = 0):
    for i in range(x,x+width,-1 if width<0 else 1):
        for j in range(y,y+height,-1 if height<0 else 1):
            c[j][i] = fillval

def drawShape(c,shape,points,fillval = 0):
    if len(points) == 0:
        return
    if shape == 1  and len(points) == 2:
        drawSquare(c,*points[0],points[1][0]-points[0][0],points[1][1]-points[0][1],fillval)
    elif shape == 2 and len(points) == 2:
        drawVerticalLine(c,*points[0],points[1][1]-points[0][1],fillval)
    elif shape == 3 and len(points) == 2:
        drawHorizontalLine(c,*points[0],points[1][0]-points[0][0],fillval)

def drawVerticalLine(c,x,y,height,fillval = 0):
    for i in range(y,y+height,-1 if height < 0 else 1):
        c[i][x] = fillval

def drawHorizontalLine(c,x,y,width,fillval = 0):
    for i in range(x,x+width,-1 if width<0 else 1):
        c[y][i] = fillval

def drawCircle(c,cx,cy,r,fillval = 0):
    for x in range(cx-r,cx+r):
        for y in range(cy-r,cy+r):
            if ((x-cx)**2 + (y-cy)**2 ) == r**2:
                setPixel(c,x,y,fillval)


        
    

def blitTo(c1,c2,dims):
    for x in range(dims[0]):
        for y in range(dims[1]):
            c2[y][x] = c1[y][x]

def clamp(n,x,y):
    return min(y,max(x,n))

def editingSession(canvas,width,height,name):
    running = True
    cursor = [0,0]
    penchar = 65
    shape = [0,[]]
    screen = createCanvas(width,height,0)
    autodraw = False
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        blitTo(canvas,screen,[width,height])
        setPixel(screen,*cursor,94)
        drawShape(screen,shape[0],shape[1]+[cursor],penchar)
        print(getOutput(screen))
        print('-'*width)
        print(f"Pen : {chr(penchar)}\nShape : {shape}\nCursor : {cursor}")
        command = input('>>')
        if command == 'd':
            cursor[0] += 1
        elif command == 'a':
            cursor[0] -= 1
        elif command == 's':
            cursor[1] += 1
        elif command == 'w':
            cursor[1] -= 1
        elif command.startswith("c") and len(command) > 1:
            penchar = ord(command[1])
        elif len(command) == 0:
            if shape[0] > 0:
                shape[1].append(cursor[:])
                if (shape[0] == 1 or shape[0] == 2 or shape[0] == 3) and len(shape[1]) == 2:            
                    drawShape(canvas,shape[0],shape[1],penchar)
                    shape[1] = []
                    shape[0] = 0
            else:
                setPixel(canvas,*cursor,penchar)
        elif command == 'shr':
            shape[0] = 1
        elif command == 'shv':
            shape[0] = 2
        elif command == 'shh':
            shape[0] = 3
        elif command == 'sho':
            shape[0] = 0
            points = []
        elif command == 'o':
            autodraw = not autodraw
        elif command == 'fill':
            canvas = createCanvas(width,height,penchar)
        elif command.startswith('text') and len(command)>4:
            for a,char in enumerate(command[4:]):
                if cursor[0]+a >=width:
                    break
                setPixel(canvas,cursor[0]+a,cursor[1],ord(char))
        elif command.startswith('save') and len(command)>4:
            if command[4:].isnumeric():
                saveCanvas(canvas,width,height,fontsize = int(command[4:]),name = f"{name}.png")
                input()
        elif command == 'help':
            print('wasd - moving the cursor')
            print('c$ - change the pen character to $')
            print('[empty] - draw where the cursor is, or choose the next point when drawing a shape')
            print('shr - start drawing a rectangle')
            print('shv - start drawing a vertical line')
            print('shh - start drawing a horizontal line')
            print('sho - cancel shape')
            print('fill - fill canvas with the current pen character')
            print('o - turn autodraw on/off')
            print('save{num} - saves the canvas as an image with the font size num')
            print('quit - exits the editor')
            input()
        elif command == 'quit':
            running = False
            

        cursor[0] = clamp(cursor[0],0,width-1)
        cursor[1] = clamp(cursor[1],0,height-1)
        if autodraw:
          setPixel(canvas,*cursor,penchar)


def saveCanvas(c,cw,ch,fontsize = 16,fontpath = None,bg = (0,0,0),fg = (255,255,255),name = 'out.png'):
    if fontpath == None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(fontpath,size = fontsize)
    end = []
    for row in c:
        end.extend([chr(i) for i in row])
    end = [font.getbbox(i) for i in end]
    #Optimal character size
    widths = [i[2]-i[0] for i in end]
    heights = [i[3] - i[1] for i in end]
    optwidth = max(widths)
    optheight = max(heights)
    leftmargin = -(end[widths.index(optwidth)][0])
    upmargin = -(end[heights.index(optheight)][1])
    optheight+=3
    cnvimg = Image.new(mode = 'RGB',size = (optwidth*cw,optheight*ch),color = bg)
    cnvdraw = ImageDraw.Draw(cnvimg)
    for a,row in enumerate(c):
        for b,block in enumerate(row):
            charsize = font.getbbox(chr(block))
            charwidth = charsize[2]-charsize[0]
            charheight = charsize[3]-charsize[1]
            cnvdraw.text((leftmargin,upmargin),chr(block),font = font,fill = fg)
            leftmargin += optwidth
        leftmargin = 0
        upmargin+=optheight

    cnvimg.show()
    cnvimg.save(name)
    

def newSession():
    name = input('Project Name:')
    width = int(input('Width:'))
    height = int(input('Height:'))
    canvas = createCanvas(width,height,65)
    editingSession(canvas,width,height,name)
    
if __name__ == "__main__":
    newSession()
    
