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
    def __init__(self, firstDesign = True, colour: str = "purple", quality: WallpaperQualities = WallpaperQualities.CHEAP, addition: WallpaperAdditions = WallpaperAdditions.NONE, liningPaper: bool = False, paste: bool = False) -> None:
        self.firstDesign = firstDesign
        self.colour = colour
        
        self.quality = quality
        self.addition = addition
        self.liningPaper = liningPaper
        self.paste = paste
    
    def calcCost(self) -> float:
        pass


class Main:
    def __init__(self) -> None:
        self.availableColours = ["purple", "DarkSlateGray4", "deep sky blue", "light sea green", "VioletRed2", "gold"]
        self.wallpaper = Wallpaper()
        self.mainLoop()
        
    def mainLoop(self) -> None:
        root = Tk()
        root.geometry("960x540")
        root.title("Wallpaper Designer")

        self.selectedOption = StringVar(root)
        self.selectedOption.set("Cheap      ")

        self.cvsMainDisp = Canvas()
        self.cvsFirstOp = Canvas()
        self.cvsSecondOp = Canvas()
        self.drawWindow(root)

        root.mainloop()

    def drawWindow(self, root: Tk) -> None:
        frmL = Frame(root, bg="lightgray")
        frmL.place(anchor=W, relx=0.5, rely=0.5, relwidth=0.5, relheight=1)

        xStart = 32; yStart = 32
        self.cvsMainDisp = Canvas(frmL, width=126, height=126, bg="white")
        self.cvsMainDisp.place(anchor=NW, x=xStart, y=yStart)
        root.update()
        self.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)

        self.cvsFirstOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsFirstOp.bind("<Button-1>", self.designClick)
        self.cvsFirstOp.place(anchor=NW, x=xStart, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()
        self.cvsSecondOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsSecondOp.bind("<Button-1>", self.designClick)
        self.cvsSecondOp.place(anchor=NW, x=self.cvsFirstOp.winfo_width()+xStart+15, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()

        self.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour)
        self.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour)


        cvsColours = []
        for i in range(len(self.availableColours)):
            cvsColours.append(Frame(frmL, width=self.cvsMainDisp.winfo_width()/7, height=self.cvsMainDisp.winfo_height()/7, bg=self.availableColours[i]))
            cvsColours[i].bind("<Button-1>", self.colourClick)
            cvsColours[i].place(anchor=NW, x=self.cvsMainDisp.winfo_width()+xStart+15, y=yStart+(i*2*self.cvsMainDisp.winfo_height()/7))


        fontObj = tf.Font(size=10)
        lblQuality = Label(frmL, text="Choose Quality:", bg=frmL["background"])
        lblQuality.config(font=fontObj)
        lblQuality.place(anchor=NE, x=frmL.winfo_width()-xStart-32, y=yStart)
        root.update()
        fontObj = tf.Font(size=14)
        drpQuality = OptionMenu(frmL, self.selectedOption, "Cheap      ", *["Expensive"], command=self.qualitySelect)
        drpQuality.config(font=fontObj)
        drpQuality.place(anchor=NE, x=frmL.winfo_width()-xStart, y=yStart+lblQuality.winfo_height())

    def drawWallpaper(self, firstDesign: bool, canvas: Canvas, colour: str) -> None:
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
            mod = canvas.winfo_width() / self.cvsMainDisp.winfo_width()
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
        
    def colourClick(self, event: Event) -> None:
        caller = event.widget
        self.wallpaper.colour = caller["background"]
        self.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)
        self.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour)
        self.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour)
    def designClick(self, event: Event) -> None:
        caller = event.widget
        if caller.winfo_name == self.cvsFirstOp.winfo_name:
            self.wallpaper.firstDesign = True
        else:
            self.wallpaper.firstDesign = False
        self.cvsMainDisp.delete("all")
        self.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)

    def qualitySelect(self, selection: str) -> None:
        self.wallpaper.quality = WallpaperQualities[((selection).upper()).strip()]

Main()