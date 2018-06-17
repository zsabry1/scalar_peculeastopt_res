from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector, EllipseSelector, LassoSelector
from matplotlib.path import Path
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import numpy as np

# Custom toolbar
class CustomToolbar(NavigationToolbar2TkAgg):
    def plot_axes(self):
        # This function currently makes it so that the 'original view' is lost
        # TODO Fix the above bug
        print(self.canvas.figure.axes[0])
        #print(self.canvas.figure.axes[1])

    def __init__(self,canvas_,parent_):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            # TODO Get this poor thing a nice gif
            ('Axes', 'Zoom in on region of interest (10-60)', 'subplots', 'plot_axes'),)
        NavigationToolbar2TkAgg.__init__(self,canvas_,parent_)
