from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector, EllipseSelector, LassoSelector
from matplotlib.path import Path
import numpy as np

## Filename
dataR=np.loadtxt("rspecial2305.225.dat",skiprows=0)

## Column names & data preparation
RA=dataR[:,0]
DEC=dataR[:,1]
ELR=dataR[:,2]
REDSH=dataR[:,3]
RADD=dataR[:,4]
sl=3E5
zbar=np.mean(REDSH)
vc=zbar*sl
VEL=vc+sl*((REDSH-zbar)/(1+zbar))

class Draw_Lasso(object):

    def __init__(self, RA, DEC, color_other=0.1):
        self.fig, self.ax = plt.subplots()
        self.canvas = self.ax.figure.canvas
        self.collection = self.ax.scatter(RA, DEC) ## Picker = 5 for close radius
        self.color_other = color_other

        self.xys = self.collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = self.collection.get_facecolors()
        print(self.fc)
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, self.Npts).reshape(self.Npts, -1)

        self.lasso = LassoSelector(self.ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero([path.contains_point(xy) for xy in self.xys])[0]
        self.fc[:, -1] = self.color_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def show(self):
        plt.show()


class Draw_Ellipse(object):
    def __init__(self, RA, DEC):
        self.fig, self.ax = plt.subplots()
        self.canvas = self.ax.figure.canvas
        self.ax.scatter(RA, DEC) ## Picker = 5 for close radius
        self.RA = RA
        self.DEC = DEC
        self.RA_subset = []
        self.DEC_subset = []
        self.cache = []
        self.ind = []
        self.ellipse = EllipseSelector(self.ax, self.line_select_callback, drawtype='box', useblit=False, button=[1, 3], ## No mousewheel
                                                        minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    def line_select_callback(self, blc, trc): ## Bottom left corner, top right corner
        width = trc.xdata-blc.xdata
        height = trc.ydata-blc.ydata
        center = (blc.xdata+0.5*width, blc.ydata+0.5*height)
        angle = 0.0

        if width > height:
            smaj = 0.5*width
            smin = 0.5*height
        if width < height:
            smaj = 0.5*height
            smin = 0.5*width

#        if semi_axis1 == semi_axis2: ## Circle

        cos_angle = np.cos((3.14159265359/180.)*(180.-angle))
        sin_angle = np.sin((3.14159265359/180.)*(180.-angle))

        xc = self.RA - center[0]
        yc = self.DEC - center[1]

        xct = xc * cos_angle - yc * sin_angle
        yct = xc * sin_angle + yc * cos_angle 

        rad_cc = (xct**2/(width/2.)**2) + (yct**2/(height/2.)**2)

        colors_array = []

        for r in rad_cc:
            if r <= 1.:
                ## points in ellipse
                colors_array.append('red')
            else:
                ## points not in ellipse
                colors_array.append('blue')

        #self.ax.clear()
        #self.ax.scatter(self.RA,self.DEC,c=colors_array,linewidths=0.3)
        #self.canvas.draw_idle()

        background = self.canvas.copy_from_bbox(self.ax.bbox)
        # then during mouse move
        self.canvas.restore_region(background)
        self.ax.scatter(self.RA, self.DEC, c=colors_array, linewidths=0.3)
        self.ax.draw_artist(self.ax)
        self.canvas.blit(self.ax.bbox)
        # only after mouse has stopped moving
        self.canvas.draw_idle()

    def show(self):
        plt.show()


class Draw_Rectangle(object):
    def __init__(self, RA, DEC):
        self.fig, self.ax = plt.subplots()
        self.canvas = self.ax.figure.canvas
        self.ax.scatter(RA, DEC) ## Picker = 5 for close radius
        self.RA = RA
        self.DEC = DEC
        self.RA_subset = []
        self.DEC_subset = []
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.rectangle = RectangleSelector(self.ax, self.line_select_callback, drawtype='box', useblit=False, button=[1, 3], # No mousewheel
                                                minspanx=5, minspany=5, spancoords='pixels', interactive=True)

    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, self.y2 = erelease.xdata, erelease.ydata
        
        if self.x1 <= self.x2: ## Setting x boundaries
            self.RA_subset=[]
            self.DEC_subset=[]
            if self.y1 <= self.y2:
                for i in range(len(self.RA)): ## Drawing rectangle from bottom left
                    if self.x1 <= self.RA[i] <= self.x2 and self.y1 <= self.DEC[i] <= self.y2:
                        self.RA_subset.append(i)
                        self.DEC_subset.append(i)
            if self.y2 <= self.y1:
                for i in range(len(self.RA)): ## Drawing rectangle from top left
                    if self.x1 <= self.RA[i] <= self.x2 and self.y2 <= self.DEC[i] <= self.y1:
                        self.RA_subset.append(i)
                        self.DEC_subset.append(i)

        if self.x2 < self.x1: ## Setting x boundaries
            self.RA_subset=[]
            self.DEC_subset=[]
            if self.y1 < self.y2:
                for i in range(len(self.RA)): ## Drawing rectangle from bottom right
                   if self.x2 < self.RA[i] < self.x1 and self.y1 < self.DEC[i] < self.y2:
                       self.RA_subset.append(i)
                       self.DEC_subset.append(i)
            if self.y2 < self.y1:
                for i in range(len(self.RA)): ## Drawing rectangle from top right
                    if self.x2 < self.RA[i] < self.x1 and self.y2 < self.DEC[i] < self.y1:
                        self.RA_subset.append(i)
                        self.DEC_subset.append(i)

        colors_array = []

        for i in range(len(self.RA)):
            if i in self.RA_subset:
                ## points in ellipse
                colors_array.append('red')
            else:
                ## points not in ellipse
                colors_array.append('blue')


        background = self.canvas.copy_from_bbox(self.ax.bbox)
        # then during mouse move
        self.canvas.restore_region(background)
        self.ax.scatter(self.RA, self.DEC, c=colors_array, linewidths=0.3)
        self.ax.draw_artist(self.ax)
        self.canvas.blit(self.ax.bbox)
        # only after mouse has stopped moving
        self.canvas.draw_idle()

    def show(self):
        plt.show()


x = np.random.randint(0, 100, 20)
y = np.random.randint(0, 100, 20)

a = Draw_Ellipse(x, y)
a.show()
