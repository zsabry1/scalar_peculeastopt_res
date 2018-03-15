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


## Figures and constants
f = Figure(figsize=(8,5))
g = Figure(figsize=(6,6)) ## Make this square
h = Figure(figsize=(4,2))

sl=3E5
conv=np.pi/180

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
            a.hist(self.datax, color='blue', bins=int(binN))
            canvas.draw()
        else:
            pass
        
        ## BINWIDTH SET TO LABEL ###


##-----------------------------------------------------------------------------------------------------------------------------------------------

class PageTwo(PageOne):
    def __init__(self,parent,controller):
        self.RA = []
        self.DEC = []
        self.redshift = []
        self.pec_VEL = []
        self.rec_VEL = []
        self.data = []
        self.H0 = 70.0
        self.z_mean = []
        self.wm = 0.3
        self.wv = 0.7
        self.RA_ent=[]
        self.DEC_ent=[]
        self.REDSHIFT_ent=[]
        self.H0_ent=[]
        self.wm_ent=[]
        self.wv_ent=[]
        self.latitude=[]
        self.longitude=[]
        self.mini_binwidth=[]
        self.upper = []
        self.lower = []
        self.combo = []
        self.vline_upper = []
        self.vline_lower = []
        self.bound_lower = []
        self.bound_upper = []
        self.bounded_RA = []
        self.bounded_DEC = []
        self.bounded_redshift = []
        self.bounded_pec_VEL = []
        self.bounded_latitude = []
        self.bounded_longitude = []
        self.bounded_z_mean = []
        self.bounded_rec_VEL = []

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
        self.H0_ent = ttk.Entry(self, width=15)
        self.H0_ent.insert(0, '70')
        self.H0_ent.grid(row=14, column=1, sticky='w')

        self.wm_ent = ttk.Entry(self, width=15)
        self.wm_ent.insert(0, '0.3')
        self.wm_ent.grid(row=15, column=1, sticky='w')

        self.z_mean_ent = ttk.Entry(self, width=15)
        self.z_mean_ent.grid(row=16, column=1, sticky='w')

        self.wv_ent = ttk.Entry(self, width=15)
        self.wv_ent.insert(0, '0.7')
        self.wv_ent.grid(row=17, column=1, sticky='w')

        ## Set data button
        button12 = ttk.Button(self, text='Set Data', command=self.getSkyCoords)
        button12.grid(row=11, column=1, sticky='sw')

        ## Set cosmology button
        button13 = ttk.Button(self, text='Set Cosmology', command= self.setCosmology)
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
        canvas_hist.get_tk_widget().grid(row=5, column=16, rowspan=50, columnspan=10, sticky='NSW')
        canvas_hist.show()

        ## Dropdown box label
        label25 = ttk.Label(self, text='Plot type:', font= NORML_FONT)
        label25.grid(row=102, column=4, sticky='w')

        ## Plot dropdown box
        self.combo = ttk.Combobox(self, width=22)
        self.combo['values'] = ('Celestial Coordinates','Cluster Centric', 'RA vs. Redshift', 'DEC vs. Redshift')
        self.combo.current(0)
        self.combo.grid(row=102, column=5, sticky='SW')

        ## Radiobuttions ## variable is option for grouping buttons
        hist_type=tk.IntVar()
        hist_type.set(1)
        radiobutton1=ttk.Radiobutton(self, text='Pec. Vel', variable=hist_type, value=1, command = lambda: self.Hist_Typer(canvas_hist, hist_plot, hist_type))
#        radiobutton1.invoke()
        radiobutton1.grid(row=68, column=18, sticky='w')

        radiobutton2=ttk.Radiobutton(self, text='Rec. Vel', variable=hist_type, value=2, command = lambda: self.Hist_Typer(canvas_hist, hist_plot, hist_type))
        radiobutton2.grid(row=68, column=19, sticky='w')

        ## Set plots
        button16 = ttk.Button(self, text='Set Plots', command = lambda: self.plot_Main_Hist(canvas_main, main_plot, canvas_hist, hist_plot, hist_type))
        button16.grid(row=103, column=4, sticky='w')

        ## Histogram labels
        ## Binwidth
        label21 = ttk.Label(self, text='Enter binwidth:', font= NORML_FONT)
        label21.grid(row=67, column=16, sticky='ew')

        self.mini_binwidth = ttk.Entry(self, width=6)
        self.mini_binwidth.grid(row=67, column=18, columnspan=2, sticky='ew')

        ## Set binwidth button
        button14 = ttk.Button(self, text='Set binwidth', command= lambda: self.pop_bins(canvas_hist, hist_plot))
        button14.grid(row=68, column=16, sticky='ew')


        ## Boundaries labels
        label22 = ttk.Label(self, text='Boundaries:', font= NORML_FONT)
        label22.grid(row=70, column=16, sticky='ew')

        ## Set crop button
        button15 = ttk.Button(self, text='Crop to bounds', command = lambda: self.drawBounds(canvas_hist, hist_plot))
        button15.grid(row=71, column=16, sticky='ew')

        ## Set update plots button
        button17 = ttk.Button(self, text='Update Plots', command = lambda: self.bounder(canvas_main, main_plot, canvas_hist, hist_plot))
        button17.grid(row=103, column=19, sticky='ew')

        ## Set reset plots button
        button18 = ttk.Button(self, text='Reset Plots', command = lambda: self.reset(canvas_main, main_plot, canvas_hist, hist_plot))
        button18.grid(row=103, column=16, sticky='ew')

        ## Boundaries labels
        label23 = ttk.Label(self, text='Upper', font= NORML_FONT)
        label23.grid(row=71, column=18, sticky='w')

        ## Boundaries labels
        label24 = ttk.Label(self, text='Lower', font= NORML_FONT)
        label24.grid(row=70, column=18, sticky='w')

        ## Boundaries entry boxes
        self.upper = ttk.Entry(self, width=6)
        self.upper.grid(row=71, column=19)

        self.lower = ttk.Entry(self, width=6)
        self.lower.grid(row=70, column=19)

        ## Information panel
        infor = tk.Canvas(self, width=250, height=75)
        infor.config(bg='white')
        infor.grid(row=1, column=16, rowspan=100, columnspan=10, sticky='NW')

        ## Coordinate information panel title
        label31 = ttk.Label(self, text='Coordinate Information', font= NORML_FONT, background='white')
        label31.grid(row=1, column=16, columnspan=10, sticky='NW')

        ## Coordinate Angular distance
        label33 = ttk.Label(self, text='Angular Separation (arcsec) =', font= SMALL_FONT, background='white')
        label33.grid(row=2, column=16, columnspan=10, sticky='NW')

        ## Coordinate linear separation
        label34 = ttk.Label(self, text='Linear Separation (kpc) = ', font= SMALL_FONT, background='white')
        label34.grid(row=3, column=16, columnspan=10, sticky='NW')
        

        ## Spacing on page
        self.grid_columnconfigure(3, minsize=20) ## Plot spacing
        self.grid_columnconfigure(0, minsize=5) ## Push from left edge
        self.grid_columnconfigure(15, minsize=15)
        self.grid_columnconfigure(2, minsize=20) ## Number of columns column
        self.grid_columnconfigure(4, minsize=20)
        self.grid_columnconfigure(17, minsize=10)
        self.grid_rowconfigure(2, minsize=10)
        self.grid_rowconfigure(3, minsize=20)
        self.grid_rowconfigure(4, minsize=20)
        self.grid_rowconfigure(12, minsize=20)
        self.grid_rowconfigure(18, minsize=10)
        self.grid_rowconfigure(69, minsize=10)
        self.grid_rowconfigure(66, minsize=10)
        self.grid_rowconfigure(10, minsize=10)
        self.grid_rowconfigure(101, minsize=10)
        self.grid_rowconfigure(20, minsize=10)

    def getSkyCoords(self):
        self.RA = []
        self.DEC = []
        self.redshift = []
        self.z_mean = []

        if len(self.data) == 0:
            popupmsg("Must enter RA, DEC, and redshift before setting data")
        else:
            try:
                self.RA = [x[int(self.RA_ent.get())-1] for x in self.data]
            except ValueError:
                popupmsg("Must enter RA column number")
            except IndexError:
                popupmsg("Invalid column number for x-data")
            
            try:
                self.DEC = [y[int(self.DEC_ent.get())-1] for y in self.data]
            except ValueError:
                popupmsg("Must enter DEC column number")
            except IndexError:
                popupmsg("Invalid column number for DEC")

            try:
                ## Starts to breakdown as speeds become relativistic
                self.redshift = [red[int(self.REDSHIFT_ent.get())-1] for red in self.data]
                self.z_mean = round(np.mean(self.redshift),3)
                vc = self.z_mean*sl
                
                ## Non-relativistic
                self.pec_VEL = sl*((self.redshift-self.z_mean)/(1+self.z_mean))
                self.rec_VEL = [x*sl for x in self.redshift]

                ## Set z_mean_ent text
                self.z_mean_ent.delete(0, len(str(self.z_mean)))
                self.z_mean_ent.insert(0, str(self.z_mean))

            except ValueError:
                popupmsg("Must enter redshift column number")
            except IndexError:
                popupmsg("Invalid column number for redshift data")

    def plot_Main_Hist(self, canvas_main, main_plot, canvas_hist, hist_plot, hist_type):
        main_plot.clear()
        hist_plot.clear()

        if len(self.bounded_pec_VEL) != 0:
            if hist_type.get() == 1:
#                binN=math.ceil((np.max(self.bounded_pec_VEL)-np.min(self.bounded_pec_VEL))/float(self.mini_binwidth.get()))

                hist_plot.hist(self.bounded_pec_VEL, color='blue', alpha=0.5, range=(min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)))

#                hist_plot.hist(self.bounded_pec_VEL, color='blue', bins=int(binN), alpha=0.5, range=(min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)))
                hist_plot.set_xlim([min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)])
                hist_plot.set_title('Peculiar Velocities')

            else:
#                binN=math.ceil((np.max(self.bounded_rec_VEL)-np.min(self.bounded_rec_VEL))/float(self.mini_binwidth.get()))

                hist_plot.hist(self.bounded_rec_VEL, color='blue', alpha=0.5, range=(min(self.bounded_rec_VEL), max(self.bounded_rec_VEL)))

#                hist_plot.hist(self.bounded_pec_VEL, color='blue', bins=int(binN), alpha=0.5, range=(min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)))
                hist_plot.set_xlim([min(self.bounded_rec_VEL), max(self.bounded_rec_VEL)])
                hist_plot.set_title('Recessional Velocities')

            ## Number of data points
            NumPoints=len(self.bounded_RA)
            hist_plot.text(0.98, 0.98, 'N = '+str(NumPoints), ha='right', va='top', transform=hist_plot.transAxes)

        else:
            if hist_type.get() == 1:
                hist_plot.hist(self.pec_VEL, color='blue', alpha=0.5, range=(min(self.pec_VEL), max(self.pec_VEL)))
                hist_plot.set_xlim([min(self.pec_VEL), max(self.pec_VEL)])
                hist_plot.set_title('Peculiar Velocities')
            else:
                hist_plot.hist(self.rec_VEL, color='blue', alpha=0.5, range=(min(self.rec_VEL), max(self.rec_VEL)))
                hist_plot.set_xlim([min(self.rec_VEL), max(self.rec_VEL)])
                hist_plot.set_title('Recessional Velocities')

            ## Number of data points
            NumPoints=len(self.RA)
            hist_plot.text(0.98, 0.98, 'N = '+str(NumPoints), ha='right', va='top', transform=hist_plot.transAxes)

        canvas_hist.draw()


        ## Plotting celestial coordinates
        if self.combo.get() == 'Celestial Coordinates':
            if len(self.bounded_RA) != 0:
                main_plot.plot(self.bounded_RA, self.bounded_DEC, 'o')
                main_plot.set_xlabel('RA')
                main_plot.set_ylabel('DEC')
                canvas_main.draw()
            else:
                main_plot.plot(self.RA, self.DEC, 'o')
                main_plot.set_xlabel('RA')
                main_plot.set_ylabel('DEC')
                canvas_main.draw()

        if self.combo.get() == 'RA vs. Redshift':
                if len(self.bounded_RA) != 0:
                    main_plot.plot(self.bounded_redshift, self.bounded_RA, 'o')
                    main_plot.set_xlabel('Redshift')
                    main_plot.set_ylabel('RA')
                    canvas_main.draw()
                else:
                    main_plot.plot(self.redshift, self.RA, 'o')
                    main_plot.set_xlabel('Redshift')
                    main_plot.set_ylabel('RA')
                    canvas_main.draw()

        if self.combo.get() == 'DEC vs. Redshift':
                if len(self.bounded_RA) != 0:
                    main_plot.plot(self.bounded_redshift, self.bounded_DEC, 'o')
                    main_plot.set_xlabel('Redshift')
                    main_plot.set_ylabel('DEC')
                    canvas_main.draw()
                else:
                    main_plot.plot(self.redshift, self.DEC, 'o')
                    main_plot.set_xlabel('Redshift')
                    main_plot.set_ylabel('DEC')
                    canvas_main.draw()

        ## Plotting cluster centric coordinates
        if self.combo.get() == 'Cluster Centric':
            if len(self.bounded_RA) != 0:
                ## converting RA & DEC to radian, getting center
                gal_RA=[x*conv for x in self.bounded_RA]
                gal_DEC=[x*conv for x in self.bounded_DEC]
                cen_RA=np.mean(self.bounded_RA)*conv
                cen_DEC=np.mean(self.bounded_DEC)*conv
                mems=len(self.bounded_RA)

            else:
                ## converting RA & DEC to radian, getting center
                gal_RA=[x*conv for x in self.RA]
                gal_DEC=[x*conv for x in self.DEC]
                cen_RA=np.mean(self.RA)*conv
                cen_DEC=np.mean(self.DEC)*conv
                mems=len(self.RA)

            angle_RA=[]
            for i in range(mems):
                angle_RA.append(np.arccos(np.sin(cen_RA)*np.sin(gal_RA[i])+np.cos(cen_RA)*np.cos(gal_RA[i])*(np.cos(cen_DEC-cen_DEC)))*(180/np.pi))
            angle_RA=np.array(angle_RA) ## Degrees

            angle_DEC=[]
            for i in range(mems):
                angle_DEC.append(np.arccos(np.sin(cen_RA)*np.sin(cen_RA)+np.cos(cen_RA)*np.cos(cen_RA)*(np.cos(cen_DEC-gal_DEC[i])))*(180/np.pi))
            angle_DEC=np.array(angle_DEC) ## Degrees

            RA_diff=[]
            DEC_diff=[]
            for i in range(mems):
                RA_diff.append(cen_RA-gal_RA[i])
                DEC_diff.append(gal_DEC[i]-cen_DEC)
	
            ## getting the index of negative values
            east_ind=[i for i,x in enumerate(RA_diff) if x < 0]
            south_ind=[i for i,x in enumerate(DEC_diff) if x < 0]

            ## conversion to linear distances
            linear_RA=angle_RA*3600*3.696      ## This needs to be modified after cosmolgy function is complete
            linear_DEC=angle_DEC*3600*3.696
            mod_RA=linear_RA[east_ind]
            mod_DEC=linear_DEC[south_ind]

            ## converting latitude values that should be negative, negative via index
            new_lat=[]
            for i in range(mems):
                if linear_RA[i] in mod_RA:
                    new_lat.append(linear_RA[i]*-1) ##east
                else:
                    new_lat.append(linear_RA[i])

            ## converting longitude values that should be negative, negative via index
            new_long=[]
            for i in range(mems):
                if linear_DEC[i] in mod_DEC:
                    new_long.append(linear_DEC[i]*-1) ##south
                else:
                    new_long.append(linear_DEC[i])

            self.latitude = new_lat
            self.longitude = new_long
            
            main_plot.plot(self.latitude, self.longitude, 'o')
            main_plot.set_xlabel('Kpc')
            main_plot.set_ylabel('Kpc')
            canvas_main.draw()


    def pop_bins(self, canvas_hist, hist_plot):
        hist_plot.clear()

        if len(self.bounded_RA) != 0:
            ## Number of bins
            binN=math.ceil((np.max(self.bounded_pec_VEL)-np.min(self.bounded_pec_VEL))/float(self.mini_binwidth.get()))
            hist_plot.hist(self.bounded_pec_VEL, color='blue', alpha=0.5, bins=int(binN), range=(min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)))
            hist_plot.set_xlim([min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)])

            hist_plot.set_title('Peculiar Velocities')

            ## Number of points
            NumPoints=len(self.bounded_RA)
            hist_plot.text(0.98, 0.98, 'N = '+str(NumPoints), ha='right', va='top', transform=hist_plot.transAxes)
            canvas_hist.draw()
        else:
            if len(self.pec_VEL) != 0:
                ## Number of bins
                binN=math.ceil((np.max(self.pec_VEL)-np.min(self.pec_VEL))/float(self.mini_binwidth.get()))
                hist_plot.hist(self.pec_VEL, color='blue', alpha=0.5, bins=int(binN), range=(min(self.pec_VEL), max(self.pec_VEL)))
                hist_plot.set_xlim([min(self.pec_VEL), max(self.pec_VEL)])

                hist_plot.set_title('Peculiar Velocities')

                ## Label of opened file
                NumPoints=len(self.RA)
                hist_plot.text(0.98, 0.98, 'N = '+str(NumPoints), ha='right', va='top', transform=hist_plot.transAxes)
                canvas_hist.draw()
            else:
                pass

    def Hist_Typer(self, canvas_hist, hist_plot, hist_type):            
        hist_plot.clear()



    def drawBounds(self, canvas_hist, hist_plot):
        del hist_plot.lines[:]
        
        try:
            if float(self.lower.get()) > float(self.upper.get()):
                popupmsg('Lower bound must be less than upper bound')
            else:
                self.vline_upper=hist_plot.axvline(float(self.upper.get()), color='green')
                self.vline_lower=hist_plot.axvline(float(self.lower.get()), color='green')

                if len(self.bounded_pec_VEL) != 0:
                    hist_plot.set_xlim([min(self.bounded_pec_VEL), max(self.bounded_pec_VEL)])
                else:
                    hist_plot.set_xlim([min(self.pec_VEL), max(self.pec_VEL)])

            ## Setting bounded data precursors
            self.bound_lower = float(self.lower.get())
            self.bound_upper = float(self.upper.get())

            canvas_hist.draw()

#            if len(self.bounded_pec_VEL) !=0:
#                hist_plot.set_xlim([min(self.pec_VEL), max(self.pec_VEL)])
                
#            ## MAKE BARS TO BE INCLUDED ORANGE
#            for i in range(len(self.RA)):
#                if self.
        except ValueError:
            pass


    def bounder(self, canvas_main, main_plot, canvas_hist, hist_plot, hist_type):
        self.bounded_RA = []
        self.bounded_DEC = []
        self.bounded_redshift = []
        self.bounded_pec_VEL = []
        
        ## Getting bounded conditions
        for i in range(len(self.pec_VEL)):
            if self.bound_lower <= self.pec_VEL[i] <= self.bound_upper:
                self.bounded_RA.append(self.RA[i])
                self.bounded_DEC.append(self.DEC[i])
                self.bounded_redshift.append(self.redshift[i])
#                self.bounded_pec_VEL.append(self.pec_VEL[i])

        ## Starts to breakdown as speeds become relativistic
#       self.redshift = [red[int(self.REDSHIFT_ent.get())-1] for red in self.data]

        self.bounded_z_mean = round(np.mean(self.bounded_redshift),3)
        vc = self.bounded_z_mean*sl
        self.bounded_pec_VEL = sl*((self.bounded_redshift-self.bounded_z_mean)/(1+self.bounded_z_mean))
        self.bounded_rec_VEL = [x*sl for x in self.bounded_redshift]

        ## Set z_mean_ent text
        if len(str(self.bounded_z_mean)) != 0:
            self.z_mean_ent.delete(0, len(str(self.bounded_z_mean)))
            self.z_mean_ent.insert(0, str(self.bounded_z_mean))
        else:
            self.z_mean_ent.delete(0, len(str(self.z_mean)))
            self.z_mean_ent.insert(0, str(self.bounded_z_mean))

        ## Plotting updated main and histogram
        self.plot_Main_Hist(canvas_main, main_plot, canvas_hist, hist_plot, hist_type)




    def reset(self, canvas_main, main_plot, canvas_hist, hist_plot, hist_type):
        self.bounded_RA = []
        self.bounded_DEC = []
        self.bounded_redshift = []
        self.bounded_pec_VEL = []

        ## Plotting main as OG
        self.plot_Main_Hist(canvas_main, main_plot, canvas_hist, hist_plot, hist_type)



    def setCosmology(self):
        self.H0 = self.H0_ent.get()
        self.z_mean = self.z_mean_ent.get()
        self.wm = self.wm_ent.get()
        self.wv = self.wv_ent.get()

        ## E function

        ## Initializing cosmology labels
#        label26 = ttk.Label(self, text="u'H\u2080' = 12", font= SMALL_FONT)
#        label27 = ttk.Label(self, text='2', font= SMALL_FONT)
#        label28 = ttk.Label(self, text='2', font= SMALL_FONT)
#        label29 = ttk.Label(self, text='2', font= SMALL_FONT)
#        label30 = ttk.Label(self, text='Cosmology Set at:', font=NORML_FONT)
#        label30.grid(row=21, column=1, sticky='w')
#        label26.grid(row=22, column=1, sticky='ew')
#        label27.grid(row=23, column=1, sticky='ew')
#        label28.grid(row=24, column=1, sticky='ew')
#        label29.grid(row=25, column=1, sticky='ew')


        ## Labels of current cosmology

#    def cosmology_formula(self):


#    def onpick1(self,event):
#        artist = event.artist
#        if isinstance(artist, AxesImage):
#            mouseevent = event.mouseevent
#            self.x = mouseevent.xdata
#            self.y = mouseevent.ydata


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
app.geometry("1024x650")
app.mainloop()


## Plotting and clicking-------------------------------------------------------------------------------------------------------------------------
def fmt(x, y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x = x, y = y)



class DataCursor(object):
    # http://stackoverflow.com/a/4674445/190597
    """A simple data cursor widget that displays the x,y location of a
    matplotlib artist when it is selected."""
    def __init__(self, artists, x = [], y = [], tolerance = 5, offsets = (-20, 20),
                 formatter = fmt, display_all = False):
        """Create the data cursor and connect it to the relevant figure.
        "artists" is the matplotlib artist or sequence of artists that will be 
            selected. 
        "tolerance" is the radius (in points) that the mouse click must be
            within to select the artist.
        "offsets" is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        "formatter" is a callback function which takes 2 numeric arguments and
            returns a string
        "display_all" controls whether more than one annotation box will
            be shown if there are multiple axes.  Only one will be shown
            per-axis, regardless. 
        """
        self._points = np.column_stack((x,y))
        self.formatter = formatter
        self.offsets = offsets
        self.display_all = display_all
        if not cbook.iterable(artists):
            artists = [artists]
        self.artists = artists
        self.axes = tuple(set(art.axes for art in self.artists))
        self.figures = tuple(set(ax.figure for ax in self.axes))

        self.annotations = {}
        for ax in self.axes:
            self.annotations[ax] = self.annotate(ax)

        for artist in self.artists:
            artist.set_picker(tolerance)
        for fig in self.figures:
            fig.canvas.mpl_connect('pick_event', self)

    def annotate(self, ax):
        """Draws and hides the annotation box for the given axis "ax"."""
        annotation = ax.annotate(self.formatter, xy = (0, 0), ha = 'right',
                xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
                )
        annotation.set_visible(False)
        return annotation

    def snap(self, x, y):
        """Return the value in self._points closest to (x, y).
        """
        idx = np.nanargmin(((self._points - (x,y))**2).sum(axis = -1))
        return self._points[idx]
    def __call__(self, event):
        """Intended to be called through "mpl_connect"."""
        # Rather than trying to interpolate, just display the clicked coords
        # This will only be called if it's within "tolerance", anyway.
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        annotation = self.annotations[event.artist.axes]
        if x is not None:
            if not self.display_all:
                # Hide any other annotation boxes...
                for ann in self.annotations.values():
                    ann.set_visible(False)
            # Update the annotation in the current axis..
            x, y = self.snap(x, y)
            annotation.xy = x, y
            annotation.set_text(self.formatter(x, y))
            annotation.set_visible(True)
            event.canvas.draw()

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
