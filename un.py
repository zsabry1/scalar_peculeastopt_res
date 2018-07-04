from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from super_rectangle import Draw_Rectangle, Draw_Ellipse, Draw_Lasso

# Custom toolbar
class CustomToolbar(NavigationToolbar2TkAgg, Draw_Rectangle, Draw_Ellipse, Draw_Lasso):
    x = []
    y = []
    canvas_main = []
    main_plot = []
    canvas_hist = []
    hist_plot = []

    def __init__(self, canvas_, parent_):
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
            ('Rectangle', 'Draw Rectangle', 'subplots', 'rectangle'),
            ('Ellipse', 'Draw Ellipse', 'subplots', 'ellipse'),
            ('Lasso', 'Draw lasso', 'subplots', 'lasso'),)
        NavigationToolbar2TkAgg.__init__(self,canvas_,parent_)

    def rectangle(self):
        print('This is a rectangle')
        print(CustomToolbar.x)
        print(CustomToolbar.y)
        a = Draw_Rectangle(CustomToolbar.x, CustomToolbar.y, CustomToolbar.canvas_main, CustomToolbar.main_plot.get_axes())
        a.show()
        #self.x = x
        #self.y = y
        #print(self.x)
        #print(self.y)


    def ellipse(self):
        print('This is an ellipse')

    def lasso(self):
#        super_rectangle.Draw_ellipse(RA, DEC)
        ax = plt.gca() ## get axis handle
        print(ax.get_offsets())
#        print(self.canvas.figure.get_xydata())
