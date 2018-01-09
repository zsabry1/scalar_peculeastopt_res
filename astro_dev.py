import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np

import tkinter as tk

LARGE_FONT=("Verdana", 12) ## Font specs
NORML_FONT=("Verdana", 10)
SMALL_FONT=("Verdana", 8)

def popupmsg(msg):
    popup = tk.Tk()


    popup.wm_title('!')
    label = tk.Label(popup, text=msg, font=NORML_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = tk.Button(popup, text='Okay', command=popup.destroy)
    B1.pack()
    popup.mainloop()


class AstroApp(tk.Tk):
    def __init__(self, *args, **kwargs): ##kwargs, passing through dictionaries

        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default='hook.bmp')  ## icon
        tk.Tk.wm_title(self, "Astro Fit client") ## title of app

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand = True)
        container.grid_rowconfigure(0, weight=1) ## priority
        container.grid_columnconfigure(0, weight=1) ## proiority

        ## Menubar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command= lambda: popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)




        self.frames = {} ## initializing dictionary, where the different pages go

        for F in (StartPage, PageOne, PageTwo, PageThree): ## Pages
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew') ## sticky = north, south, east, west (where it's aligned, stretch to size of window)


        self.show_frame(StartPage) ## What frame to show


    def show_frame(self, cont):
    
        frame = self.frames[cont] #cont is key, thrown into show_frame. self inherits
        frame.tkraise()    ## raise to the front

##-----------------------------------------------------------------------------------------------------------------------------------------------


class StartPage(tk.Frame): ## inherit all the stuff from the frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) ## main class, inherits from AstroApp
        label = tk.Label(self, text='Start Page', font=LARGE_FONT) ## Returned object to label
        label.pack(pady=10, padx=10) ## Padding on top and bottom to look neat

        ## Navigate pages from start
        button1 = tk.Button(self, text='Data Visualization', command=lambda: controller.show_frame(PageOne)) ## text on button, command = function
        button1.pack()

        button2 = tk.Button(self, text='Visit Page 2', command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text='Graph Page', command=lambda: controller.show_frame(PageThree))
        button3.pack()

### All above code is the foundation to the rest of the app, it's the baseline for displaying pages
    


##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        self.datax = []
        self.datay = []
        tk.Frame.__init__(self, parent)

        ## Label of page
        label1 = tk.Label(self, text='Data Visualization', font=LARGE_FONT)
        label1.grid(row=0, column=1)

        ## Navigate Home
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, sticky='ew')


        ## Open file
        button2 = tk.Button(self, text='Browse Data', command= self.askopenfile)
        button2.grid(row=2, column=1, sticky='ew')


        ## Label of data wrangling
        label2 = tk.Label(self, text='Data Wrangling', font= LARGE_FONT)
        label2.grid(row=4, column=1, sticky='ew')


        ## Spacing on page
        self.grid_columnconfigure(2, minsize=20)
        self.grid_columnconfigure(0, minsize=5)
        self.grid_rowconfigure(3, minsize=20)

        ## Plot setup
        f = Figure(figsize=(8,5))
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])



        ## Plotting
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=1, column=3, rowspan=100, columnspan=100, sticky='NS')
#        canvas.configure(scrollregion=(-200, -200, 200, 200))

        ## Toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.grid(row=0,column=3, sticky='ew')

#        toolbar.update()


    def askopenfile(self): ## Read all data types
            file_name=tk.filedialog.askopenfilename(initialdir = '/Desktop', title="Select text document", filetypes=(("text files", "*.txt"),("csv files", "*.csv"), ("dat files", "*.dat"), ("all files", "*.*")))
            self.datax=np.loadtxt(str(file_name), skiprows=0)
            print(self.datax)
            return(file_name)


        #return tkFileDialog.askopenfile(mode='r', **self.file_opt)

##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Two', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ## Navigate to home
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

##-----------------------------------------------------------------------------------------------------------------------------------------------


class PageThree(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Graph Page', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ## Navigate to home
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()


        f = Figure()
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

##-----------------------------------------------------------------------------------------------------------------------------------------------

app = AstroApp()
app.geometry("800x600")
app.mainloop()


## Possibly useful things------------------------------------------------------------------------------------------------------------------------

## Backgrounds
## w = tk.Canvas(self, width=200, height=100)
## w.config(bg='white')
## w.grid(row=1, column=3, rowspan=90, columnspan=100)

