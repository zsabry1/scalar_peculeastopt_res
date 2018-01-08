''' Fit_Astro class and Fit_Xray subclass documentation (version 2 of Fit). The Fit_Astro class is largely the same as the older version of the class (Fit) with the exception of syntax differences.

Contents (comment out the section you want to test):
Changes made to Fit (now Fit_Astro)                 lines 20-100
New features in Fit_Astro                           lines 183-216
Fit_Xray subclass example                           lines 221-274


NEW FEATURES V2
* Compatible with Python 2.7 and 3.5
* Syntax changes in class inputs (init and bds are input in the fitting functions, not class header)
* New subclass Fit_Xray easily fits and plots xray surface brightness and electron density (electron density still work in progress)
* New function to main class (Fit_Astro) fit_subcluster (double gaussian formula hardcoded in)
* view_plots allows you to plot as many histograms with varying binwidths as you want
* read_fits prints mu1 and mu2 offset (use fit_subcluster)
* plot_fits plots double gaussian constituent curves (use fit_subcluster)

'''

## Import data reading modules and Fit class

import numpy as np
from fitting_class import Fit_Astro, Fit_Xray
from scipy.special import beta, betainc ## This is the beta function that we need for our x-ray surface brightness formula

##################################################
## X-ray surface brightness model fitting tests ##
##################################################

## File name
data=np.loadtxt("zuhone_sb22.dat",skiprows=0)

## Column names
radius=data[:,0]*5.0517
sb=data[:,1]	
sb_err=data[:,2]

## Surface Brightness Function
I_x = lambda p,r: (p[1]*p[2]*((beta(p[3]-0.5,0.5))/(beta(p[4]-0.5,0.5)))*(r/p[0])**((-2)*p[3]+1))*np.piecewise((r/p[0]),[(r/p[0])**2<1,(r/p[0])**2>=1], [lambda A: 1-betainc(p[4]-0.5,0.5,A**2), lambda A: 0])  + (p[2]*(r/p[0])**((-2)*p[4]+1))*np.piecewise((r/p[0]),[(r/p[0])**2<1,(r/p[0])**2>=1],[lambda A: betainc(p[4]-0.5,0.5,A**2), lambda A: 1])

## Preparing fits
x_init=[72, 5, 26, 2, 2]
x_bds=([40, 0, 10, 0, 0],[90, 9, 50, 9, 9])


################# THIS IS WHERE DATA PREPARATION ENDS FOR X-RAY #################

''' First thing to do is to call the class name and enter the arguments in this order: xdata, ydata, and fit function. Y-data is optional because you could fit one dimensional data as well using this class. Fit function is also optional (because there are already two hardcoded fucntions in the class). Since we set the Fit class equal to xray, we must call xray every time we run a function from within the class'''

xray=Fit_Astro(radius, datay=sb, fitfunc=I_x)




''' Once we call the class and enter our arguments, we can now use the functions from within the class. Here, we just want to visualize the data, so we call the interactive view_plot function.'''

xray.view_plot()




''' Once we have an idea of what the plot looks like we can fit using bootstrap residuals or bootstrap input errors. In this case we call the fit_errors function becase we have a column of errors in our data (sb_err). Now, we must also input the initial guess and boundaries. Unless otherwise specified, iterations are set to 1000 and error calculations are set to asymmetric. To set symmetric errors, set mean=True '''

xray.fit_errors(x_init, x_bds, sb_err, iterations=10, mean=False)




''' Once we fit our function, we can call the read_fits function to read the parameters as well as the errors '''

xray.read_fits()




''' We can also plot the fitted function using the interactive plot_fit. '''

xray.plot_fit()




''' Use the p_spread function to get the spread of the parameters that were fitted. There is one histogram per fitted parameter. If we had 10 iterations, expect a population of 10 per parameter histogram.'''

xray.p_spread()




''' To calculate the reduced chi-square statistic, run the reduced_chi_sq function'''

#xray.reduced_chi_sq()




''' And to return the reduced chi-square statistic and degrees of freedom, use print as follows'''

#print('')
#print('Chi-squared statistic: ', xray.chi_square_statistic)
#print('Chi-squared degrees of freedom: ', xray.chi_square_df)




############################### BELOW HERE IS DATA PREPARATION FOR VELOCITIES ###############################

#########################################
## Double Gaussian model fitting tests ##
#########################################

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

## Gaussian Functions
triple  = lambda p, x: np.abs(p[0])*np.exp(-0.5*((x-p[1])/p[2])**2)+np.abs(p[3])*np.exp(-0.5*((x-p[4])/p[5])**2)+np.abs(p[6])*np.exp(-0.5*((x-p[7])/p[8])**2)
double  = lambda p, x: np.abs(p[0])*np.exp(-0.5*((x-p[1])/p[2])**2)+np.abs(p[3])*np.exp(-0.5*((x-p[4])/p[5])**2)
single  = lambda p, x: np.abs(p[0])*np.exp(-0.5*((x-p[1])/p[2])**2)

## Preparing fits
init  = [18, 69500, 1000, 7, 70500, 500.1]
bds=([1.0,65000,200, 0, 65000, 500],[20,75000,2000, 15, 75000, 500.2])

############################### DATA PREPARATION FOR VELOCITIES ENDS ###############################

'''Call the Fit class and enter the xdata and optional fit function. Since our data is one dimensional, there is no need to set ydata = to something'''

d_gauss=Fit_Astro(VEL, fitfunc=double)



''' We use the view_plot command to look at the data. Since this is one-dimensional data pick the hist option and, if you want, specify the binwidth. Can plot as many binwidths as you want.'''

d_gauss.view_plot()




''' Once you've seen the data, use the populate_bins function to set the binwidth on your data. This function sets y-data equal to the number of observations per bin. It also calculates the error by taking the square root per bin'''

d_gauss.populate_bins(250)




''' We fit using fit_errors again. Since populate_bins already calculated our errors, there is no need to enter the errors as an argument here. Here, we change the iterations to 100 here and we calculate symmetrical errors.'''

d_gauss.fit_errors(init, bds, iterations=100, mean=True)




''' Call read_fits to read the fitted parameters '''

d_gauss.read_fits()




''' Use plot_fit to plot the fitted parameters. Select either hist, scat, or hist_scat to fit your function it'''

d_gauss.plot_fit()




''' Finally, use the p_spread function to view the distribution of each function parameter '''

d_gauss.p_spread()



#####################################################
############  NEW FEATURES IN Fit_Astro  ############
#####################################################


'''Using the new function fit_subcluster will allow you to see the offset between mu1 and mu2 as well as the constituent curves of the double Gaussian model. You do not need to specify a fitfunc in the class header to use fit_subcluster (it uses double Gaussian). First create Fit_Astro object with just xdata.'''


subcluster=Fit_Astro(VEL)


'''You can view the distribution of the velocities with different binwidths simultaneously now using view_plot. This is done by selecting hist, entering yes to specify binwidth, specify whatever binwidth, then when asked to specify another, type 'yes' and then another binwidth. The different binwidth plots will both appear with their title's representing the binwidth entered (ignore any errors that pop-up, I'll clean those up soon).'''


subcluster.view_plot()




'''Once you are satisfied with a binwidth, use fit_subcluster to input initial guess, boundaries, binwidth, then optionally specifying iterations and error types'''


subcluster.fit_subcluster(init, bds, 250, iterations=100)




'''You can then plot the fit and see the double Gaussian and its component curves'''


subcluster.plot_fit()


'''That's all that's new in the main class'''




#####################################################
################  Fit_Xray SUBCLASS #################
#####################################################

''' Load in data as usual '''

## File name
data_xray=np.loadtxt("zuhone_sb22.dat",skiprows=0)

## Column names
radius=data_xray[:,0]*5.0517
sb=data_xray[:,1]	
sb_err=data_xray[:,2]

## Preparing fits
x_init=[72, 5, 26, 2, 2]
x_bds=([40, 0, 10, 0, 0],[90, 9, 50, 9, 9])


''' This time, call the Fit_Xray class. You need to input xdata and ydata. You can optionally enter errors as show here by sigma=sb_err. If errors are not entered, the class will automatically fit using fit_residuals. '''

xrays=Fit_Xray(radius, sb, sb_err)





''' You can call any function in Fit_Astro (as long as it makes sense, don't call something like populate_bins since you're not fitting a histogram). Choose log to view the surface brightness data.'''

xrays.view_plot()





''' Use fit_xray_sb to fit xray surface brightness. Enter initial guess, boundaries, and optionally specify iterations and error type. '''

xrays.fit_xray_sb(x_init, x_bds, iterations=100)





''' Use fit_xray_density to fit the electron density. BE WARNED, THIS IS PROBABLY VERY WRONG DUE TO ME NOT BEING ENTIRELY SURE WHAT THE X-RAY FUNCTION IS. The idea here is you only need to fit the x-ray surface brightness and use its pfit values to plug into the x-ray density function (which I am not confident in my current density function).'''

xrays.fit_xray_density()





''' View side-by-side plots of x-ray surface brightness and electron density. This gives you an idea of what I am going for. However, the true X-ray density function must be coded. '''

xrays.xray_plots()









