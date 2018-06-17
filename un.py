from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import super_rectangle 

# Custom toolbar
class CustomToolbar(NavigationToolbar2TkAgg):
    def plot_axes(self):
        # This function currently makes it so that the 'original view' is lost
        # TODO Fix the above bug
        print(self.canvas.figure.axes[0])
        #print(self.canvas.figure.axes[1])

    def rectangle(self):
        print('This is a rectangle')

    def ellipse(self):
        print('This is an ellipse')

    def lasso(self):
#        super_rectangle.Draw_ellipse(RA, DEC)
        ax = plt.gca() ## get axis handle
        print(ax.get_offsets())
#        print(self.canvas.figure.get_xydata())

    def __init__(self,canvas_,parent_):
        self.toolitems = (
            # Name of tool, tool tip, icon save file, function to be called
            # Icons are saved in /home/zsabry/anaconda3/lib/python3.5/site-packages/matplotlib/mpl-data/images/
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            # TODO Get this poor thing a nice gif
            ('Axes', 'Zoom in on region of interest (10-60)', 'subplots', 'plot_axes'),
            ('Rectangle', 'Draw Rectangle', 'subplots', 'rectangle'),
            ('Ellipse', 'Draw Ellipse', 'subplots', 'ellipse'),
            ('Lasso', 'Draw lasso', 'subplots', 'lasso'),)
        NavigationToolbar2TkAgg.__init__(self,canvas_,parent_)
