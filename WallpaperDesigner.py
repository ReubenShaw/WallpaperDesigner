from enum import Enum
from tkinter import *
import tkinter.font as tf
import math
import re

class WallpaperQualities(Enum): #REDO, PRICES WRONG
    CHEAP = 0.003
    EXPENSIVE = 0.006

class WallpaperAdditions(Enum):
    NONE = 0
    EMBOSSING = 0.06
    FOIL = 0.12
    GLITTER = 0.18

class Windows(Enum):
    VIEW_WALLPAPER = 0
    VIEW_ORDER = 1

class Wallpaper:
    def __init__(self, quality: WallpaperQualities = WallpaperQualities.CHEAP, colour: str = "purple", rolls: int = 1, addition: WallpaperAdditions = WallpaperAdditions.NONE, liningPaper: bool = False, paste: bool = False) -> None:
        """Whilst the constructor does allow custom values, this is purely for testing purposes and instead wallpapers are all initially initiated with default attributes"""
        self.quality = quality
        self.colour = colour
        self.rolls = rolls

        self.addition = addition
        self.liningPaper = liningPaper
        self.paste = paste

    def __str__(self) -> str:
        """Overridden for the display of the wallpaper's data in the view order page's labels"""
        text = ""
        text += f"Quality: {self.quality.name.capitalize()}"
        if self.addition != WallpaperAdditions.NONE:
            text += f"\nModification: {self.addition.name.capitalize()}"
        if self.liningPaper:
            text += "\nLining Paper"
        if self.paste:
            text += "\nWallpaper Paste"
        return text
    
    def calcCost(self) -> float:
        width = 0.52
        height = 10.05

        totalHeight = height * self.rolls
        totalArea = width * height * self.rolls

        cost = 0
        if self.rolls > 0:
            cost += self.quality.value * totalArea * 10000
            cost += self.addition.value * totalHeight

            if self.liningPaper and self.paste:
                cost += math.ceil(totalArea / 20) * 7.63
                cost += math.ceil(totalArea / 53) * 13.99 * 2
            elif self.liningPaper:
                cost += math.ceil(totalArea / 20) * 7.63
            elif self.paste:
                cost += math.ceil(totalArea / 53) * 13.99

        return round(cost, 2)


class Main:
    """Main class used to initiate the first page and control the mainloop"""
    def mainLoop() -> None:
        order = []
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=28))
        order.append(Wallpaper(colour="gold", liningPaper=True, rolls=17))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=19))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=23))
        order.append(Wallpaper(paste=True, colour="VioletRed2", rolls=8))
        order.append(Wallpaper(colour="gold", liningPaper=True, rolls=1))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=18))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=25))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=3))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=2))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=15))
        order.append(Wallpaper(colour="gold", liningPaper=True))
        order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue"))
        order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=5))
        mainWin = ViewWallpaper(order=order)
        
        mainWin.root.mainloop()


class ViewWallpaper():
    def __init__(self, root: Tk = Tk(), wallpaper: Wallpaper = Wallpaper(), order: list = [], modIndex: int = -1) -> None:
        """First window, stored in the Main class and contains the second window within itself"""
        self.originalRoot = root
        root.withdraw()

        self.root = Toplevel()
        self.root.title("Wallpaper Designer")
        self.root.config(width=960, height=540)
        self.root.focus()
        self.root.grab_set()
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.rootClose)

        self.availableColours = ["purple", "DarkSlateGray4", "deep sky blue", "light sea green", "VioletRed2", "gold"]
        self.wallpaper = wallpaper
        self.order = order
        self.modIndex = modIndex

        self.liningOp = IntVar(value=int(wallpaper.liningPaper))
        self.pasteOp = IntVar(value=int(wallpaper.paste))
        self.modificationOp = StringVar(self.root, str(wallpaper.addition.name))
        self.metresVar = StringVar(root, format(round(self.wallpaper.rolls * 10.05, 2), ",.2f"))

        self.cvsMainDisp = Canvas()
        self.cvsFirstOp = Canvas()
        self.cvsSecondOp = Canvas()

        self.txtMetres = Entry()

        self.lblQuality = Label()
        self.lblCost = Label()
        self.lblTotalCost = Label()
        self.lblRolls = Label()

        self.drawWindow(self.root)

    def drawWindow(self, root: Tk) -> None:
        frmL = Frame(root, bg="lightgray")
        frmL.place(anchor=W, relx=0.5, rely=0.5, relwidth=0.5, relheight=1)

        xStart = 32; yStart = 32
        self.cvsMainDisp = Canvas(frmL, width=126, height=126, bg="white")
        self.cvsMainDisp.place(anchor=NW, x=xStart, y=yStart)
        root.update()
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)

        self.cvsFirstOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsFirstOp.bind("<Button-1>", self.designClick)
        self.cvsFirstOp.place(anchor=NW, x=xStart, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()
        self.cvsSecondOp = Canvas(frmL, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsSecondOp.bind("<Button-1>", self.designClick)
        self.cvsSecondOp.place(anchor=NW, x=self.cvsFirstOp.winfo_width()+xStart+15, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()

        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)


        cvsColours = []
        for i in range(len(self.availableColours)):
            cvsColours.append(Frame(frmL, width=self.cvsMainDisp.winfo_width()/7, height=self.cvsMainDisp.winfo_height()/7, bg=self.availableColours[i]))
            cvsColours[i].bind("<Button-1>", self.colourClick)
            cvsColours[i].place(anchor=NW, x=self.cvsMainDisp.winfo_width()+xStart+15, y=yStart+(i*2*self.cvsMainDisp.winfo_height()/7))

        xStart = 64
        lblQualityDescrip = Label(frmL, text="Quality:", bg=frmL["background"], font=tf.Font(size=12))
        lblQualityDescrip.place(anchor=NE, x=frmL.winfo_width()-xStart-64, y=yStart)
        root.update()
        self.lblQuality = Label(frmL, text=self.wallpaper.quality.name.capitalize(), font=tf.Font(size=14), justify=LEFT, bg="#C2C2C2")
        self.lblQuality.place(anchor=NW, x=lblQualityDescrip.winfo_x(), y=yStart+lblQualityDescrip.winfo_height(), width=lblQualityDescrip.winfo_width()+80)
        root.update()

        lblAdditions = Label(frmL, text="Additions", bg="darkgray")
        lblAdditions.config(font=tf.Font(size=12))
        lblAdditions.place(anchor=NW, x=self.lblQuality.winfo_x(), y=yStart+self.lblQuality.winfo_y()+48, width=self.lblQuality.winfo_width()+16)
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
        lblMetres = Label(frmL, text="Metres of Wallpaper", bg=frmL["background"], font=tf.Font(size=12))
        lblMetres.place(anchor=NW, x=lblAdditions.winfo_x(), y=lblModifications.winfo_y(), width=frmAdditions.winfo_width())
        root.update()
        
        callback = root.register(self.metreValidate)
        self.txtMetres = Entry(frmL, font=tf.Font(size=10), validate="key", validatecommand=(callback, '%S'), textvariable=self.metresVar)
        self.txtMetres.bind("<KeyRelease>", self.metreKeyPress)
        self.txtMetres.place(anchor=NW, x=lblMetres.winfo_x(), y=lblMetres.winfo_y()+lblMetres.winfo_height(), width=lblMetres.winfo_width(), height=20)

        root.update()
        self.lblRolls = Label(frmL, text=f"Rolls: {self.wallpaper.rolls}", bg=frmL["background"], font=tf.Font(size=12))
        self.lblRolls.place(x=self.txtMetres.winfo_x(), y=self.txtMetres.winfo_y()+self.txtMetres.winfo_height())

        btnAdd = Button(frmL, fg="white", bg="orange", command=self.addClick)
        btnAdd.config(font=tf.Font(size=12, weight="bold"))
        if self.modIndex > -1:
            btnAdd.config(text="Modiy Wallpaper")
        else:
            btnAdd.config(text="Add to Basket")
        btnAdd.place(anchor=SW, x=lblMetres.winfo_x(), y=frmModifications.winfo_height()+frmModifications.winfo_y(), width=lblMetres.winfo_width(), height=48)
        root.update()
        self.lblCost = Label(frmL, bg=frmL["background"], font=tf.Font(size=12))
        self.lblCost.place(x=btnAdd.winfo_x(), y=btnAdd.winfo_y()-24)
        self.calcCost()
        


        lblTitle = Label(root, text="Design a new Wallpaper")
        lblTitle.config(font=tf.Font(size=28))
        lblTitle.place(anchor=NW, x=38, y=12)

        btnOrder = Button(root, fg="white", bg="orange", command=self.orderClick)
        btnOrder.config(font=tf.Font(size=12, weight="bold"))
        if self.modIndex > -1:
            btnOrder.config(text="Return to Order")
        else:
            btnOrder.config(text="View Order")
        btnOrder.place(anchor=SW, x=16, y=frmL.winfo_height()-16, width=lblMetres.winfo_width(), height=48)
        root.update()

        self.lblTotalCost = Label(root, bg=root["background"], font=tf.Font(size=16))
        self.lblTotalCost.place(anchor=SE, x=frmL.winfo_x()-48, y=btnOrder.winfo_y()+btnOrder.winfo_height())
        self.calcOrderCost()

    def colourClick(self, event: Event) -> None:
        caller = event.widget
        self.wallpaper.colour = caller["background"]
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)
    def designClick(self, event: Event) -> None:
        caller = event.widget
        if caller.winfo_name == self.cvsFirstOp.winfo_name:
            self.wallpaper.quality = WallpaperQualities.CHEAP
        else:
            self.wallpaper.quality = WallpaperQualities.EXPENSIVE
        self.lblQuality.config(text=self.wallpaper.quality.name.capitalize())
        self.cvsMainDisp.delete("all")
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)
        self.calcCost()

    def additionsSelect(self) -> None:
        if self.liningOp.get() == 0:
            self.wallpaper.liningPaper = False
        else: self.wallpaper.liningPaper = True
        if self.pasteOp.get() == 0:
            self.wallpaper.paste = False
        else: self.wallpaper.paste = True
        self.calcCost()
        
    def modificationsSelect(self) -> None:
        self.wallpaper.addition = WallpaperAdditions[self.modificationOp.get()]
        self.calcCost()

    def metreValidate(self, input: str) -> bool:
        if input.isdigit() or input == "" or input == ".":
            return True
        return False
    def metreKeyPress(self, event: Event) -> None:
        if isNumber.check(self.txtMetres.get()):
            self.wallpaper.rolls = math.ceil(float(self.txtMetres.get()) / 10.05)
        else:
            self.wallpaper.rolls = 0
        self.calcCost()
        self.lblRolls.config(text=f"Rolls: {self.wallpaper.rolls}")

    def addClick(self) -> None:
        if self.modIndex > -1:
            self.order[self.modIndex] = self.wallpaper
            ViewOrder(self.order, self.root)
        else:
            self.order.append(self.wallpaper)
            self.calcOrderCost()
            self.wallpaper = Wallpaper()
            self.reset()
    def orderClick(self) -> None:
        self.reset()
        ViewOrder(self.order, self.root)

    def calcCost(self) -> None:
        stringDisp = format(self.wallpaper.calcCost(), ",.2f")
        self.lblCost.config(text=f"Cost: £{stringDisp}")

    def calcOrderCost(self) -> None:
        orderCost = 0
        for i in range (len(self.order)):
            orderCost += self.order[i].calcCost()
        stringDisp = format(orderCost, ",.2f")
        self.lblTotalCost.config(text=f"Order Cost: £{stringDisp}")


    def reset(self) -> None:
        self.wallpaper = Wallpaper()
        self.liningOp.set(int(self.wallpaper.liningPaper))
        self.pasteOp.set(int(self.wallpaper.paste))
        self.modificationOp.set(self.wallpaper.addition.name)
        self.metresVar.set("10.05")
        
        self.lblQuality.config(text=self.wallpaper.quality.name.capitalize())
        self.cvsMainDisp.delete("all")
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)
        self.additionsSelect()
        self.modificationsSelect()

    def rootClose(self) -> None:
        self.originalRoot.destroy()
        self.root.quit()


  
class ViewOrder:
    def __init__(self, order: list, root: Tk) -> None:
        self.originalRoot = root
        root.withdraw()

        self.order = order
        


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
        self.backFrame = Frame()

        self.frmOrdBack = []
        self.cvsOrd = []
        self.lblOrdDet = []
        self.btnEdit = []
        self.spnRolls = []
        self.rollsOp = []

        self.drawWindow(rootOrder)

    def drawWindow(self, rootOrder: Tk) -> None:
        rootOrder.update()
        self.cvsHidden.place(x=0, y=0, relheight=1, relwidth=1)

        self.backFrame = Frame(self.cvsHidden, width=rootOrder.winfo_width(), height=len(self.order)*115+80)
        self.backFrame.bind('<Configure>', self.on_configure)
        self.cvsHidden.create_window(0, 80, window=self.backFrame)

        self.barMain = Scrollbar(rootOrder, command=self.cvsHidden.yview)
        self.barMain.place(x=720, y=80, relheight=0.85)
        self.cvsHidden.configure(yscrollcommand=self.barMain.set)
        rootOrder.update()
        
        for i in range(len(self.order)):
            self.frmOrdBack.append(Frame(self.backFrame, background="#C2C2C2", highlightbackground="black", highlightthickness=2, width=720, height=115))
            self.cvsOrd.append(Canvas(self.frmOrdBack[i], bg="white"))
            self.lblOrdDet.append(Label(self.frmOrdBack[i], bg="#C2C2C2", text=str(self.order[i]), font=tf.Font(size=16), justify=LEFT))
            self.btnEdit.append(Button(self.frmOrdBack[i], bg="#C2C2C2", text="Edit"))
            self.rollsOp.append(StringVar(rootOrder, value=self.order[i].rolls))
            self.spnRolls.append(Spinbox(self.frmOrdBack[i], from_=0, to=50, textvariable=self.rollsOp[i], font=tf.Font(size=14)))

        self.orderListDisp(rootOrder)
        Frame(self.backFrame, background="black").place(x=117, rely=0, width=4, relheight=1)
        Frame(self.backFrame, background="black").place(x=480, rely=0, width=4, relheight=1)


        rootOrder.update()
        
        frmTop = Frame(rootOrder, bg="darkgray")
        frmTop.place(x=0, y=0, relwidth=rootOrder.winfo_height(), height=82)
        lblTitle = Label(frmTop, text="Order", bg="darkgray")
        lblTitle.config(font=tf.Font(size=36))
        lblTitle.place(anchor=NW, x=16, y=10)
        rootOrder.update()

        cvsBack = Canvas(frmTop, bg="orange", width=32, height=32)
        cvsBack.bind("<Button-1>", self.backClick)
        cvsBack.place(anchor=NE, x=938, y=20)
        rootOrder.update()


        self.cvsHidden.yview_moveto(0)
        Draw.drawArrow(cvsBack)

    def on_configure(self, event: Event) -> None:
        self.cvsHidden.configure(scrollregion=self.cvsHidden.bbox('all'))
       

    def orderListDisp(self, rootOrder: Tk) -> None:
        for i in range(len(self.order)):
            self.frmOrdBack[i].place(x=1, y=80+i*115)
            self.cvsOrd[i].place(x=24, y=24, width=65, height=65)
            self.lblOrdDet[i].place(x=145, y=4)
            self.btnEdit[i].config(command=lambda i=i: self.editClick(i))
            self.btnEdit[i].place(anchor=NE, x=464, y=67, width=32, height=32)
            self.spnRolls[i].config(command=lambda i=i: self.rollsSelect(i))
            self.spnRolls[i].place(anchor=NW, x=528, y=42, width=128)
            self.backFrame.config(height=len(self.order)*115+80)
        rootOrder.update()
        for i in range(len(self.order)):
            Draw.drawWallpaper(self.order[i].quality, self.cvsOrd[i], self.order[i].colour)

    def rollsSelect(self, i) -> None:
        if int(self.rollsOp[i].get()) == 0:
            self.frmOrdBack[i].destroy()
            del self.frmOrdBack[i]
            del self.cvsOrd[i]
            del self.lblOrdDet[i]
            del self.btnEdit[i]
            del self.spnRolls[i]

            del self.rollsOp[i]
            del self.order[i]
            self.orderListDisp(self.rootOrder)
        else:
            self.order[i].rolls = self.rollsOp[i].get()

    def editClick(self, i) -> None:
        self.rootOrder.destroy()
        ViewWallpaper(Tk(), self.order[i], self.order, i)


    def backClick(self, event: Event) -> None:
        self.originalRoot.iconify()
        self.originalRoot.deiconify()
        self.rootOrder.destroy()

    def rootOrderClose(self) -> None:
        self.rootOrder.quit()


class Draw:
    def drawWallpaper(quality: WallpaperQualities, canvas: Canvas, colour: str) -> None:
        cx = canvas.winfo_width(); cy = canvas.winfo_height()
        if quality == WallpaperQualities.EXPENSIVE:
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
            mod = canvas.winfo_width() / 129
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
        # canvas.create_polygon(4, cy / 2,
        #                       cx / 2, 4,
        #                       cx / 2, 32,
        #                       4, cy / 2, fill=colour)
        # canvas.create_rectangle(cx / 2, cy * 0.3, cx - 8, cy * 0.6, fill=colour, outline=colour)
        canvas.create_line(6, cy/2, cx-6, cy/2, fill=colour, width=3)
        canvas.create_line(5, cy/2, cx/2, cy/4, fill=colour, width=3)
        canvas.create_line(5, cy/2, cx/2, cy-cy/4, fill=colour, width=3)

class isNumber():
    def check(input: str) -> bool:
        #Finally my knowledge in Regex came to use!!
        if re.match("^\d+(\.\d+)?$", input):
            return True
        return False

Main.mainLoop()