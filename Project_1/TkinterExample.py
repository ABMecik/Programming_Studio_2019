import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk


openedImage=None
pixelMap=None
framedImage=None
nCol, nRow, orNRow, orNCol = 0,0,0,0
pixelMapAsString=""

root = tk.Tk() #Define GUI
xSize,ySize = 1200,900
size = str(xSize)+"x"+str(ySize)
root.geometry(size)
root.title("Programing Studio")
root.configure(bg='white')



for r in range(3):
    for c in range(3):
        if r == 0:
            Label(root, bg='white').grid(row=r, column=c, padx=(xSize/6)-15, pady=20)
        else:
            Label(root, bg='white', text="test").grid(row=r, column=c, padx=(xSize/6)-15, pady=(ySize*2/9))


def openImage():
    try:
        openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
        path = askopenfilename(parent=root, filetypes=openFileFormats)  # Basic file pick gui
        fp = open(path, "rb")  # Read file as a byte map

        global openedImage
        openedImage = Image.open(fp).convert('1', dither=Image.NONE)  # Byte map to images
    except:
        reset()

    imageProcess()

def imageProcess():
    global openedImage
    nCol, nRow = openedImage.size
    print("-------------------------------------------")
    print("Image size : \nHorizontal : ",nCol,"\nVertical : ", nRow)
    print("-------------------------------------------")

    colorMap = openedImage.load() # Images to pixel map

    global framedImage
    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE)

    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1])

    colorMap = framedImage.load()
    orNCol,orNRow=nCol,nRow

    nCol, nRow = framedImage.size
    print("-------------------------------------------")
    print("Framed Image size : \nHorizontal : ", nCol, "\nVertical : ", nRow)
    print("-------------------------------------------")


    global pixelMap
    pixelMap = [[0 for x in range(nCol)] for y in range(nRow)]  # Set pixelValue sizes

    global pixelMapAsString

    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] == 0:
                pixelMap[r][c] = 0
            else:
                pixelMap[r][c] = 1
            pixelMapAsString +=  str(pixelMap[r][c])
        pixelMapAsString += "\n"

    print(pixelMapAsString)

    # image
    defImg = ImageTk.PhotoImage(framedImage) # for absulute img or path u can use file=[path] and any os seperator : os.path.sep
    img1 = Label(root, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
    img1.config(image=defImg)
    img1.image = defImg
    img1.grid(row=1, column=0, sticky=W + E + N + S)


def reset():
    print("")

def writeBinaryToScreen():
    global binaryCanvas
    global pixelMapAsString
    fontSize = 3

    binaryCanvas.create_text(200,25, text=pixelMapAsString, font=("Times New Roman", fontSize, "bold"), tag="lvTag")  # "Times New Roman" , "bold"
    # for remove text from canvas use tag
    #binaryCanvas.select_clear()
    #binaryCanvas.delete("lvTag")
    binaryCanvas.update()

writeBinaryButton = Button(root, text='Binary', borderwidth=1, command=writeBinaryToScreen, relief=RAISED)
writeBinaryButton.grid(row=0, column=2, sticky=NE, padx=20, pady=20)


selectButton = Button(root, text='Open', borderwidth=1, command=openImage, relief=RAISED)
#selectButtonImage = ImageTk.PhotoImage([path])  # for any os seperator : os.path.sep
#selectButton.config(image=lvButtonTabImg)
#selectButton.image = lvButtonTabImg
selectButton.grid(row=0, column=0, sticky=NW, padx=20, pady=20)

binaryLabel = Label(root, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
binaryLabel.grid(row=1, column=1, sticky=W+E+N+S)

binaryCanvas = Canvas(binaryLabel)
binaryCanvas.grid(row=0, column=0, sticky=W+E+N+S)

root.mainloop()