from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
from super_rectangle import Draw_Rectangle, Draw_Ellipse, Draw_Lasso

# Custom toolbar
class CustomToolbar(NavigationToolbar2Tk, Draw_Lasso):
    x = []
    y = []
    canvas_main = []
    main_plot = []
    canvas_hist = []
    hist_plot = []
    collections = []
    xlabel = []
    ylabel = []

    def __init__(self, canvas_, parent_):
        self.a = []
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
#            ('Rectangle', 'Draw Rectangle', 'subplots', 'rectangle'),
#            ('Ellipse', 'Draw Ellipse', 'subplots', 'ellipse'),
            ('Lasso', 'Draw lasso', 'subplots', 'lasso'),)
        NavigationToolbar2Tk.__init__(self,canvas_,parent_)

    def lasso(self):
        self.a = Draw_Lasso(CustomToolbar.x, CustomToolbar.y, CustomToolbar.canvas_main, CustomToolbar.main_plot, 
                        CustomToolbar.collections, CustomToolbar.xlabel, CustomToolbar.ylabel)

    def disable_lasso(self):
        try:
            self.a.disconnect()
        except AttributeError:
            pass

#    def rectangle(self):
#        a = Draw_Rectangle(CustomToolbar.x, CustomToolbar.y, CustomToolbar.canvas_main, CustomToolbar.main_plot, CustomToolbar.xlabel, CustomToolbar.ylabel)
        
        #CustomToolbar.canvas_main.draw()
        #self.x = x
        #self.y = y
        #print(self.x)
        #print(self.y)


#    def ellipse(self):
#        a = Draw_Ellipse(CustomToolbar.x, CustomToolbar.y, CustomToolbar.canvas_main, CustomToolbar.main_plot, CustomToolbar.xlabel, CustomToolbar.ylabel)

