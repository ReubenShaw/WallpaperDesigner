from enum import Enum
from tkinter import *
import tkinter.font as tf

class WallpaperQualities(Enum): #REDO, PRICES WRONG
    CHEAP = 0.03
    EXPENSIVE = 0.06

class WallpaperAdditions(Enum):
    NONE = 0
    EMBOSSING = 6
    FOIL = 12
    GLITTER = 18

class Windows(Enum):
    VIEW_WALLPAPER = 0
    VIEW_ORDER = 1

class Wallpaper:
    def __init__(self, firstDesign = True, colour: str = "purple", rolls: int = 0, quality: WallpaperQualities = WallpaperQualities.CHEAP, addition: WallpaperAdditions = WallpaperAdditions.NONE, liningPaper: bool = False, paste: bool = False) -> None:
        self.firstDesign = firstDesign
        self.colour = colour
        self.rolls = rolls

        self.quality = quality
        self.addition = addition
        self.liningPaper = liningPaper
        self.paste = paste
    
    def calcCost(self) -> float:
        pass


class Main:
    def __init__(self) -> None:
        self.mainLoop()
        
    def mainLoop(self) -> None:
        root = Tk()
        root.geometry("960x540")
        root.title("Wallpaper Designer")

        self.viewWallpaper = ViewWallpaper(root)
        self.viewWallpaper.drawWindow(root)

        root.mainloop()

        
    

class ViewWallpaper:
    def __init__(self, root: Tk) -> None:
        self.availableColours = ["purple", "DarkSlateGray4", "deep sky blue", "light sea green", "VioletRed2", "gold"]
        self.wallpaper = Wallpaper()
        self.order = []

        self.selectedOption = StringVar(root)
        self.selectedOption.set("Cheap      ")
        self.liningOp = IntVar()
        self.pasteOp = IntVar()
        self.modificationOp = StringVar(root, "NONE")
        self.rollsOp = StringVar(root, value=0)

        self.cvsMainDisp = Canvas()
        self.cvsFirstOp = Canvas()
        self.cvsSecondOp = Canvas()

    def drawWindow(self, root: Tk) -> None:
        frmL = Frame(root, bg="lightgray")
        frmL.place(anchor=W, relx=0.5, rely=0.5, relwidth=0.5, relheight=1)

        xStart = 32; yStart = 32
        self.cvsMainDisp = Canvas(frmL, width=126, height=126, bg="white")
        self.cvsMainDisp.place(anchor=NW, x=xStart, y=yStart)
        root.update()
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour, self.cvsMainDisp)

        self.cvsFirstOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsFirstOp.bind("<Button-1>", self.designClick)
        self.cvsFirstOp.place(anchor=NW, x=xStart, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()
        self.cvsSecondOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsSecondOp.bind("<Button-1>", self.designClick)
        self.cvsSecondOp.place(anchor=NW, x=self.cvsFirstOp.winfo_width()+xStart+15, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()

        Draw.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour, self.cvsMainDisp)
        Draw.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour, self.cvsMainDisp)


        cvsColours = []
        for i in range(len(self.availableColours)):
            cvsColours.append(Frame(frmL, width=self.cvsMainDisp.winfo_width()/7, height=self.cvsMainDisp.winfo_height()/7, bg=self.availableColours[i]))
            cvsColours[i].bind("<Button-1>", self.colourClick)
            cvsColours[i].place(anchor=NW, x=self.cvsMainDisp.winfo_width()+xStart+15, y=yStart+(i*2*self.cvsMainDisp.winfo_height()/7))

        xStart = 64
        lblQuality = Label(frmL, text="Choose Quality:", bg=frmL["background"])
        lblQuality.config(font=tf.Font(size=12))
        lblQuality.place(anchor=NE, x=frmL.winfo_width()-xStart-16, y=yStart)
        root.update()
        drpQuality = OptionMenu(frmL, self.selectedOption, "Cheap      ", *["Expensive"], command=self.qualitySelect)
        drpQuality.config(font=tf.Font(size=14), bg = "#C2C2C2")
        drpQuality.place(anchor=NE, x=frmL.winfo_width()-xStart, y=yStart+lblQuality.winfo_height())
        root.update()

        lblAdditions = Label(frmL, text="Additions", bg="darkgray")
        lblAdditions.config(font=tf.Font(size=12))
        lblAdditions.place(anchor=NE, x=frmL.winfo_width()-xStart+16, y=yStart+drpQuality.winfo_y()+48, width=drpQuality.winfo_width()+16)
        root.update()
        frmAdditions = Frame(frmL, bg="#C2C2C2")
        frmAdditions.place(anchor=NW, x=lblAdditions.winfo_x(), y=lblAdditions.winfo_y()+lblAdditions.winfo_height(), width=lblAdditions.winfo_width(), 
                           height=cvsColours[5].winfo_y()+cvsColours[5].winfo_height()-lblAdditions.winfo_y()-lblAdditions.winfo_height())
        root.update()
        chkLining = Checkbutton(frmAdditions, text="Lining Paper", variable=self.liningOp, bg=frmAdditions["background"], command=self.additionsSelect)
        chkLining.config(font=tf.Font(size=12))
        chkLining.place(anchor=NW, y=2)
        root.update()
        chkPaste = Checkbutton(frmAdditions, text="Wallpaper Paste", variable=self.pasteOp, bg=frmAdditions["background"], command=self.additionsSelect)
        chkPaste.config(font=tf.Font(size=12))
        chkPaste.place(anchor=NW, y=chkLining.winfo_height()+8)

        xStart = 32
        lblModifications = Label(frmL, text="Modifications", bg="darkgray")
        lblModifications.config(font=tf.Font(size=12))
        lblModifications.place(anchor=NW, x=xStart, y=self.cvsFirstOp.winfo_y()+self.cvsFirstOp.winfo_height()+128, width=self.cvsMainDisp.winfo_width()+cvsColours[0].winfo_width()+15)
        root.update()
        frmModifications = Frame(frmL, bg="#C2C2C2")
        frmModifications.place(anchor=NW, x=xStart, y=lblModifications.winfo_y()+lblModifications.winfo_height(), width=lblModifications.winfo_width(), height = 96)

        values = {"None" : "NONE",
                  "Foil" : "FOIL",
                  "Glitter" : "GLITTER",
                  "Embossing" : "EMBOSSING"}
        rdbModifications = []
        i = 0
        for (text, value) in values.items():
            Radiobutton(frmModifications, variable=self.modificationOp, text=text, value=value, bg=frmModifications["background"], command=self.modificationsSelect).place(anchor=NW, y=2+i*22)
            i+=1

        root.update()
        lblRolls = Label(frmL, text="Rolls", bg=frmL["background"])
        lblRolls.config(font=tf.Font(size=12))
        lblRolls.place(anchor=NW, x=lblAdditions.winfo_x(), y=lblModifications.winfo_y(), width=frmAdditions.winfo_width())
        root.update()
        spnRolls = Spinbox(frmL, from_=1, to=50, textvariable=self.rollsOp, command=self.rollsSelect)
        spnRolls.config(font=tf.Font(size=14))
        spnRolls.place(anchor=NW, x=lblRolls.winfo_x(), y=lblRolls.winfo_y()+lblRolls.winfo_height(), width=lblRolls.winfo_width())
        root.update()

        btnAdd = Button(frmL, text="Add to Basket", fg="white", bg="orange", command=self.addClick)
        btnAdd.config(font=tf.Font(size=12, weight="bold"))
        btnAdd.place(anchor=NW, x=lblRolls.winfo_x(), y=spnRolls.winfo_y()+spnRolls.winfo_height()+20, width=lblRolls.winfo_width(), height=48)


        lblTitle = Label(root, text="Design a new Wallpaper")
        lblTitle.config(font=tf.Font(size=28))
        lblTitle.place(anchor=NW, x=38, y=12)

        btnOrder = Button(root, text="View Order", fg="white", bg="orange")
        btnOrder.config(font=tf.Font(size=12, weight="bold"))
        btnOrder.place(anchor=SW, x=16, y=frmL.winfo_height()-16, width=lblRolls.winfo_width(), height=48)

    def colourClick(self, event: Event) -> None:
        caller = event.widget
        self.wallpaper.colour = caller["background"]
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour, self.cvsMainDisp)
        Draw.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour, self.cvsMainDisp)
        Draw.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour, self.cvsMainDisp)
    def designClick(self, event: Event) -> None:
        caller = event.widget
        if caller.winfo_name == self.cvsFirstOp.winfo_name:
            self.wallpaper.firstDesign = True
        else:
            self.wallpaper.firstDesign = False
        self.cvsMainDisp.delete("all")
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour, self.cvsMainDisp)

    def qualitySelect(self, selection: str) -> None:
        self.wallpaper.quality = WallpaperQualities[((selection).upper()).strip()]
    def additionsSelect(self) -> None:
        if self.liningOp.get() == 0:
            self.wallpaper.liningPaper = False
        else: self.wallpaper.liningPaper = True
        if self.pasteOp.get() == 0:
            self.wallpaper.paste = False
        else: self.wallpaper.paste = True
    def modificationsSelect(self) -> None:
        self.wallpaper.quality = WallpaperAdditions[self.modificationOp.get()]
    def rollsSelect(self) -> None:
        self.wallpaper.rolls = self.rollsOp.get()

    def addClick(self) -> None:
        self.order.append(self.wallpaper)

class Draw:
    def drawWallpaper(firstDesign: bool, canvas: Canvas, colour: str, cvsMainDisp: Canvas) -> None:
        cx = canvas.winfo_width(); cy = canvas.winfo_height()
        if firstDesign:
            sx = (int)(cx / 5); sy = (int)(cy / 5)

            for i in range(5):
                rsx = (sx / 2 * i); rsy = (sy / 2 * i)
                if i % 2 == 0:
                    fillCol = colour
                else:
                    fillCol = canvas["background"]
            
                canvas.create_rectangle(0 + rsx, 0 + rsy, sx + rsx, sy + rsy, fill=fillCol, outline=colour)
                canvas.create_rectangle(0 + rsx, cy - sy - rsy, sx + rsx, cy - rsy, fill=fillCol, outline=colour)
                canvas.create_rectangle(cx - rsx - sx, 0 + rsy, cx - rsx, sy + rsy, fill=fillCol, outline=colour)
                canvas.create_rectangle(cx - rsx - sx, cy - rsy - sy, cx - rsx, cy - rsy, fill=fillCol, outline=colour)
        else:
            mod = canvas.winfo_width() / cvsMainDisp.winfo_width()
            for y in range(2):
                startx=2; starty=(y + 1) * 40 - 15
                for x in range(5):
                    canvas.create_polygon((startx+12.5)*mod,(starty+0)*mod, 
                                          (startx+7.5)*mod,(starty+10)*mod, 
                                          (startx+0)*mod,(starty+10)*mod, 
                                          (startx+5)*mod,(starty+20)*mod, 
                                          (startx+0)*mod,(starty+30)*mod, 
                                          (startx+7.5)*mod,(starty+30)*mod, 
                                          (startx+12.5)*mod,(starty+40)*mod, 
                                          (startx+17.5)*mod,(starty+30)*mod, 
                                          (startx+25)*mod,(starty+30)*mod, 
                                          (startx+20)*mod,(starty+20)*mod, 
                                          (startx+25)*mod,(starty+10)*mod, 
                                          (startx+17.5)*mod,(starty+10)*mod, 
                                          (startx+12.5)*mod,(starty+0)*mod,
                                          fill=colour,
                                          outline=colour)
                    startx+=25

Main()