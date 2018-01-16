import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import numpy as np

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

LARGE_FONT=("Verdana", 12) ## Font specs
NORML_FONT=("Verdana", 10)
SMALL_FONT=("Verdana", 8)
style.use('ggplot')


## Figures
f = Figure(figsize=(8,5))

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORML_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='Okay', command=popup.destroy)
    B1.pack()
    popup.mainloop()

def printer(thing):
    print(thing)


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

        ## Styling buttons
        self.style=ttk.Style()
        self.style.theme_use("clam")
        #('clam', 'alt', 'default', 'classic')

        ## Page label
        label = ttk.Label(self, text='Start Page', font=LARGE_FONT) ## Returned object to label
        label.pack(pady=10, padx=10) ## Padding on top and bottom to look neat

        ## Navigate pages from start
        button1 = ttk.Button(self, text='Data Visualization', command=lambda: controller.show_frame(PageOne)) ## text on button, command = function
        button1.pack()

        button2 = ttk.Button(self, text='Visit Page 2', command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text='Graph Page', command=lambda: controller.show_frame(PageThree))
        button3.pack()

### All above code is the foundation to the rest of the app, it's the baseline for displaying pages
    


##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        self.data = []
        self.datax = []
        self.datay = []
        self.datax_err=[]
        self.datay_err=[]
        self.ent1=[]
        self.ent2=[]
        self.ent3=[]
        self.ent4=[]
        self.binwidth=[]
        self.combo=[]
        tk.Frame.__init__(self, parent)

        ## Label of page
        label1 = ttk.Label(self, text='Data Visualization', font=LARGE_FONT)
        label1.grid(row=0, column=1, columnspan=2)

        ## Navigate Home
        button1 = ttk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, columnspan=2, sticky='ew')


        ## Open file
        button2 = ttk.Button(self, text='Browse Data', command= self.askopenfile)
        button2.grid(row=2, column=1, columnspan=2, sticky='ew')
        button2 = ttk.Button(self, text='Browse Data', command= self.askopenfile)
        button2.grid(row=2, column=1, columnspan=2, sticky='ew')

        ## Set data button
        button3 = ttk.Button(self, text='Set Data', command= self.getContent)
        button3.grid(row=10, column=1, sticky='sw')


        ## Label of data wrangling
        label2 = ttk.Label(self, text='Data Wrangling', font= LARGE_FONT)
        label2.grid(row=4, column=1, columnspan=2, sticky='SW')

        ## Number of columns
        label3 = ttk.Label(self, text='Number of columns = ', font= NORML_FONT)
        label3.grid(row=5, column=1, sticky='ew')

        ## Data variables labels
        label4 = ttk.Label(self, text='Enter x-data column # ', font= NORML_FONT)
        label4.grid(row=6, column=1, sticky='w')

        label5 = ttk.Label(self, text='Enter y-data column # ', font= NORML_FONT)
        label5.grid(row=7, column=1, sticky='w')

        label6 = ttk.Label(self, text='Enter x-error column #', font= NORML_FONT)
        label6.grid(row=8, column=1, sticky='ew')

        label7 = ttk.Label(self, text='Enter y-error column #', font= NORML_FONT)
        label7.grid(row=9, column=1, sticky='ew')

        ## Data variables entry
        self.ent1 = ttk.Entry(self, width=3)
        self.ent1.grid(row=6, column=2)

        self.ent2 = ttk.Entry(self, width=3)
        self.ent2.grid(row=7, column=2)

        self.ent3 = ttk.Entry(self, width=3)
        self.ent3.grid(row=8, column=2)

        self.ent4 = ttk.Entry(self, width=3)
        self.ent4.grid(row=9, column=2)

        ## Spacing on page
        self.grid_columnconfigure(3, minsize=20)
        self.grid_columnconfigure(0, minsize=5)
        self.grid_columnconfigure(2, minsize=20)
        self.grid_columnconfigure(4, minsize=110)
        self.grid_rowconfigure(3, minsize=20)
        self.grid_rowconfigure(4, minsize=40)
        self.grid_rowconfigure(101, minsize=20)
        self.grid_rowconfigure(10, minsize=20)
        self.grid_rowconfigure(103, minsize=20)
#        self.grid_columnconfigure(6, minsize=700)

        ## Dropdown box label
        label8 = ttk.Label(self, text='Plot type: ', font= NORML_FONT)
        label8.grid(row=101, column=4, sticky='SW')

        ## getResponse buttons
        button5 = ttk.Button(self, text='Set binwidth')#, command= self.getContent)
        label9 = ttk.Label(self, text='Enter binwidth:', font= NORML_FONT)

        ## Plot dropdown box
        self.combo = ttk.Combobox(self)
        self.combo['values'] = ('Linear','Scatterplot', 'Histogram', 'Logarithmic')#, 'Semilogx', 'Semilogy')
        self.combo.current(0)
        self.combo.grid(row=101, column=5, sticky='SW')

        ## Plot setup
        a = f.add_subplot(111)

        ## Plotting
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=1, column=4, rowspan=100, columnspan=50, sticky='NS')
        canvas.show()

        ## Toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.grid(row=0,column=4, columnspan=100, sticky='ew')
        #toolbar.update()

        ## Set plot button
        button4 = ttk.Button(self, text='Set Plot', command = lambda: self.getResponse(canvas,a))
        button4.grid(row=102, column=4, sticky='sw')


    def askopenfile(self): ## Read all data types
        file_name=tk.filedialog.askopenfilename(initialdir = '/Desktop', title="Select data file", filetypes=(("dat files", "*.dat"), ("text files", "*.txt"), ("csv files", "*.csv"), ("all files", "*.*")))
        self.data=np.loadtxt(str(file_name), skiprows=0)
        try:
            numcols=len(self.data[0])
        except IndexError:
            popupmsg("The data file is empty")
            
        ## Display number of colums
        label3 = ttk.Label(self, text=str(numcols), font=NORML_FONT)
        label3.grid(row=5, column=2)

        ## Modifying file name to display and not be too long
        abb_file = file_name.rsplit('/',1)[1] # split after last /
        info = (abb_file[:20] + '...') if len(abb_file) > 20 else abb_file # if str > 25 characters, ellipsis

        ## Label of opened file
        filelabel= ttk.Label(self, text=info, font=SMALL_FONT)
        filelabel.grid(row=3, column=1, sticky='ew')


    def getContent(self):
        self.datax = []
        self.datay = []
        self.datax_err = []
        self.datay_err = []

        try:
            self.datax = [x[int(self.ent1.get())-1] for x in self.data]
        except ValueError:
            popupmsg("At least x-data must be entered")
        except IndexError:
            popupmsg("Invalid column number for x-data")
        
        try:
            self.datay = [y[int(self.ent2.get())-1] for y in self.data]
        except ValueError:
            pass
        except IndexError:
            popupmsg("Invalid column number for y-data")

        try:
            self.datax_err = [x_err[int(self.ent3.get())-1] for x_err in self.data]
        except ValueError:
            pass
        except IndexError:
            popupmsg("Invalid column number for x-error data")

        try:
            self.datay_err = [y_err[int(self.ent4.get())-1] for y_err in self.data]
        except ValueError:
            pass
        except IndexError:
            popupmsg("Invalid column number for y-error data")

#    def plot_histogram(self):
#        if len(self.binwidth) == 0:
#            fsdfsdf
#        else:
            
        

    def getResponse(self, canvas, a):
        a.clear()

        global button5, label9
        if len(self.data) == 0:
            popupmsg('Must set data first')

        if self.combo.get() == 'Histogram':
            ## Set data button placement
            button5.grid(row=104, column=4, sticky='sw')

            self.binwidth = ttk.Entry(self, width=9)
            self.binwidth.grid(row=103, column=5, sticky='sw')

            ## Label of data wrangling placement
            label9.grid(row=103, column=4, sticky='SW')

        if self.combo.get() != 'Histogram':
            button5.grid_forget()
            label9.grid_forget()
            self.binwidth.grid_forget()

        if self.combo.get() == 'Linear' and len(self.datax_err) == 0 and len(self.datay_err) == 0:
            try:
                a.plot(self.datax, self.datay)
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Linear' and len(self.datax_err) != 0 and len(self.datay_err) == 0:
            try:
                a.errorbar(self.datax, self.datay, xerr=self.datax_err)
                a.plot(self.datax, self.datay)
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Linear' and len(self.datax_err) == 0 and len(self.datay_err) != 0:
            try:
                a.errorbar(self.datax, self.datay, yerr=self.datay_err)
                a.plot(self.datax, self.datay)
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Linear' and len(self.datax_err) != 0 and len(self.datay_err) != 0:
            try:
                a.errorbar(self.datax, self.datay, xerr=self.datax_err, yerr=self.datay_err)
                a.plot(self.datax, self.datay)
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Scatterplot' and len(self.datax_err) == 0 and len(self.datay_err) == 0:
            try:
                a.plot(self.datax, self.datay, 'o')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Scatterplot' and len(self.datax_err) != 0 and len(self.datay_err) == 0:
            try:
                a.errorbar(self.datax, self.datay, xerr=self.datax_err, ls='none')
                a.plot(self.datax, self.datay, 'o')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Scatterplot' and len(self.datax_err) == 0 and len(self.datay_err) != 0:
            try:
                a.errorbar(self.datax, self.datay, yerr=self.datay_err, ls='none')
                a.plot(self.datax, self.datay, 'o')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Scatterplot' and len(self.datax_err) != 0 and len(self.datay_err) != 0:
            try:
                a.errorbar(self.datax, self.datay, xerr=self.datax_err, yerr=self.datay_err, ls='none')
                a.plot(self.datax, self.datay, 'o')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')


        if self.combo.get() == 'Logarithmic' and len(self.datax_err) == 0 and len(self.datay_err) == 0:
            try:
                a.loglog(self.datax, self.datay, 'o')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Logarithmic' and len(self.datax_err) != 0 and len(self.datay_err) == 0:
            try:
                a.loglog(self.datax, self.datay, 'o')
                a.errorbar(self.datax, self.datay, xerr=self.datax_err, ls='none')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Logarithmic' and len(self.datax_err) == 0 and len(self.datay_err) != 0:
            try:
                a.loglog(self.datax, self.datay, 'o')
                a.errorbar(self.datax, self.datay, yerr=self.datay_err, ls='none')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')

        if self.combo.get() == 'Logarithmic' and len(self.datax_err) != 0 and len(self.datay_err) != 0:
            try:
                a.loglog(self.datax, self.datay, 'o')
                a.errorbar(self.datax, self.datay, xerr=self.datax_err, yerr=self.datay_err, ls='none')
                canvas.draw()
            except ValueError:
                popupmsg('Must enter y-data')


#    def getPlot_Linear(self):
        
#        datax = [x[int(ent1.get())] for x in data]
#        datay = [y[int(ent2.get())] for y in data]
#        datax_err = [x_err[int(ent3.get())] for x_err in data]
#        datay_err = [y_err[int(ent4.get())] for y_err in data]
#        print(datax[0])
#        print(datay[0])
#        print(datax_err[0])
#        print(datay_err[0])

##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageTwo(PageOne):
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
#ani = animation.FuncAnimation(f, self.getResponses)
#app.geometry("800x600")
app.mainloop()


## Possibly useful things------------------------------------------------------------------------------------------------------------------------

## Backgrounds
## w = tk.Canvas(self, width=200, height=100)
## w.config(bg='white')
## w.grid(row=1, column=3, rowspan=90, columnspan=100)

## Icons
#To get this bitmap method to work on linux I needed .mbc files which looked nasty and B+W. After some searching I got this to work for gifs. #icon = tk.PhotoImage(file='Icon.gif') self.tk.call('wm', 'iconphoto', self._w, icon)﻿


## Dropdown box
        ## Data variable choices
#        choiceVar = tk.StringVar()
#        choices = ['a','b','c','d']
#        choiceVar.set(choices[0])

#        xdata_choice = ttk.Combobox(self, textvariable=choiceVar, values=choices)
#        xdata_choice.bind('<Configure>', self.on_combo_configure)
#        xdata_choice.grid(row=6, column=2, sticky='e')

