import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk


#GLOBAL VARIABLES
openedImage=None #Opened image
rowSize=0
columnSize=0
pix=None #Opened image as a pixel map
labelValue=None #Opened image as a labeled map according to siyah beyaz pixel map
pixelValue=None #Black and white pixel map
layerCount=0


window = tk.Tk()
window.title("Programing Studio")

img = Label(window) #Define basic image board on window



def openFile(): #Read image file
    fp = open(".\\simple.png", "rb") #Read file as a byte map
    global openedImage
    openedImage = Image.open(fp) #Byte map to images
    imageProcess()



def imageProcess():
    global pix
    pix = openedImage.load() #Images to pixel map
    global rowSize,columnSize
    rowSize,columnSize=openedImage.size #Get images width and height


    print(rowSize,columnSize)


    for i in range(rowSize):
        for j in range(columnSize):
            pix[i,j] = cleanNoise(pix[i,j]) # Clean gray pixels -> Black/White imagemenu.add_cascade(label = "File", menu = fileMenu)
            if (i == 0) or (j == 0) or (i == rowSize-1) or (j == columnSize-1):
                pix[i, j] = (0, 0, 0) #Frames with formal black

    global pixelValue
    pixelValue = [[0 for x in range(columnSize)] for y in range(rowSize)]  # Set pixelValue sizes

    for i in range(1, rowSize - 1):
        for j in range(1, columnSize - 1):
            pixelValue[i][j] = convertToBinary(pix[i, j])  # Give value to pixels -> White:1 and Black:0

    for j in range(1, columnSize - 1):
        for i in range(1, rowSize - 1):
            print(pixelValue[i][j], end='')  # Print w/b pixel map
        print("")



    defImg = ImageTk.PhotoImage(openedImage)
    img.config(image=defImg)
    img.image = defImg
    img.place(x=0, y=0)
    print("img size:", "height size=", rowSize, "and width size=", columnSize)







def convertToBinary(Value):
    #Create w/b pixel map - binary map
    if len(Value) == 4:
        r, g, b, op = Value #opacity
    else:
        r, g, b = Value

    average = (r + g + b) / 3

    if average == 255:
        return 1
    else:
        return 0


def cleanNoise(Value):
    #Clean gray pixel according to RGB average
    global isImgOpened
    if len(Value) == 4: #opacity
        r, g, b, op = Value
    else:
        r, g, b = Value

    average = (r + g + b) / 3

    if average > 200:
        return 255, 255, 255
    else:
        return 0, 0, 0


openFile()


window.mainloop()