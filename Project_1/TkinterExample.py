import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk

#Global Variables
openedImage=None
binaryImage=None
framedImage=None
nCol, nRow, orNRow, orNCol = 0,0,0,0
pixelMapAsString=""


#GUI Creation
root = tk.Tk()
xSize,ySize = 900,600
size = str(xSize)+"x"+str(ySize)
root.geometry(size)
root.title("Programing Studio")
root.configure(bg='white')


#Main 2x2 GUI Grid Partioning
#You should implement 3x3
for r in range(2):
    for c in range(2):
        if r == 0:
            Label(root, bg='white').grid(row=r, column=c, padx=(xSize/6)-15, pady=20)
        else:
            Label(root, bg='white', text="test").grid(row=r, column=c, padx=(xSize*2/9)-15, pady=(ySize*2/6))

#Opening an image
def openImage():
    try:
        openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
        path = askopenfilename(parent=root, filetypes=openFileFormats)  # Basic file pick gui
        fp = open(path, "rb")  # Read file as a byte map

        global openedImage
        openedImage = Image.open(fp).convert('1', dither=Image.NONE)  # Convert byte map to Image then grayscaling of the image
    except:
        reset()

    imageProcess()

def imageProcess():
    global openedImage
    nCol, nRow = openedImage.size
    print("-------------------------------------------")
    print("Image size : \nHorizontal : ",nCol,"\nVertical : ", nRow)
    print("-------------------------------------------")

    colorMap = openedImage.load() # Images to pixel map because of converting return average of RGB

    global framedImage
    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE) #Creates an image with 2 additional columns and rows for framing edges
    #convert 1 : black white image
    #convert L : gray scaled image

    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1]) #Coloring framed image

    colorMap = framedImage.load() # Images to pixel map
    orNCol,orNRow=nCol,nRow

    nCol, nRow = framedImage.size
    print("-------------------------------------------")
    print("Framed Image size : \nHorizontal : ", nCol, "\nVertical : ", nRow)
    print("-------------------------------------------")


    global binaryImage
    binaryImage = [[0 for x in range(nCol)] for y in range(nRow)]  # Set pixelValue sizes

    global pixelMapAsString

    #Create binary image according to pixel map
    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] > 200:
                binaryImage[r][c] = 1
            else:
                binaryImage[r][c] = 0
            pixelMapAsString +=  str(binaryImage[r][c])
        pixelMapAsString += "\n"

    print(pixelMapAsString)

    # Putting image to screen
    global img1
    defImg = ImageTk.PhotoImage(framedImage) # for absulute img or path u can use file=[path] and any os seperator : os.path.sep
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()



def reset():
    print("")

def writeBinaryToScreen():
    global binaryCanvas
    global pixelMapAsString
    fontSize = 3

    binaryCanvas.create_text(0,0, text=pixelMapAsString, font=("Times New Roman", fontSize, "bold"), tag="lvTag", anchor=NW)  # "Times New Roman" , "bold"
    # for remove text from canvas use tag
    #binaryCanvas.select_clear()
    #binaryCanvas.delete("lvTag")

    #for update u can remove and write text for every iteration
    binaryCanvas.update()

writeBinaryButton = Button(root, text='Binary', borderwidth=1, command=writeBinaryToScreen, relief=RAISED)
writeBinaryButton.grid(row=0, column=1, sticky=NE, padx=20, pady=20)


selectButton = Button(root, text='Open', borderwidth=1, command=openImage, relief=RAISED)
#selectButtonImage = ImageTk.PhotoImage([path])  # for any os seperator : os.path.sep
#selectButton.config(image=lvButtonTabImg)
#selectButton.image = lvButtonTabImg
selectButton.grid(row=0, column=0, sticky=NW, padx=20, pady=20)

binaryCanvas = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
binaryCanvas.grid(row=1, column=1, sticky=W + E + N + S)

img1 = Label(root, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
img1.grid(row=1, column=0, sticky=W + E + N + S)

root.mainloop()
