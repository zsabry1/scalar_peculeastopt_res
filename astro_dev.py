import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk

LARGE_FONT=("Verdana", 12) ## Font specs

class AstroApp(tk.Tk):
    def __init__(self, *args, **kwargs): ##kwargs, passing through dictionaries

        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default='hook.bmp')  ## icon
        tk.Tk.wm_title(self, "Astro Fit client") ## title of app
        

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand = True)
        container.grid_rowconfigure(0, weight=1) ## priority
        container.grid_columnconfigure(0, weight=1) ## proiority

        self.frames = {} ## initializing dictionary, where the different pages go

        for F in (StartPage, PageOne, PageTwo, PageThree): ## Pages
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew') ## sticky = north, south, east, west (where it's aligned, stretch to size of window)


        self.show_frame(StartPage) ## What frame to show

##----------------------------------------------------------------------------------------------------------------------------------------------

    def show_frame(self, cont):
    
        frame = self.frames[cont] #cont is key, thrown into show_frame. self inherits
        frame.tkraise()    ## raise to the front


class StartPage(tk.Frame): ## inherit all the stuff from the frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) ## main class, inherits from AstroApp
        label = tk.Label(self, text='Start Page', font=LARGE_FONT) ## Returned object to label
        label.pack(pady=10, padx=10) ## Padding on top and bottom to look neat

        ## Navigate pages from start
        button1 = tk.Button(self, text='Visit Page 1', command=lambda: controller.show_frame(PageOne)) ## text on button, command = function
        button1.pack()

        button2 = tk.Button(self, text='Visit Page 2', command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text='Graph Page', command=lambda: controller.show_frame(PageThree))
        button3.pack()

### All above code is the foundation to the rest of the app, it's the baseline for displaying pages
    


##-----------------------------------------------------------------------------------------------------------------------------------------------

#    def open_file(self):
#            file_name=tk.filedialog.askopenfilename(initialdir = '/Desktop', title="Select text document", filetypes=(("Text files", "*.txt"),("all files", "*.*")))
#            return(file_name)


class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page One', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ## Navigate Home
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()


        ## Open file
        button2 = tk.Button(self, text='Browse', command= self.askopenfile)
        button2.pack()


    def askopenfile(self):
            file_name=tk.filedialog.askopenfilename(initialdir = '/Desktop', title="Select text document", filetypes=(("text files", "*.txt"),("csv files", "*.csv"), ("dat files", "*.dat"), ("all files", "*.*")))
            return(file_name)


        #return tkFileDialog.askopenfile(mode='r', **self.file_opt)

##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Two', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ## Navigate Home
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

##-----------------------------------------------------------------------------------------------------------------------------------------------


class PageThree(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Graph Page', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        ## Navigate pages
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

#        button2 = tk.Button(self, text='Browse', command=self.askopenfile)

#        button2 = tk.Button(self, text='Page One', command=lambda: controller.show_frame(PageOne))
#        button2.pack()

#        button3 = tk.Button(self, text='Page Two', command=lambda: controller.show_frame(PageTwo))
#        button3.pack()

        f = Figure(figsize=(5,5), dpi=100)
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
app.mainloop()
