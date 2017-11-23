''' Astronomy Fit class test documentation '''

## Import data reading modules and Fit class

import numpy as np
from fitting_class import Fit
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

''' First thing to do is to call the class name and enter the bare minimum arguments in this order: function, initial, bounds, and xdata. Y-data is optional because you could fit one dimensional data as well using this class. Since we set the Fit class equal to xray, we must call xray every time we run a function from within the class'''

#xray=Fit(I_x, x_init, x_bds, radius, datay=sb)




''' Once we call the class and enter our arguments, we can now use the functions from within the class. Here, we just want to visualize the data, so we call the interactive view_plot function.'''

#xray.view_plot()




''' Once we have an idea of what the plot looks like we can fit using any one of three methods. In this case we call the fit_errors function becase we have a column of errors in our data (sb_err). Unless otherwise specified, iterations are set to 1000 and error calculations are set to asymmetric. To set symmetric errors, set mean=True '''

#xray.fit_errors(sb_err, iterations=10, mean=False)




''' Once we fit our function, we can call the read_fits function to read the parameters as well as the errors '''

#xray.read_fits()




''' We can also plot the fitted function using the interactive plot_fit. '''

#xray.plot_fit()




''' Use the p_spread function to get the spread of the parameters that were fitted. There is one histogram per fitted parameter. If we had 10 iterations, expect a population of 10 per parameter histogram.'''

#xray.p_spread()




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
VELR=dataR[:,2]
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

'''Call the Fit class and enter the function, initial, boundaries, and xdata arguments. Since our data is one dimensional, there is no need to set ydata = to something'''

d_gauss=Fit(double, init, bds, VEL)
d_gauss.fit_subcluster()
d_gauss.read_fits()



''' We use the view_plot command to look at the data. Since this is one-dimensional data pick the hist option and, if you want, specify the binwidth'''

#d_gauss.view_plot()




''' Once you've seen the data, use the populate_bins function to set the binwidth on your data. This function sets y-data equal to the number of observations per bin. It also calculates the error by taking the square root per bin'''

#d_gauss.populate_bins(250)




''' We fit using fit_errors again. Since populate_bins already calculated our errors, there is no need to enter the errors as an argument here. Here, we change the iterations to 100 here and we calculate symmetrical errors.'''

#d_gauss.fit_errors(iterations=100, mean=True)




''' Call read_fits to read the fitted parameters '''

#d_gauss.read_fits()




''' Use plot_fit to plot the fitted parameters. Select either hist, scat, or hist_scat to fit your function it'''

#d_gauss.plot_fit()




''' Finally, use the p_spread function to view the distribution of each function parameter '''

#d_gauss.p_spread()
