from enum import Enum
from tkinter import *
import tkinter.font as tf
from copy import copy

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
    def __init__(self, firstDesign = True, colour: str = "purple", rolls: int = 1, quality: WallpaperQualities = WallpaperQualities.CHEAP, addition: WallpaperAdditions = WallpaperAdditions.NONE, liningPaper: bool = False, paste: bool = False) -> None:
        """Whilst the constructor does allow custom values, this is purely for testing purposes and instead wallpapers are all initially initiated with default attributes"""
        self.firstDesign = firstDesign
        self.colour = colour
        self.rolls = rolls

        self.quality = quality
        self.addition = addition
        self.liningPaper = liningPaper
        self.paste = paste

    def __str__(self) -> str:
        """Overridden for the display of the wallpaper's data in the view order page's labels"""
        text = ""
        text += f"Quality: {(str(self.quality.name)).capitalize()}"
        if self.addition != WallpaperAdditions.NONE:
            text += f"\nModification: {(str(self.addition.name)).capitalize()}"
        if self.liningPaper:
            text += "\nLining Paper"
        if self.paste:
            text += "\nWallpaper Paste"
        return text
    
    def calcCost(self) -> float:
        pass


class Main:
    """Main class used to initiate the first page and control the mainloop, primary root is also created"""
    def mainLoop() -> None:
        root = Tk()
        root.geometry("960x540")
        root.title("Wallpaper Designer")

        viewWallpaper = ViewWallpaper(root)
        viewWallpaper.drawWindow(root)

        root.resizable(False, False)

        root.mainloop()


    

class ViewWallpaper:
    def __init__(self, root: Tk) -> None:
        """First window, stored in the Main class and contains the second window within itself"""
        self.root = root
        
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
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)

        self.cvsFirstOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsFirstOp.bind("<Button-1>", self.designClick)
        self.cvsFirstOp.place(anchor=NW, x=xStart, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()
        self.cvsSecondOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsSecondOp.bind("<Button-1>", self.designClick)
        self.cvsSecondOp.place(anchor=NW, x=self.cvsFirstOp.winfo_width()+xStart+15, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()

        Draw.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour)


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
        lblModifications.place(anchor=NW, x=xStart, y=self.cvsFirstOp.winfo_y()+self.cvsFirstOp.winfo_height()+96, width=self.cvsMainDisp.winfo_width()+cvsColours[0].winfo_width()+15)
        root.update()
        frmModifications = Frame(frmL, bg="#C2C2C2")
        frmModifications.place(anchor=NW, x=xStart, y=lblModifications.winfo_y()+lblModifications.winfo_height(), width=lblModifications.winfo_width(), height = 128)

        values = {"None" : "NONE",
                  "Foil" : "FOIL",
                  "Glitter" : "GLITTER",
                  "Embossing" : "EMBOSSING"}
        i = 0
        for (text, value) in values.items():
            Radiobutton(frmModifications, variable=self.modificationOp, text=text, value=value, bg=frmModifications["background"], font=tf.Font(size=12), command=self.modificationsSelect).place(anchor=NW, y=2+i*30)
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
        btnAdd.place(anchor=SW, x=lblRolls.winfo_x(), y=frmModifications.winfo_height()+frmModifications.winfo_y(), width=lblRolls.winfo_width(), height=48)


        lblTitle = Label(root, text="Design a new Wallpaper")
        lblTitle.config(font=tf.Font(size=28))
        lblTitle.place(anchor=NW, x=38, y=12)

        btnOrder = Button(root, text="View Order", fg="white", bg="orange", command=self.orderClick)
        btnOrder.config(font=tf.Font(size=12, weight="bold"))
        btnOrder.place(anchor=SW, x=16, y=frmL.winfo_height()-16, width=lblRolls.winfo_width(), height=48)

    def colourClick(self, event: Event) -> None:
        caller = event.widget
        self.wallpaper.colour = caller["background"]
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)
        Draw.drawWallpaper(True, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(False, self.cvsSecondOp, self.wallpaper.colour)
    def designClick(self, event: Event) -> None:
        caller = event.widget
        if caller.winfo_name == self.cvsFirstOp.winfo_name:
            self.wallpaper.firstDesign = True
        else:
            self.wallpaper.firstDesign = False
        self.cvsMainDisp.delete("all")
        Draw.drawWallpaper(self.wallpaper.firstDesign, self.cvsMainDisp, self.wallpaper.colour)

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
        self.wallpaper = Wallpaper()
    def orderClick(self) -> None:
        ViewOrder(self.order, self.root)


  
class ViewOrder:
    def __init__(self, order: list, root: Tk) -> None:
        self.originalRoot = root
        root.withdraw()

        self.order = order
        order.append(Wallpaper(addition=WallpaperAdditions.GLITTER, paste=True, quality=WallpaperQualities.EXPENSIVE, rolls=28))
        order.append(Wallpaper(False, "gold", liningPaper=True, rolls=17))
        order.append(Wallpaper(False, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, quality=WallpaperQualities.EXPENSIVE, rolls=19))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=23))
        order.append(Wallpaper(paste=True, colour="VioletRed2", rolls=8))
        order.append(Wallpaper(False, "gold", liningPaper=True, rolls=1))
        order.append(Wallpaper(False, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, quality=WallpaperQualities.EXPENSIVE, rolls=18))
        order.append(Wallpaper(False, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, quality=WallpaperQualities.EXPENSIVE, rolls=25))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=3))
        order.append(Wallpaper(addition=WallpaperAdditions.GLITTER, paste=True, quality=WallpaperQualities.EXPENSIVE, rolls=2))
        order.append(Wallpaper(addition=WallpaperAdditions.GLITTER, paste=True, quality=WallpaperQualities.EXPENSIVE, rolls=15))
        order.append(Wallpaper(False, "gold", liningPaper=True))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue"))
        order.append(Wallpaper(addition=WallpaperAdditions.GLITTER, paste=True, quality=WallpaperQualities.EXPENSIVE, rolls=5))


        rootOrder = Toplevel()
        rootOrder.title("Secondary Window")
        rootOrder.config(width=960, height=540)
        rootOrder.focus()
        rootOrder.grab_set()
        rootOrder.resizable(False, False)
        rootOrder.protocol('WM_DELETE_WINDOW', self.rootOrderClose)

        self.rootOrder = rootOrder

        self.barMain = Scrollbar()
        self.cvsHidden = Canvas(rootOrder)

        self.frmOrdBack = []
        self.cvsOrd = []
        self.lblOrdDet = []
        self.spnRolls = []
        self.rollsOp = []

        self.drawWindow(rootOrder)

    def drawWindow(self, rootOrder: Tk) -> None:
        rootOrder.update()
        self.cvsHidden.place(x=0, y=0, relheight=1, relwidth=1)

        backFrame = Frame(self.cvsHidden, width=rootOrder.winfo_width(), height=len(self.order)*115+80)
        backFrame.bind('<Configure>', self.on_configure)
        self.cvsHidden.create_window(0, 80, window=backFrame)

        self.barMain = Scrollbar(rootOrder, command=self.cvsHidden.yview)
        self.barMain.place(x=720, y=80, relheight=0.85)
        self.cvsHidden.configure(yscrollcommand=self.barMain.set)
        rootOrder.update()
        
        for i in range(len(self.order)):
            self.frmOrdBack.append(Frame(backFrame, background="#C2C2C2", highlightbackground="black", highlightthickness=2, width=720, height=115))
            self.cvsOrd.append(Canvas(self.frmOrdBack[i], bg="white"))
            self.lblOrdDet.append(Label(self.frmOrdBack[i], bg="#C2C2C2", text=str(self.order[i]), font=tf.Font(size=16), justify=LEFT))
            self.rollsOp.append(StringVar(rootOrder, value=self.order[i].rolls))
            self.spnRolls.append(Spinbox(self.frmOrdBack[i], from_=0, to=50, textvariable=self.rollsOp[i], font=tf.Font(size=14)))
            
        self.orderListDisp(rootOrder)
        Frame(backFrame, background="black").place(x=117, rely=0, width=4, relheight=1)
        Frame(backFrame, background="black").place(x=480, rely=0, width=4, relheight=1)


        rootOrder.update()
        
        frmTop = Frame(rootOrder, bg="darkgray")
        frmTop.place(x=0, y=0, relwidth=rootOrder.winfo_height(), height=82)
        lblTitle = Label(frmTop, text="Order", bg="darkgray")
        lblTitle.config(font=tf.Font(size=36))
        lblTitle.place(anchor=NW, x=16, y=10)
        rootOrder.update()

        cvsBack = Canvas(frmTop, bg="orange", width=32, height=32)
        cvsBack.bind("<Button-1>", self.backClick)
        cvsBack.place(anchor=NE, x=frmTop.winfo_width()-16, y=20)
        rootOrder.update()


        self.cvsHidden.yview_moveto(0)
        Draw.drawArrow(cvsBack)

    def on_configure(self, event: Event) -> None:
        self.cvsHidden.configure(scrollregion=self.cvsHidden.bbox('all'))
       

    def orderListDisp(self, rootOrder: Tk) -> None:
        for i in range(len(self.order)):
            self.frmOrdBack[i].place(x=1, y=80+i*115)
            self.cvsOrd[i].place(x=25, y=25, width=63, height=63)
            self.lblOrdDet[i].place(x=145, y=4)
            self.spnRolls[i].config(command=lambda i=i: self.rollsSelect(i))
            self.spnRolls[i].place(anchor=NW, x=528, y=42, width=128)
        rootOrder.update()
        for i in range(len(self.order)):
            Draw.drawWallpaper(self.order[i].firstDesign, self.cvsOrd[i], self.order[i].colour)

    def rollsSelect(self, i) -> None:
        print(f"{i}")
        if int(self.rollsOp[i].get()) == 0:
            del self.frmOrdBack[i]
            del self.cvsOrd[i]
            del self.lblOrdDet[i]
            del self.spnRolls[i]

            del self.rollsOp[i]
            del self.order[i]
            self.orderListDisp(self.rootOrder)


    def backClick(self, event: Event) -> None:
        self.originalRoot.iconify()
        self.originalRoot.deiconify()
        self.rootOrder.destroy()

    def rootOrderClose(self) -> None:
        self.rootOrder.quit()


class Draw:
    def drawWallpaper(firstDesign: bool, canvas: Canvas, colour: str) -> None:
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
            mod = canvas.winfo_width() / 126
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

    def drawArrow(canvas: Canvas, colour: str = "white") -> None:
        cx = canvas.winfo_width(); cy = canvas.winfo_height()
        canvas.create_polygon(4, cy / 2,
                              cx / 2, 4,
                              cx / 2, 32,
                              4, cy / 2, fill=colour)
        canvas.create_rectangle(cx / 2, cy * 0.3, cx - 8, cy * 0.6, fill=colour, outline=colour)

Main.mainLoop()