"""
IMPORTANT INFORMATION FOR REVIEWER:

Lines 138-153 have commented out test data, uncomment to get immediate data to test with
"""

#The program:
from enum import Enum
from tkinter import *
from tkinter import messagebox
import tkinter.font as tf #For both tkinter.font and messagebox I was unable to get it to work unless I specifically imported them, a little strange
import math
import re

WIDTH = 0.52
HEIGHT = 10.05 #Constants for wallpaper dimensions

class WallpaperQualities(Enum):
    """Used for the quality which is linked to design, the values refer to the cost per cm^2 of wallpaper\n
    Cheap = £0.003, Expensive = £0.006"""
    
    CHEAP = 0.003
    EXPENSIVE = 0.006

class WallpaperAdditions(Enum):
    """Used for the modifications part of the system, only one of these options can be chosen and their respective values are the price per metre\n
    Embossing = £0.06, Foil = £0.12, Glitter = £0.18"""
    
    NONE = 0
    EMBOSSING = 0.06
    FOIL = 0.12
    GLITTER = 0.18

class Wallpaper:
    def __init__(self, quality: WallpaperQualities = WallpaperQualities.CHEAP, colour: str = "purple", rolls: int = 1, addition: WallpaperAdditions = WallpaperAdditions.NONE, liningPaper: bool = False, paste: bool = False) -> None:
        """Whilst the constructor does allow custom values, this is purely for testing purposes and instead wallpapers are all initially initiated with default attributes\n
        All parameteres default to the base properties of a wallpaper:\n
        Quality: Cheap, Colour: Purple, Rolls: 1, Additions: None,, Lining Paper: False, Paste: False"""
        
        self._quality = quality
        self._colour = colour
        self._rolls = rolls

        self._addition = addition
        self._liningPaper = liningPaper
        self._paste = paste
    
    #Get setters
    @property
    def quality(self) -> WallpaperQualities:
        return self._quality
    @quality.setter
    def quality(self, value) -> None:
        self._quality = value
        
    @property
    def colour(self) -> str:
        return self._colour
    @colour.setter
    def colour(self, value) -> None:
        self._colour = value
        
    @property
    def rolls(self) -> int:
        return self._rolls
    @rolls.setter
    def rolls(self, value) -> None:
        self._rolls = value
        
    @property
    def addition(self) -> WallpaperAdditions:
        return self._addition
    @addition.setter
    def addition(self, value) -> None:
        self._addition = value
        
    @property
    def liningPaper(self) -> bool:
        return self._liningPaper
    @liningPaper.setter
    def liningPaper(self, value) -> None:
        self._liningPaper = value
        
    @property
    def paste(self) -> bool:
        return self._paste
    @paste.setter
    def paste(self, value) -> None:
        self._paste = value

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
    
    def calcFinalCost(self) -> float:
        """Used for calculating the cost of the wallpaper object, works persuming that the width is 0.52m and the height is 10.05m"""
        
        totalHeight = HEIGHT * self.rolls #unit: metres
        totalArea = WIDTH * HEIGHT * self.rolls #unit: metres^2

        cost = 0
        if self.rolls > 0: #If used when displaying price to ensure that if the metres entry box is blank or holding an incomplete decimal number that the displayed output is not incorrect
            cost += self.quality.value * totalArea * 10000 #*10000 is to convert the values which are in cm^2 to m^2, which is the units totalArea uses
            cost += self.addition.value * math.ceil(totalHeight / 1)

            #3 part if statement as if there's lining paper and paste the paste has to be doubled, as one n amount is for the wallpaper and an equal n amount for the lining
            if self.liningPaper and self.paste: 
                cost += math.ceil(totalArea / 20) * 7.63 #math.ceil always used to ensure partial values are rounded up, as a these are provided in set amounts
                cost += math.ceil(totalArea / 53) * 13.99 * 2 #TODO: look into the length of a roll
            elif self.liningPaper:
                cost += math.ceil(totalArea / 20) * 7.63 #20m is how much a single roll of lining paper stretches, this costs £7.63
            elif self.paste:
                cost += math.ceil(totalArea / 53) * 13.99 #53m is how much a single tub or paste covers, this costs £13.99

        return round(cost, 2) #Whilst a formatting display is used for presenting the value as a string, rounding here as well ensures that the price is more accurate
    


class Main:
    """Main class used to initiate the first page and control the mainloop"""
    
    def mainLoop() -> None:
        """Call to initialise loop"""
        
        order : Wallpaper = [] #Used just for testing purposes, so that an order can be created in here and passed to the main window
        
        #Test data:
        
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=28))
        # order.append(Wallpaper(colour="gold", liningPaper=True, rolls=17))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=19))
        # order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=23))
        # order.append(Wallpaper(paste=True, colour="VioletRed2", rolls=8))
        # order.append(Wallpaper(colour="gold", liningPaper=True, rolls=1))
        # order.append(Wallpaper(colour="gold", rolls=7))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=18))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.EMBOSSING, paste=True, liningPaper=True, rolls=25))
        # order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue", rolls=3))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=2))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=15))
        # order.append(Wallpaper(colour="gold", liningPaper=True))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, colour="deep sky blue", rolls=1))
        # order.append(Wallpaper(addition=WallpaperAdditions.FOIL, colour="deep sky blue"))
        # order.append(Wallpaper(WallpaperQualities.EXPENSIVE, addition=WallpaperAdditions.GLITTER, paste=True, rolls=5))
        
        mainWin = ViewWallpaper(order=order)
        
        mainWin.root.mainloop()


class ViewWallpaper():
    """Class for the first page, that enables the creation of new wallpapers, dispalyed on startup and can be reaccessed as a modification page from the ViewOrder() window"""
    
    def __init__(self, root: Tk = Tk(), wallpaper: Wallpaper = Wallpaper(), order: list = [], modIndex: int = -1) -> None:
        """First window, stored in the Main class and contains the second window within itself\n
        All parameters have default values where the initialise themselves, aside from modIndex which = -1
        """
        
        #Due to this constructor needing to be invoked by the other window and not just in Main.mainLoop() hiding the origianl root means that the original window doesn't also show
        #Destroy cannot be used here, as because of the reason mentioned above this window must be created as a TopLevel(), which means when first booting up another smaller window is created that acts as the "true" toplevel window for this program, but is intrisically linked to this one
        #-which means that if either that window or this one is destroyed the program is closed, so instead withdraw also works to just hide it
        self.originalRoot = root 
        root.withdraw()

        self.initRoot()

        self.availableColours = ["purple", "DarkSlateGray4", "deep sky blue", "light sea green", "VioletRed2", "gold"]
        self.wallpaper = wallpaper
        self.order = order
        self.modIndex = modIndex #modIndex is used when the page is constructed from the order page and it instructs the index in the order which is being modified

        #Options used by various widgets in the page
        self.liningOp = IntVar(value=int(wallpaper.liningPaper))
        self.pasteOp = IntVar(value=int(wallpaper.paste))
        self.modificationOp = StringVar(self.root, str(wallpaper.addition.name))

        #Canvases for displaying the designs, needs to be accessible everywhere as multiple subroutines interact with the design
        self.cvsMainDisp = Canvas()
        self.cvsFirstOp = Canvas()
        self.cvsSecondOp = Canvas()

        #Used for entering the amount of wallpaper needed, data is taken from it in multiple subroutines
        self.txtMetres = Entry()

        #Labels used for displaying cost, wallpaper type and the conversion from entered metres to rolls, all have their display value modified after creation so they need to be accessible
        self.lblQuality = Label()
        self.lblCost = Label()
        self.lblTotalCost = Label()
        self.lblRolls = Label()

        self.drawWindow(self.root)
        
    def initRoot(self):
        self.root = Toplevel() #TopLevel() as this can be invoked from the other window and as such needs to be able to fully recreate itself as a main window
        self.root.title("Wallpaper Designer")
        self.root.geometry("960x540+50+50")
        self.root.focus()
        self.root.grab_set()
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.rootClose) #Needed as depending on which iteration of the window this is it may not be the main window, meaning if it's closed the program will not exit and additional logic is needed
        self.root.bind("<FocusIn>", self.rootFocus)

    def drawWindow(self, root: Tk) -> None:
        """Window drawing for ViewWallpaper page"""
        
        frmMain = Frame(root, bg="lightgray") #frmMain is the right-hand half of the page where the majority of widgets are drawn to
        frmMain.place(anchor=W, relx=0.5, rely=0.5, relwidth=0.5, relheight=1)

        xStart = 32; yStart = 32 #These variables are used for changing the padding of where widgets should first been drawn from on frmMain
        self.cvsMainDisp = Canvas(frmMain, width=126, height=126, bg="white")
        self.cvsMainDisp.place(anchor=NW, x=xStart, y=yStart)
        root.update() #root.update is called a lot, as winfo_*() calls won't provide accurate values otherwise
        
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour) #Draws the currently selected wallpaper, ensuring that if this window was accessed from the order winow the wallpaper design and colour is accurate

        self.cvsFirstOp = Canvas(frmMain, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsFirstOp.bind("<Button-1>", self.designClick)
        self.cvsFirstOp.place(anchor=NW, x=xStart, y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()
        
        self.cvsSecondOp = Canvas(frmMain, width=56, height=56, bg=self.cvsMainDisp["background"])
        self.cvsSecondOp.bind("<Button-1>", self.designClick)
        self.cvsSecondOp.place(anchor=NE, x=self.cvsMainDisp.winfo_x()+self.cvsMainDisp.winfo_width(), y=self.cvsMainDisp.winfo_height()+yStart+15)
        root.update()

        #Once again, these are used to draw the designs that can be selected but ensure to use the current wallpaper's colour in case the window was accessed from the order window and the user is modifying a wallpaper
        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)


        frmColours : Frame = []
        for i in range(len(self.availableColours)):
            frmColours.append(Frame(frmMain, width=self.cvsMainDisp.winfo_width()/7, height=self.cvsMainDisp.winfo_height()/7, bg=self.availableColours[i]))
            frmColours[i].bind("<Button-1>", self.colourClick) #All different colours are routed through a single event function, to decrease repetitive code
            frmColours[i].place(anchor=NW, x=self.cvsMainDisp.winfo_width()+xStart+15, y=yStart+(i*2*self.cvsMainDisp.winfo_height()/7))

        xStart = 128 #Padding updated as the other side of the frame is being drawn to now
        lblQualityDescrip = Label(frmMain, text="Quality:", bg=frmMain["background"], font=tf.Font(size=12))
        lblQualityDescrip.place(anchor=NE, x=frmMain.winfo_width()-xStart, y=yStart)
        root.update()
        
        self.lblQuality = Label(frmMain, text=self.wallpaper.quality.name.capitalize(), font=tf.Font(size=14), justify=LEFT, bg="#C2C2C2")
        self.lblQuality.place(anchor=NW, x=lblQualityDescrip.winfo_x(), y=yStart+lblQualityDescrip.winfo_height(), width=lblQualityDescrip.winfo_width()+80)
        root.update()

        lblAdditions = Label(frmMain, text="Additions", bg="darkgray", font=tf.Font(size=12))
        lblAdditions.place(anchor=NW, x=self.lblQuality.winfo_x(), y=yStart+self.lblQuality.winfo_y()+48, width=self.lblQuality.winfo_width()+16)
        root.update()
        
        frmAdditions = Frame(frmMain, bg="#C2C2C2")
        frmAdditions.place(anchor=NW, x=lblAdditions.winfo_x(), y=lblAdditions.winfo_y()+lblAdditions.winfo_height(), width=lblAdditions.winfo_width(), 
                           height=frmColours[5].winfo_y()+frmColours[5].winfo_height()-lblAdditions.winfo_y()-lblAdditions.winfo_height())
        #Drawing around the location of frmColours[5] is because that's the final frame for displaying colours
        root.update()
        
        #Both checkbuttons take their default state from their relevant self.*Op variable, which is responsible for ensuring they have the correct state when entering this window form the order screen
        chkLining = Checkbutton(frmAdditions, text="Lining Paper", variable=self.liningOp, bg=frmAdditions["background"], command=self.additionsSelect)
        chkLining.config(font=tf.Font(size=12)) #For some reason checkbuttons don't allow initilisation with custom fonts, but can be configured to have one
        chkLining.place(anchor=NW, y=2)
        root.update()
        
        chkPaste = Checkbutton(frmAdditions, text="Wallpaper Paste", variable=self.pasteOp, bg=frmAdditions["background"], command=self.additionsSelect)
        chkPaste.config(font=tf.Font(size=12))
        chkPaste.place(anchor=NW, y=chkLining.winfo_height()+8)

        xStart = 32
        lblModifications = Label(frmMain, text="Modifications", bg="darkgray")
        lblModifications.config(font=tf.Font(size=12))
        lblModifications.place(anchor=NW, x=xStart, y=self.cvsFirstOp.winfo_y()+self.cvsFirstOp.winfo_height()+128, width=self.cvsMainDisp.winfo_width()+frmColours[0].winfo_width()+15)
        root.update()
        
        frmModifications = Frame(frmMain, bg="#C2C2C2")
        frmModifications.place(anchor=NW, x=xStart, y=lblModifications.winfo_y()+lblModifications.winfo_height(), width=lblModifications.winfo_width(), height = 128)

        #The first part of the values is the name that gets displayed, the second is the reference to the enum value
        values = {"None" : "NONE",
                  "Foil" : "FOIL",
                  "Glitter" : "GLITTER",
                  "Embossing" : "EMBOSSING"}
        i = 0
        #This could be done more neatly but I had a lot of issues with getting tkinter to accept converted enum values across the entire program, so this worked best
        for (text, value) in values.items():
            Radiobutton(frmModifications, variable=self.modificationOp, text=text, value=value, bg=frmModifications["background"], font=tf.Font(size=12), command=self.modificationsSelect).place(anchor=NW, y=2+i*30)
            #Radiobuttons were chosen as unlike checkbuttons only one from the group can be on at a time
            i+=1

        root.update()
        lblMetres = Label(frmMain, text="Metres of Wallpaper", bg=frmMain["background"], font=tf.Font(size=12))
        lblMetres.place(anchor=NW, x=lblAdditions.winfo_x(), y=lblModifications.winfo_y(), width=frmAdditions.winfo_width())
        root.update()
        
        callback = root.register(self.metreValidate) #This callback is needed so that I can restrict entry into the textbox to just allowed values
        self.txtMetres = Entry(frmMain, font=tf.Font(size=12), validate="key", validatecommand=(callback, '%S'))
        self.txtMetres.bind("<KeyRelease>", self.metreKeyPress)
        self.txtMetres.place(anchor=NW, x=lblMetres.winfo_x(), y=lblMetres.winfo_y()+lblMetres.winfo_height(), width=lblMetres.winfo_width(), height=20)
        self.txtMetres.insert(0, round(self.wallpaper.rolls * 10.05, 2)) #Add the metres of wallpaper needed
        root.update()
        
        self.lblRolls = Label(frmMain, text=f"Rolls: {self.wallpaper.rolls}", bg=frmMain["background"], font=tf.Font(size=10))
        self.lblRolls.place(x=self.txtMetres.winfo_x(), y=self.txtMetres.winfo_y()+self.txtMetres.winfo_height())

        btnAdd = Button(frmMain, fg="white", bg="orange", command=self.addClick, font=tf.Font(size=12, weight="bold"))
        if self.modIndex > -1: #Since the user is either going to be adding a new wallpaper to basket or modifying an existing one, the text on the button needs to be different, by using modIndex - which is -1 unless this window is accessed through the order screen - this can be checked
            btnAdd.config(text="Modiy Wallpaper")
        else:
            btnAdd.config(text="Add to Basket")
        btnAdd.place(anchor=SW, x=lblMetres.winfo_x(), y=frmModifications.winfo_height()+frmModifications.winfo_y(), width=lblMetres.winfo_width(), height=48)
        root.update()
        
        self.lblCost = Label(frmMain, bg=frmMain["background"], font=tf.Font(size=12))
        self.lblCost.place(x=btnAdd.winfo_x(), y=btnAdd.winfo_y()-24)
        self.calcCost()
        
        lblTitle = Label(root, text="Design a new Wallpaper")
        lblTitle.config(font=tf.Font(size=28))
        lblTitle.place(anchor=NW, x=38, y=12)
        root.update()
        
        lblPrices = Label(root, text="Cheap Wallpaper = £156.78 per roll\n" +
                         "Expensive Wallpaper = £313.56 per roll\n\n" +
                         "Foil = £1.32 per roll\n" + 
                         "Glitter = £1.98 per roll\n" +
                         "Embossing = £0.66 per roll\n\n" +
                         "Lining Paper = £7.63 per 20 metres\n" +
                         "Wallpaper Paste = £13.99 per 53m^2\n\n" + 
                         "Please note, double the amount of wallpaper paste\nis needed if lining paper is also purchased", justify="left")
        lblPrices.config(font=tf.Font(size=14))
        lblPrices.place(anchor=NW, x=lblTitle.winfo_x() - 16, y=lblTitle.winfo_y() + lblTitle.winfo_height() + 48)

        btnOrder = Button(root, fg="white", bg="orange", command=self.orderClick, font=tf.Font(size=12, weight="bold"))
        if self.modIndex > -1: #Same as the previous button, just a minor rewording to try and promote more concistency depending on how the user accesses the window
            btnOrder.config(text="Return to Order")
        else:
            btnOrder.config(text="View Order")
        btnOrder.place(anchor=SW, x=16, y=frmMain.winfo_height()-16, width=lblMetres.winfo_width(), height=48)
        root.update()

        self.lblTotalCost = Label(root, bg=root["background"], font=tf.Font(size=16))
        self.lblTotalCost.place(anchor=SE, x=frmMain.winfo_x()-48, y=btnOrder.winfo_y()+btnOrder.winfo_height())
        self.lblTotalCost.config(text=f"Order Cost: £{Cost.calcOrderCost(self.order)}")

    def colourClick(self, event: Event) -> None:
        """Method used for updating the self.wallpaper's colour select, also manages the calls to change the colours of the display\n
        Acts an event handler for all six colour frames"""
        
        caller = event.widget #Since this is envoked by a bind event, not a command, an event paramater is needed to fetch the envoked widget 
        self.wallpaper.colour = caller["background"] #Since the frame clicked has the colour of the desired wallpaper, just fetching the background colour is enough
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)
    
    def designClick(self, event: Event) -> None:
        """Method used to handle events from both the design canvas selections"""
        
        caller = event.widget
        if caller.winfo_name() == self.cvsFirstOp.winfo_name(): #Checks the canvas name against the first design's canvas name, to determine the selected quality
            self.wallpaper.quality = WallpaperQualities.CHEAP
        else:
            self.wallpaper.quality = WallpaperQualities.EXPENSIVE

        self.lblQuality.config(text=self.wallpaper.quality.name.capitalize())
        self.cvsMainDisp.delete("all") #This clears the canvas so drawing to it works properly
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour)
        self.calcCost()

    def additionsSelect(self) -> None:
        """Handles both checkbutton's tick and untick events"""
        
        self.wallpaper.liningPaper = bool(self.liningOp.get())
        self.wallpaper.paste = bool(self.pasteOp.get())
        
        self.calcCost()
        
    def modificationsSelect(self) -> None:
        """Handles the radiobutton check events"""
        
        self.wallpaper.addition = WallpaperAdditions[self.modificationOp.get()] #Converts the already captalised modification name to the relevant enum
        self.calcCost()

    def metreValidate(self, input: str) -> bool:
        """Function that handles the callback event for entering metres, will cancel the input if it fails\n
        Checks if the input is either a digit, \".\" or an empty space (needed for backspace)"""
        
        if IsNumber.check(input) or input == "" or input == ".":
            return True
        print(f"Failed as {input} is not allowed")
        return False
    
    def metreKeyPress(self, event: Event) -> None:
        """Subroutine that runs everytime data is entered into the entering metres box to check if it's a valid number and if so to update the rolls display\n
        Despite metreValidate preventing bad input, the check here is still needed as it could be either blank or a half number like: 43. which would cause an error when converting to int"""
        
        if IsNumber.check(self.txtMetres.get()):
            self.wallpaper.rolls = math.ceil(float(self.txtMetres.get()) / 10.05) #math.ceil as you always need 1 roll up when a decimal
        else:
            self.wallpaper.rolls = 0
        self.calcCost()
        self.lblRolls.config(text=f"Rolls: {self.wallpaper.rolls}")

    def addClick(self) -> None:
        """Manages either adding a wallpaper to the order, or modifying a wallpaper in modification and returning to the other window"""
        
        if self.wallpaper.rolls > 0: #Check to ensure more than 1 roll is being added
            if self.modIndex > -1: #If modindex is > -1 then that means this window was accessed from the order window and is being used for modification, thus a wallpaper needs updating
                self.order[self.modIndex] = self.wallpaper
                self.reset(True)
                self.modIndex = -1
                self.drawWindow(self.root)
                ViewOrder(self.order, self.root)
            else:
                messagebox.showinfo("Success", "Successfully added the wallpaper to basket!")
                self.order.append(self.wallpaper)
                self.lblTotalCost.config(text=f"Order Cost: £{Cost.calcOrderCost(self.order)}")
                self.wallpaper = Wallpaper()
                self.reset()
        else:
            messagebox.showerror("Failure", "Invalid metre entry!")

    def orderClick(self) -> None:
        """Opens the order window"""
        
        if self.modIndex > -1: #Check if this window was accessed through the order window
            self.originalRoot.destroy() #Destroys the original root if so, as this is the original order window and you want it out of memory
            self.modIndex = -1
            
        self.reset(True) #This makes sure if they come back to the window any half complete wallpapers are cleared
        ViewOrder(self.order, self.root)

    def calcCost(self) -> None:
        """Used to calculate the individual cost of a wallpaper"""
        
        stringDisp = format(self.wallpaper.calcFinalCost(), ",.2f")
        self.lblCost.config(text=f"Cost: £{stringDisp}")


    def reset(self, destroy: bool = False) -> None:
        """Resets the window to display the default settings for wallpaper"""
        
        if destroy: #For resets where the page isn't closed, destroying the root is unecessary and looks messy
            self.root.destroy() #This clean destroy was the only way to fix a bug when navigating between menus in a specific manner, otherwise ghost self.originalRoots could get caught
            self.initRoot()
            self.drawWindow(self.root)
        
        self.wallpaper = Wallpaper()
        self.liningOp.set(int(self.wallpaper.liningPaper))
        self.pasteOp.set(int(self.wallpaper.paste))
        self.modificationOp.set(self.wallpaper.addition.name)
        
        self.txtMetres.delete(0, END)
        self.txtMetres.insert(0, round(self.wallpaper.rolls * 10.05, 2)) #Rounded to as big numbers sometimes have very small decimal number due to float innacuracy
        
        self.lblRolls.config(text=f"Rolls: {self.wallpaper.rolls}")
        
        self.lblQuality.config(text=self.wallpaper.quality.name.capitalize())
        self.cvsMainDisp.delete("all")
        Draw.drawWallpaper(self.wallpaper.quality, self.cvsMainDisp, self.wallpaper.colour) #Redraws needed to update colour
        Draw.drawWallpaper(WallpaperQualities.CHEAP, self.cvsFirstOp, self.wallpaper.colour)
        Draw.drawWallpaper(WallpaperQualities.EXPENSIVE, self.cvsSecondOp, self.wallpaper.colour)
        self.additionsSelect()
        self.modificationsSelect()
        
    def rootFocus(self, event: Event) -> None:
        """Called whenever the window is refocussed, used just for updating the total order cost when the winow is refocused after leaving the order window"""
        
        self.lblTotalCost.config(text=f"Order Cost: £{Cost.calcOrderCost(self.order)}")

    def rootClose(self) -> None:
        """Called whenever the window is closed, performs a cleaner exit to ensure that other hidden windows don't hang the program"""
        
        exit()



class ViewOrder:
    """Class for the second page that allows viewing all wallpapers in the order, can be accessed only through the ViewWallpaper() window"""
    
    def __init__(self, order: list, root: Tk) -> None:
        """All paramateres must be passed values\n
        order must be a list of wallpapers, root must be the caller's root, so that it can be stored and removed later"""
        
        self.originalRoot = root
        root.withdraw() #Withdraw not destroy, as if destroyed the main root is closed exiting the program

        self.order = order #Used only for returning to the original window
        
        rootOrder = Toplevel()
        rootOrder.title("Wallpaper Designer")
        rootOrder.geometry("960x540+50+50")
        rootOrder.focus()
        rootOrder.grab_set()
        rootOrder.resizable(False, False)
        rootOrder.protocol('WM_DELETE_WINDOW', self.rootOrderClose)

        self.rootOrder = rootOrder

        self.barMain = Scrollbar()
        self.cvsHidden = Canvas(rootOrder) #Hiden widget used to enable scrolling, as Canvas is a scroll object
        self.backFrame = Frame() #Drawn ont cvsHidden so that the widgets

        self.lblTotalCost = Label()

        #Widgets used in drawing the scroll region
        self.frmOrdBack : Frame = []
        self.cvsOrd : Canvas = []
        self.lblOrdDet : Label = []
        self.btnEdit : Button = []
        self.spnRolls : Spinbox = []
        self.rollsOp : StringVar = [] #Stores the value of the scrollbars
        self.lblCost : Label = []

        self.drawWindow(rootOrder)

    def drawWindow(self, rootOrder: Tk) -> None:
        """Method used for drawing widgets"""
        
        rootOrder.update()
        self.cvsHidden.place(x=0, y=0, relheight=1, relwidth=1) #The scroll canvas works only if it's drawn over the entire scree

        #The back frame provides the visible area which can be changed, the height is equal to an offset of 80 (the height of the top of the window label) and then multiplies the number of entries by the height of the framestheir data is drawn to
        self.backFrame = Frame(self.cvsHidden, width=rootOrder.winfo_width(), height=len(self.order)*115+80)
        self.backFrame.bind('<Configure>', self.on_configure) #Boilerplate code to make scrolling work properly
        self.cvsHidden.create_window(0, 80, window=self.backFrame) #Creates the window that gets scrolled in the hidden region

        barBack = Frame(rootOrder, highlightbackground="black", highlightthickness=2) #This is an outline for the scroll bar as in Windows 11 the way it looks is different to Windows 10, making it difficult to see
        barBack.place(x=717, y=81, width=23, relheight=0.85) #RelHeight is just the percentage of the screen the bar takes up
        
        self.barMain = Scrollbar(barBack, command=self.cvsHidden.yview)
        rootOrder.update()
        self.barMain.place(x=0, y=0, relheight=1) #RelHeight 1 here as it's drawn to the barBack frame, meaning it's already the perfect height
        
        rootOrder.update()
        self.cvsHidden.configure(yscrollcommand=self.barMain.set) #Sets the scrollbar to act on the hidden canvas
        rootOrder.update()
        
        for i in range(len(self.order)): #For loop that creates all the widgets used for display, does not place
            self.frmOrdBack.append(Frame(self.backFrame, background="#C2C2C2", highlightbackground="black", highlightthickness=2, width=720, height=115))
            self.cvsOrd.append(Canvas(self.frmOrdBack[i], bg="white"))
            self.lblOrdDet.append(Label(self.frmOrdBack[i], bg="#C2C2C2", text=str(self.order[i]), font=tf.Font(size=16), justify=LEFT))
            self.btnEdit.append(Button(self.frmOrdBack[i], bg="orange", text="Edit"))
            self.rollsOp.append(StringVar(rootOrder, value=self.order[i].rolls))
            self.spnRolls.append(Spinbox(self.frmOrdBack[i], from_=0, to=10000, textvariable=self.rollsOp[i], font=tf.Font(size=14), state="readonly"))
            cost = format(self.order[i].calcFinalCost(), ",.2f") #For whatever reason Python gets unhappy with passing a format within formatted strings
            self.lblCost.append(Label(self.frmOrdBack[i], text=f"Cost: £{cost}", bg="#C2C2C2", font=tf.Font(size=12)))

        self.orderListDisp(rootOrder) #Used to place all the widgets
        Frame(self.backFrame, background="black").place(x=117, rely=0, width=4, relheight=1) #Places the dividing verticle black bars, placing them on the scroll region isn't necissary but fixes a small visual glitch where it'd overrun the list by 1 pixel
        Frame(self.backFrame, background="black").place(x=480, rely=0, width=4, relheight=1)


        rootOrder.update()
        
        #Places the Window's label, has to be done here so it covers the "hidden" canvas properly
        frmTop = Frame(rootOrder, bg="darkgray")
        frmTop.place(x=0, y=0, relwidth=rootOrder.winfo_width(), height=82)
        lblTitle = Label(frmTop, text="Order", bg="darkgray")
        lblTitle.config(font=tf.Font(size=36))
        lblTitle.place(anchor=NW, x=16, y=10)
        rootOrder.update()

        self.lblTotalCost = Label(rootOrder, text=f"Total Order Cost:\n£{Cost.calcOrderCost(self.order)}", bg="darkgray", font=tf.Font(size=18))
        self.lblTotalCost.place(x=barBack.winfo_x()+barBack.winfo_width(), y=frmTop.winfo_height(), width=rootOrder.winfo_width()-(barBack.winfo_x()+barBack.winfo_width()), height=128)
        rootOrder.update()

        btnPrint = Button(rootOrder, text="Print Order", bg="orange", fg="white", font=tf.Font(size=12, weight="bold"), command=self.printOrder)
        btnPrint.place(anchor=SW, x=self.lblTotalCost.winfo_x()+38, y=rootOrder.winfo_height()-16, width=148, height=56)

        #cvsBack is the button used for going back, an arrow is drawn onto it however so I used a canvas instead of a regular button
        cvsBack = Canvas(frmTop, bg="orange", width=32, height=32)
        cvsBack.bind("<Button-1>", self.backClick)
        cvsBack.place(anchor=NE, x=938, y=20)
        rootOrder.update()
        Draw.drawArrow(cvsBack)

        self.cvsHidden.yview_moveto(0) #Resets the scrollregion so display works properly

    def on_configure(self, event: Event) -> None:
        """Boilerplate method to make sure scrollbar updates properly"""
        
        self.cvsHidden.configure(scrollregion=self.cvsHidden.bbox('all'))
       
    def orderListDisp(self, rootOrder: Tk) -> None:
        """Method used to place all widgets used in the display list"""
        
        for i in range(len(self.order)):
            self.frmOrdBack[i].place(x=1, y=80+i*115)
            
            self.cvsOrd[i].place(x=24, y=24, width=65, height=65)
            rootOrder.update()
            Draw.drawWallpaper(self.order[i].quality, self.cvsOrd[i], self.order[i].colour)
            
            self.lblOrdDet[i].place(x=145, y=4)
            
            self.btnEdit[i].config(command=lambda i=i: self.editClick(i)) #This Lambda is to make it so that the command label can pass the index to the event method, basically tricks it into not passing by reference but instead by value
            self.btnEdit[i].place(anchor=NE, x=464, y=67, width=32, height=32)
            
            self.spnRolls[i].config(command=lambda i=i: self.rollsSelect(i))
            self.spnRolls[i].place(anchor=NW, x=528, y=30, width=128)
            rootOrder.update()
            
            #Simple label doesn't require any special work
            Label(self.frmOrdBack[i], text="Rolls:", font=tf.Font(size=12), fg="black", bg=self.frmOrdBack[i]["background"]).place(anchor=SW, x=self.spnRolls[i].winfo_x()-2, y=self.spnRolls[i].winfo_y()-2, width=self.spnRolls[i].winfo_width())
            
            self.lblCost[i].place(anchor=NW, x=self.spnRolls[i].winfo_x()-2, y=72, width=self.spnRolls[i].winfo_width())
            self.backFrame.config(height=len(self.order)*115+80)

    def printOrder(self) -> None:
        """Method used for printing order to directory, file called Order Details.txt"""
        
        f = open("Order Details.txt", "w") #Creates or opens file, if it exists
        text = "Order print out:\n"
        for i in range(len(self.order)):
            cost = format(self.order[i].calcFinalCost(), ",.2f") #Again, strangeness with Pthon's formatted strings and format() means this has t be done seperately
            #Most stuff that's printed comes from the override method in Wallpaper for converting to string 
            text += f"\nWallpaper {i+1}:\nColour: {self.order[i].colour.capitalize()}\n{str(self.order[i])}\n\
                        Number of rolls: {self.order[i].rolls} - ({round(self.order[i].rolls * 10.05, 2)} metres)\nCost: £{cost}\n"
        text += f"\n\nTotal cost:\n£{Cost.calcOrderCost(self.order)}"
        f.write(text) #Write replaces any text already in the document
        f.close

        messagebox.showinfo("Success", "Successfully printed to file!")

    def rollsSelect(self, i) -> None:
        """Used for removing from the list and increasing the number of rolls, """
        
        if int(self.rollsOp[i].get()) == 0: #Checks if the new value is 0, in which case rolls need to be removed
            self.frmOrdBack[i].destroy() #Destroying the back frame kills all the children
            
            del self.frmOrdBack[i] 
            del self.cvsOrd[i]
            del self.lblOrdDet[i]
            del self.btnEdit[i]
            del self.spnRolls[i]
            del self.lblCost[i]
            del self.rollsOp[i]
            del self.order[i]
            
            self.orderListDisp(self.rootOrder) #Replaces everything in the order list

            if len(self.order) < 4: #A bug occured when the screen wasn't filled with the order the scroll bar would get stuck in the middle, simply just moves it back to the top if this is the case
                self.cvsHidden.yview_moveto(0)
                if len(self.order) == 0:
                    self.cvsHidden.destroy() #This stops a pair of black bars from being left over
        else:
            self.order[i].rolls = int(self.rollsOp[i].get())

        for i in range(len(self.order)): #Updates the new cost of the wallpaper
            cost = format(self.order[i].calcFinalCost(), ",.2f")
            self.lblCost[i].config(text=f"Cost: £{cost}")
            
        self.lblTotalCost.config(text=f"Total Order Cost:\n£{Cost.calcOrderCost(self.order)}")

    def editClick(self, i) -> None:
        """Exits this window and move on to the previous window, providing it the index in the order where the modified wallpaper is located"""
        
        self.rootOrder.destroy()
        ViewWallpaper(Tk(), self.order[i], self.order, i)

    def backClick(self, event: Event) -> None:
        """Exits this window and returns to the previous one"""
        
        self.originalRoot.iconify()
        self.originalRoot.deiconify()
        self.rootOrder.destroy()

    def rootOrderClose(self) -> None:
        """Called whenever the window is closed, performs a cleaner exit to ensure that other hidden windows don't hang the program"""
        
        exit()


class Draw:
    """Used for drawing the arrow on the return button and both wallpapers"""
    
    def drawWallpaper(quality: WallpaperQualities, canvas: Canvas, colour: str) -> None:
        """Method used for drawing the 2 different designs canvases can have, whenever a canvas design is drawn this method must be envoked"""
        
        cx = canvas.winfo_width(); cy = canvas.winfo_height()
        
        if quality == WallpaperQualities.EXPENSIVE:
            sx = (int)(cx / 5); sy = (int)(cy / 5) #Start locations for the draw, since each square is drawn halfway into another square, despite in total there being 10 squares per axis only / 5 is needed

            for i in range(5): #Single for loop used as 4 squares are drawn each loop
                rsx = (sx / 2 * i); rsy = (sy / 2 * i) #End location for each draw, the / 2 is because each square is drawn only halfway into the other square
                
                if i % 2 == 0: #Checks whether the index is even, as ever other draw needs to fill in the shape
                    fillCol = colour
                else:
                    fillCol = canvas["background"]
            
                canvas.create_rectangle(0 + rsx, 0 + rsy, sx + rsx, sy + rsy, fill=fillCol, outline=colour) #Top left
                canvas.create_rectangle(0 + rsx, cy - sy - rsy, sx + rsx, cy - rsy, fill=fillCol, outline=colour) #Bottom left
                canvas.create_rectangle(cx - rsx - sx, 0 + rsy, cx - rsx, sy + rsy, fill=fillCol, outline=colour) #Top right
                canvas.create_rectangle(cx - rsx - sx, cy - rsy - sy, cx - rsx, cy - rsy, fill=fillCol, outline=colour) #Bottom right
        else:
            mod = float(cx - 4) / 52 #mod is used to effect the percentage size of the design, so it can be drawn to canvases of varying size
            
            for y in range(2):
                sx = 2; sy=(y + 1) * 15 + 9 #Start draw locations, sy is multiplied by 15 (as that's the height of one star) and then has 9 added to assist with centring it properly
                
                for x in range(5): #Draws 2 overlapping triangles to get the star shape display
                    canvas.create_polygon(sx*mod,sy*mod,
                                          (sx+5)*mod, (sy-15)*mod,
                                          (sx+10)*mod, sy*mod,
                                          fill=colour, outline=colour)
                    
                    canvas.create_polygon(sx*mod, (sy-10)*mod,
                                          (sx+5)*mod, (sy+5)*mod,
                                          (sx+10)*mod,(sy-10)*mod,
                                          fill=colour, outline=colour)
                    
                    sx += 10 #Adds 10 as each star is 10 wide

    def drawArrow(canvas: Canvas, colour: str = "white") -> None:
        """Small subroutine used to draw the arrow on the order screen's return button"""
        
        cx = canvas.winfo_width(); cy = canvas.winfo_height()
        canvas.create_line(6, cy/2, cx-6, cy/2, fill=colour, width=3)
        canvas.create_line(5, cy/2, cx/2, cy/4, fill=colour, width=3)
        canvas.create_line(5, cy/2, cx/2, cy-cy/4, fill=colour, width=3)

class IsNumber():
    """Class used just for checking if a string is a number, invoke IsNumber.check()"""
    #Python's isDigit(), isNumeric() and isDecimal() all return false if a decimal is present, thus this class is needed
    
    def check(input: str) -> bool:
        """Utilises regex to determine if a provided string is a number, decimal or not"""
        
        #Finally my knowledge in Regex came to use!!
        #^ - Start of string, \d+ - One or more digits [0-9], ()? - Zero or one of whats inside the brackets, . - Literally checks for [.] character, $ - End of string
        if re.match("^\d+(.\d+)?$", input):
            return True
        return False
    
class Cost():
    """Class used for calculating the total order cost, call calcOrderCost"""
    
    def calcOrderCost(order: list) -> str:
        """Calculates the total order cost and returns it in format 'x.xx'"""
        
        orderCost = 0
        for i in range (len(order)):
            orderCost += order[i].calcFinalCost()
        return format(orderCost, ",.2f")

Main.mainLoop() #Start call for the entire program