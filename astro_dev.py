import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import numpy as np
import math

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

LARGE_FONT=("Verdana", 12) ## Font specs
NORML_FONT=("Verdana", 10)
SMALL_FONT=("Verdana", 8)
style.use('ggplot')


## Figures
f = Figure(figsize=(8,5))
g = Figure(figsize=(6,6))
h = Figure(figsize=(4,2))

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

        button2 = ttk.Button(self, text='Sky Coordinates', command=lambda: controller.show_frame(PageTwo))
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
        self.bins = []
        self.datax_bins = []
        self.datay_hist = []
        self.datay = []
        self.sigma = []
        tk.Frame.__init__(self, parent)

        ## Label of page
        label1 = ttk.Label(self, text='Data Visualization', font=LARGE_FONT)
        label1.grid(row=0, column=1, columnspan=2)

        ## Navigate Home
        button1 = ttk.Button(self, text='Back to Home', command = lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=1, columnspan=2, sticky='ew')


        ## Open file
        button2 = ttk.Button(self, text='Browse Data', command= lambda: self.askopenfile(5,2,3,1))
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

        ## getResponse buttons
        button5 = ttk.Button(self, text='Set binwidth', command = lambda: self.populate_bins(canvas, a))
        label9 = ttk.Label(self, text='Enter binwidth:', font= NORML_FONT)

        ## Toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.grid(row=0,column=4, columnspan=100, sticky='ew')
        #toolbar.update()

        ## Set plot button
        button4 = ttk.Button(self, text='Set Plot', command = lambda: self.getResponse(canvas, a, button5, label9))
        button4.grid(row=102, column=4, sticky='sw')


    def askopenfile(self, x1, y1, x2, y2): ## Read all data types
        file_name=tk.filedialog.askopenfilename(initialdir = '/Desktop', title="Select data file", filetypes=(("dat files", "*.dat"), ("text files", "*.txt"), ("csv files", "*.csv"), ("all files", "*.*")))
        try:
            self.data=np.loadtxt(str(file_name), skiprows=0)
        except FileNotFoundError:
            return
        try:
            numcols=len(self.data[0])
        except IndexError:
            popupmsg("The data file is empty")
            
        ## Display number of colums
        label3 = ttk.Label(self, text=str(numcols), font=NORML_FONT)
        label3.grid(row=x1, column=y1)

        ## Modifying file name to display and not be too long
        abb_file = file_name.rsplit('/',1)[1] # split after last /
        info = (abb_file[:20] + '...') if len(abb_file) > 20 else abb_file # if str > 25 characters, ellipsis

        ## Label of opened file
        filelabel= ttk.Label(self, text=info, font=SMALL_FONT)
        filelabel.grid(row=x2, column=y2, sticky='ew')


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


    def getResponse(self, canvas, a, button5, label9):
        a.clear()

        if len(self.data) == 0:
            popupmsg('Must set data first')

        if self.combo.get() == 'Histogram':
            self.binwidth = ttk.Entry(self, width=9)
            self.binwidth.grid(row=103, column=5, sticky='sw')

            ## Set data button placement
            button5.grid(row=104, column=4, sticky='sw')

            ## Label of data wrangling placement
            label9.grid(row=103, column=4, sticky='SW')

            ## Plotting histogram
            a.hist(self.datax, color='blue')
            canvas.draw()

        else:
            try:
                button5.grid_forget()
                label9.grid_forget()
                self.binwidth.grid_forget()
            except AttributeError:
                pass

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


    def populate_bins(self, canvas, a):
        a.clear()        

        if len(self.datax) != 0:
            ## Number of bins
            binN=math.ceil((np.max(self.datax)-np.min(self.datax))/float(self.binwidth.get()))

            ## Preparing historgram
            y,x=np.histogram(self.datax,int(binN))
            x=(x[1:]+x[:-1])/2 # for len(x)==len(y)
            data=np.vstack((x,y)).T
        
        ## Bins and their respective populations
            self.bins = binN
            self.datax_bins = data[:,0]
            self.datay_hist = data[:,1]
            self.sigma = data[:,1]**0.5

#            binN=math.ceil((np.max(self.datax)-np.min(self.datax))/float(binwidth))
            a.hist(self.datax, bins=int(binN))
            canvas.draw()
        else:
            pass
        
        ## BINWIDTH SET TO ###


##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageTwo(PageOne):
    def __init__(self,parent,controller):
        self.RA = []
        self.DEC = []
        self.redshift = []
        self.H0 = []
        self.z_mean = []
        self.wm = []
        self.wv = []
        self.RA_ent=[]
        self.DEC_ent=[]
        self.REDSHIFT_ent=[]
        self.mini_binwidth=[]
        self.upper = []
        self.lower = []

        tk.Frame.__init__(self, parent)
        label10 = tk.Label(self, text='Sky Coordinates', font=LARGE_FONT)
        label10.grid(row=0, column=1, columnspan=2)

        ## Navigate Home
        button10 = ttk.Button(self, text='Back to Home', command = lambda: controller.show_frame(StartPage))
        button10.grid(row=1, column=1, columnspan=2, sticky='ew')

        ## Open file
        button11 = ttk.Button(self, text='Browse Data', command = lambda: self.askopenfile(6,2,3,1))
        button11.grid(row=2, column=1, columnspan=2, sticky='ew')

        ## Label of data wrangling
        label11 = ttk.Label(self, text='Data Wrangling', font= LARGE_FONT)
        label11.grid(row=5, column=1, columnspan=2, sticky='SW')

        ## Number of columns
        label12 = ttk.Label(self, text='Number of columns = ', font= NORML_FONT)
        label12.grid(row=6, column=1, sticky='ew')

        ## Data variables labels
        label13 = ttk.Label(self, text='RA column #', font= NORML_FONT)
        label13.grid(row=7, column=1, sticky='w')

        label14 = ttk.Label(self, text='DEC column #', font= NORML_FONT)
        label14.grid(row=8, column=1, sticky='w')

        label15 = ttk.Label(self, text='REDSHIFT column #', font= NORML_FONT)
        label15.grid(row=9, column=1, sticky='ew')

        ## Data variables entries
        self.RA_ent = ttk.Entry(self, width=3)
        self.RA_ent.grid(row=7, column=2)

        self.DEC_ent = ttk.Entry(self, width=3)
        self.DEC_ent.grid(row=8, column=2)

        self.REDSHIFT_ent = ttk.Entry(self, width=3)
        self.REDSHIFT_ent.grid(row=9, column=2)

        ## Set data button
        button12 = ttk.Button(self, text='Set Data', command= self.getContent)
        button12.grid(row=11, column=1, sticky='sw')


        ## Cosmology
        label16 = ttk.Label(self, text='Cosmology', font=LARGE_FONT)
        label16.grid(row=13, column=1, sticky='sw')

        label17 = ttk.Label(self, text=u'H\u2080', font=NORML_FONT)
        label17.grid(row=14, column=2, sticky='sw')

        label18 = ttk.Label(self, text=u'\u03A9m', font=NORML_FONT) # u'\u03a9'
        label18.grid(row=15, column=2, sticky='sw')

        label19 = ttk.Label(self, text='z', font=NORML_FONT)
        label19.grid(row=16, column=2, sticky='sw')

        label20 = ttk.Label(self, text=u'\u03A9\u03BB', font=NORML_FONT)
        label20.grid(row=17, column=2, sticky='sw')

        ## Data variables entries
        self.H0 = ttk.Entry(self, width=15)
        self.H0.insert(0, '70')
        self.H0.grid(row=14, column=1, sticky='w')

        self.wm = ttk.Entry(self, width=15)
        self.wm.insert(0, '0.3')
        self.wm.grid(row=15, column=1, sticky='w')

        self.z_mean = ttk.Entry(self, width=15)
        self.z_mean.grid(row=16, column=1, sticky='w')

        self.wv = ttk.Entry(self, width=15)
        self.wv.insert(0, '0.7')
        self.wv.grid(row=17, column=1, sticky='w')

        ## Set cosmology button
        button13 = ttk.Button(self, text='Set Cosmology')#, command= self.cosmo)
        button13.grid(row=19, column=1, sticky='sw')


        ## Type of plot
        main_plot = g.add_subplot(111)
        hist_plot = h.add_subplot(111)

        ## Plotting canvas main
        canvas_main = FigureCanvasTkAgg(g, self)
        canvas_main.get_tk_widget().grid(row=1, column=4, rowspan=100, columnspan=10, sticky='NS')
        canvas_main.show()

        ## Toolbar canvas main
        toolbar = NavigationToolbar2TkAgg(canvas_main, self)
        toolbar.grid(row=0,column=4, columnspan=10, sticky='ew')
        #toolbar.update()

        ## Plotting canvas hist
        canvas_hist = FigureCanvasTkAgg(h, self)
        canvas_hist.get_tk_widget().grid(row=5, column=16, rowspan=50, columnspan=10, sticky='NS')
        canvas_hist.show()

        ## Histogram labels
        ## Binwidth
        label21 = ttk.Label(self, text='Enter binwidth:', font= NORML_FONT)
        label21.grid(row=67, column=16, sticky='ew')

        self.mini_binwidth = ttk.Entry(self, width=6)
        self.mini_binwidth.grid(row=67, column=18, columnspan=2, sticky='ew')

        ## Set binwidth button
        button14 = ttk.Button(self, text='Set binwidth')#, command= self.cosmo)
        button14.grid(row=68, column=16, sticky='ew')

        ## Boundaries labels
        label22 = ttk.Label(self, text='Boundaries:', font= NORML_FONT)
        label22.grid(row=70, column=16, sticky='ew')

        ## Set crop button
        button15 = ttk.Button(self, text='Crop to bounds')#, command= self.cosmo)
        button15.grid(row=71, column=16, sticky='ew')

        ## Boundaries labels
        label23 = ttk.Label(self, text='Upper', font= NORML_FONT)
        label23.grid(row=70, column=18, sticky='w')

        ## Boundaries labels
        label24 = ttk.Label(self, text='Lower', font= NORML_FONT)
        label24.grid(row=71, column=18, sticky='w')

        ## Boundaries entry boxes
        self.upper = ttk.Entry(self, width=6)
        self.upper.grid(row=70, column=19)

        self.lower = ttk.Entry(self, width=6)
        self.lower.grid(row=71, column=19)

        ## Spacing on page
        self.grid_columnconfigure(3, minsize=20) ## Plot spacing
        self.grid_columnconfigure(0, minsize=5) ## Push from left edge
        self.grid_columnconfigure(15, minsize=15)
        self.grid_columnconfigure(2, minsize=20) ## Number of columns column
        self.grid_columnconfigure(4, minsize=110)
        self.grid_columnconfigure(17, minsize=10)
        self.grid_rowconfigure(3, minsize=20)
        self.grid_rowconfigure(4, minsize=20)
        self.grid_rowconfigure(12, minsize=20)
        self.grid_rowconfigure(18, minsize=10)
        self.grid_rowconfigure(69, minsize=10)
        self.grid_rowconfigure(66, minsize=10)
        self.grid_rowconfigure(10, minsize=10)
#        self.grid_rowconfigure(103, minsize=20)


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
app.geometry("1024x600")
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

