'''Version 1.1 of the astronomy fitting class for Python 2.7 & 3.5
Fit galaxy subclusters, xray surface brightness, or any formula using bootstrap residuals or input errors. Plot data and/or fitted function and return chi-square statistic'''

import pylab
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import iqr, chi2
import math
import matplotlib.pyplot as plt
import sys

class Fit_Astro(object):
    """
    Fit subcluster or any function using either bootstrap residuals or input errors. 
    Fitting is done for galaxy subclusters and includes plotting methods.
    """

    def __init__(self, datax, datay=[], fitfunc=[]):
        """ Initialize attributes for fit"""
        self.datax = datax
        self.datay = datay
        self.fitfunc= fitfunc
        self.pfit = []
        self.perr_sym = []
        self.perr_pos = []
        self.perr_neg = []
        self.sigma = []
        self.chi_square = []
        self.binwidth = []
        self.bins = []
        self.datax_bins=[]
        self.master_list = []
        self.residuals= []
        self.chi_square_statistic = []
        self.chi_square_df = []
        self.mu_offset = None

    def view_plot(self):
        """Look at simple plot of data before plotting fits"""
        
        print('')
        print('')
        print(">>> Select plot type to view the data:")
        print("")
        print('>>> For logarithmic plots, enter: log')
        print('>>> For histogram plot, enter: hist')
        print('>>> For scatter plot, enter: scat')
        print('')
        
        try:
            method=raw_input('> ')
        except NameError:
            method=input('> ')

        if method=='hist':
            try:
                plt.rcParams["patch.force_edgecolor"] = True
            except KeyError:
                pass

            print('')
            print('>>> Would you like to specify the binwidth?')
            print('>>> Please enter yes/no')
            print('')

            try:
                would=raw_input('> ')
            except NameError:
                would=input('> ')

            if would == 'no':
                plt.hist(self.datax, color='blue')


            elif would == 'yes':

                while would == 'yes':
                    print('')
                    print('>>> What binwidth would you like?')
                    print('')

                    try:
                        binwidth=raw_input('> ')
                    except NameError: ## Is there a better way of doing this?
                        binwidth=input('> ')

                    plt.figure()
                    plt.title(str(binwidth))
                    binN=math.ceil((np.max(self.datax)-np.min(self.datax))/float(binwidth))
                    plt.hist(self.datax, bins=int(binN))
                    plt.pause(0.001)

                    print('')
                    print('>>> Specify another binwidth?')
                    print('>>> Please enter yes/no')
                    print('')

                    try:
                        would=raw_input('> ')
                    except NameError:
                        would=input('> ')
                else:
                   plt.close('all') 
                    
        elif method=='log':
            try:
                plt.loglog(self.datax, self.datay, 'o')
            except ValueError:
                print('>>> There was no y-data entered')
                sys.exit()

        elif method=='scat':
            try:
                plt.plot(self.datax, self.datay, 'o')
            except ValueError:
                print('>>> There was no y-data entered')
                sys.exit()
        plt.show()



    def fit_subcluster(self, init, bds, binw, mean=False, iterations=1000):
        """ Fit subcluster of galaxy cluster using double Gaussian """

        self.fitfunc = lambda p, x: np.abs(p[0])*np.exp(-0.5*((x-p[1])/p[2])**2)+np.abs(p[3])*np.exp(-0.5*((x-p[4])/p[5])**2)

        self.populate_bins(int(binw))
        self.fit_errors(init, bds, iterations=iterations, mean=mean) # data_point**0.5 as errors
        self.mu_offset = round((self.pfit[4]-self.pfit[1]),2)


    def fit_errors(self, init, bds, sigma=[], iterations=1000, mean=False):
        """A bootstrap least_squares fit using standard errors. Can cylce through asymmetric errors 
        using median and 1-3 quartiles and symmetric errors using mean and standard deviation."""

        errfunc = lambda p, x, y: (y - self.fitfunc(p, x))


        if len(self.sigma)==0:
            self.sigma=sigma

        try:
            # Random data sets are generated and fitted
            ps = []
            for i in range(iterations):
                randomdataY=[]
                for k in range(len(self.sigma)):
                    randomDelta = np.random.normal(0., self.sigma[k], 1)
                    randomdataY.append(self.datay[k] + randomDelta)
                    out=np.concatenate(randomdataY)
                randomfit = least_squares(errfunc, init, bounds=bds, args=(self.datax, out))
                ps.append(randomfit.x)
            
            # Combining fits
            master_list=[]
            indexed=[]
            for k in range(len(ps[0])): # 0-6
                it=[]
                for i in range(len(ps)): # 0-1000
                    it.append(ps[i][k])
                master_list.append(it)
            self.master_list=master_list

        except ValueError:
            # Random data sets are generated and fitted
            ps = []
            for i in range(iterations):
                randomdataY=[]
                for k in range(len(self.sigma)):
                    randomDelta = np.random.normal(0., self.sigma[k], 1)
                    randomdataY.append(self.datay[k] + randomDelta)
                    out=np.concatenate(randomdataY)
                randomfit = least_squares(errfunc, init, bounds=bds, args=(self.datax_bins, out))
                ps.append(randomfit.x)
            
            # Combining fits
            master_list=[]
            indexed=[]
            for k in range(len(ps[0])): # 0-6
                it=[]
                for i in range(len(ps)): # 0-1000
                    it.append(ps[i][k])
                master_list.append(it)
            self.master_list=master_list

        except NameError:
            print("Must input errors")
            sys.exit()

        ##################################################################################
        ## Below here there are two paths: median and asymmetric, or mean and symmetric ##
        ##################################################################################

        ## Asymmetric error method
        if mean==False:
            pfit_bootstrap=[]
            perr_pos=[]
            perr_neg=[]
            for i in master_list:
                pfit_bootstrap.append(np.median(i))
                perr_pos.append(np.percentile(i,84)-np.median(i))
                perr_neg.append(np.median(i)-np.percentile(i,16))
            
            perr_bootstrap=[]
            for i in range(len(perr_pos)):
                perr_bootstrap.append(str('[+')+str(perr_pos[i])+str(',-')+str(perr_neg[i])+str(']'))

            self.pfit=pfit_bootstrap
            self.perr_pos=perr_pos
            self.perr_neg=perr_neg

        ## Symmetric error method
        else:
            pfit_bootstrap=[]
            perr_bootstrap=[]
            for i in master_list:
                pfit_bootstrap.append(np.median(i))
                perr_bootstrap.append(np.std(i))

            self.pfit=pfit_bootstrap
            self.perr_sym=perr_bootstrap

        return (pfit_bootstrap, perr_bootstrap)



    def fit_residuals(self, init, bds, iterations=1000, yerr_systematic=0, mean=False):
        """A bootstrap least_squares fit using residuals as errors. Can cylce through asymmetric errors
        errors using median and 1-3 quartiles and symmetric errors using mean and standard deviation."""


#        self.init=init
#        self.bds=bds

        errfunc = lambda p, x, y: (y - self.fitfunc(p, x))

        # Fit first time
        pfit = least_squares(errfunc, init, bounds=bds, args=(self.datax, self.datay), max_nfev=10000)
        residuals = pfit.fun

        # Get the stdev of the residuals
        sigma_res = np.std(residuals)

        sigma_err_total = np.sqrt(sigma_res**2 + yerr_systematic**2)
        self.sigma=sigma_err_total

        # 100 random data sets are generated and fitted
        ps = []
        for i in range(iterations):

            randomDelta = np.random.normal(0., sigma_err_total, len(self.datay))
            randomdataY = self.datay + randomDelta

            randomfit = least_squares(errfunc, init, bounds=bds, args=(self.datax, randomdataY))

            ps.append(randomfit.x) 

        # Combining fits
        master_list=[]
        indexed=[]
        for k in range(len(ps[0])): # 0-6
            it=[]
            for i in range(len(ps)): # 0-1000
                it.append(ps[i][k])
            master_list.append(it)
        self.master_list=master_list

        ##################################################################################
        ## Below here there are two paths: median and asymmetric, or mean and symmetric ##
        ##################################################################################
        
        ## Asymmetric error method
        if mean==False:
            pfit_bootstrap=[]
            perr_pos=[]
            perr_neg=[]
            for i in master_list:
                pfit_bootstrap.append(np.median(i))
                perr_pos.append(np.percentile(i,84)-np.median(i))
                perr_neg.append(np.median(i)-np.percentile(i,16))
            
            perr_bootstrap=[]
            for i in range(len(perr_pos)):
                perr_bootstrap.append(str('[+')+str(perr_pos[i])+str(',-')+str(perr_neg[i])+str(']'))

            self.pfit=pfit_bootstrap
            self.perr_pos=perr_pos
            self.perr_nefitfuncg=perr_neg

        ## Symmetric error method
        else:
            pfit_bootstrap = np.mean(ps,0)
            self.pfit=pfit_bootstrap

            perr_bootstrap = np.std(ps,0)
            self.perr_sym=perr_bootstrap

        return (pfit_bootstrap, perr_bootstrap)


    def read_fits(self):
        """Pretty print of fit parameters"""
        if len(self.pfit) > 0:
            if len(self.perr_pos) > 0:
                print("")
                print("__________Asymmetric Errors__________")
                print("")
                for i in range(len(self.perr_pos)):
                    print(str(self.pfit[i])+str(' [+')+str(self.perr_pos[i])+str(',-')+str(self.perr_neg[i])+str(']'))
                if self.mu_offset != None:
                    print("")
                    print("OFFSET BETWEEN mu1 & mu2: "+str(round((self.pfit[4]-self.pfit[1]),2))+" km/s")
                    print("")

            elif len(self.perr_sym) > 0:
                print("")
                print("__________Symmetric Errors__________")
                print("")
                for i in range(len(self.pfit)):
                    print(str(self.pfit[i])+str(' +/- ')+str(self.perr_sym[i]))
                if self.mu_offset != None:
                    print("")
                    print("OFFSET BETWEEN mu1 & mu2: "+str(round((self.pfit[4]-self.pfit[1]),2))+" km/s")
                    print("")
            
        else:
            print("")
            print("You didn't fit anything!")
        return("")


    def plot_fit(self): ## Keep code running after showing plots
        """Plot fits on a logarithmic plot, scatterplot, histogram, or scatterplot and histogram"""


        try:
            plt.rcParams["patch.force_edgecolor"] = True
        except KeyError:
            pass


        more_data=np.linspace(np.min(self.datax), np.max(self.datax), 1000)
        
        if self.mu_offset != None:
            single= lambda p, x: np.abs(p[0])*np.exp(-0.5*((x-p[1])/p[2])**2)
            p_1 = [self.pfit[0], self.pfit[1], self.pfit[2]]
            p_2 = [self.pfit[3], self.pfit[4], self.pfit[5]]
            first = single(p_1, more_data)
            secod = single(p_2, more_data)
        else:
            pass

        real_func= self.fitfunc(self.pfit, more_data)
        
        print('')
        print('')
        print(">>> Select plot type for fitted function:")
        print("")
        print('>>> For a logarithmic plot, enter: log')
        print('>>> For histogram plot, enter: hist')
        print('>>> For a scatter plot, enter: scat')
        print('>>> For a superimposed scatter plot on a histogram, enter: scat_hist')
        print('')
        
        try:
            method=raw_input('> ')
        except NameError:
            method=input('> ')

        if method=='log':
            plt.loglog(self.datax, self.datay, 'o')
            plt.errorbar(self.datax, self.datay, ls='none', yerr=self.sigma/2) ## yerr= 2*N
            plt.loglog(more_data, real_func)

        elif method=='scat':
            plt.errorbar(self.datax_bins, self.datay, xerr=self.binwidth, ls='none', yerr=self.sigma)
            plt.plot(self.datax_bins, self.datay,'ro')
            plt.plot(more_data, real_func)
            if self.mu_offset != None:
                plt.plot(more_data, first)
                plt.plot(more_data, secod)

        elif method=='hist':
#            plt.errorbar(self.datax_bins,self.datay,xerr=self.binwidth,ls='none', yerr=self.sigma)
            plt.hist(self.datax, bins=int(self.bins))
            plt.plot(more_data, real_func)
            if self.mu_offset != None:
                plt.plot(more_data, first)
                plt.plot(more_data, secod)

        elif method=='scat_hist':
            try:
                plt.rcParams["patch.force_edgecolor"] = True
            except KeyError:
                pass
            plt.errorbar(self.datax_bins,self.datay,xerr=self.binwidth,ls='none', yerr=self.sigma)
            plt.hist(self.datax, bins=int(self.bins))
            plt.plot(self.datax_bins, self.datay, 'ro')
            plt.plot(more_data, real_func)
            if self.mu_offset != None:
                plt.plot(more_data, first)
                plt.plot(more_data, secod)

        else:
            print('>>> Specify which method of plotting, log or scat_hist')

        plt.show()



    def populate_bins(self, binwidth):
        """Fit to histogram"""

        errfunc = lambda p, x, y: (y - self.fitfunc(p, x))        

        ## Number of bins
        binN=math.ceil((np.max(self.datax)-np.min(self.datax))/binwidth)

        ## Preparing historgram
        y,x=np.histogram(self.datax,int(binN))
        x=(x[1:]+x[:-1])/2 # for len(x)==len(y)
        data=np.vstack((x,y)).T
        
        ## Bins and their respective populations
        self.binwidth = binwidth
        self.bins = binN
        self.datax_bins = data[:,0]
        self.datay = data[:,1]
        self.sigma = data[:,1]**0.5


    def p_spread(self):
        """ View the function parameter distribution given by the fit"""

        try:
            plt.rcParams["patch.force_edgecolor"] = True
        except KeyError:
            pass
        
        rows=np.ceil(float(len(self.master_list))/3)
        for i in range(len(self.master_list)):
            plt.figure(2)
            pylab.subplot(3,rows,i+1)
            plt.hist(self.master_list[i])
            plt.title('p'+str(i))
        plt.show()


    def reduced_chi_sq(self):
        """Calculates reduced chi_square for any fitted function"""

        errfunc = lambda p, x, y: (y - self.fitfunc(p, x))

        ## Returning residuals
        self.residuals = errfunc(self.pfit, self.datax, self.datay)
                
        try:
            ## Vector of chi-square[i] for one dimensional
            vect=[]
            for i in range(len(self.residuals)):
                vect.append(self.residuals[i]**2/(self.bins-len(self.pfit)))
            self.chi_square_statistic = sum(vect)
            self.chi_square_df = self.bins-len(self.pfit)

        except TypeError:
            ## Vector of chi-square[i] for multi-dimensional
            vect=[]
            for i in range(len(self.residuals)):
                vect.append(self.residuals[i]**2/(len(self.datax)-len(self.pfit)))
            self.chi_square_statistic = sum(vect)
            self.chi_square_df = len(self.datax)-len(self.pfit)
            #self.chi_square_p = 1-chi2.cdf(self.chi_square_statistic, df)



class Fit_Xray(Fit_Astro):
    """
    Fit xray surface brightness and density function using bootstrap residuals or input errors. 
    """
    
    def __init__(self, datax, datay, sigma=[]): ## FIX INHERITANCE BS
        self.datax = datax
        self.datay = datay
        self.sigma = sigma
        self.density = []
        self.y_density = []
        self.fitfunc = []
        self.pfit = []
        self.perr_sym = []
        self.perr_pos = []
        self.perr_neg = []
        self.chi_square = []
        self.binwidth = []
        self.bins = []
        self.datax_bins=[]
        self.master_list = []
        self.residuals= []
        self.chi_square_statistic = []
        self.chi_square_df = []
        self.mu_offset = None

    def fit_xray_sb(self, init, bds, yerr_systematic=0, iterations=1000, mean=False): ## THIS HAS MANY UNRESOLVED ISSUES
        """ Fit x-ray surface brightness """    
    
        from scipy.special import beta, betainc

        self.fitfunc = lambda p,r: (p[1]*p[2]*((beta(p[3]-0.5,0.5))/(beta(p[4]-0.5,0.5)))*(r/p[0])**((-2)*p[3]+1))*np.piecewise((r/p[0]),[(r/p[0])**2<1,(r/p[0])**2>=1], [lambda A: 1-betainc(p[4]-0.5,0.5,A**2), lambda A: 0])  + (p[2]*(r/p[0])**((-2)*p[4]+1))*np.piecewise((r/p[0]),[(r/p[0])**2<1,(r/p[0])**2>=1],[lambda A: betainc(p[4]-0.5,0.5,A**2), lambda A: 1])

        if len(self.sigma)==0:
            self.fit_residuals(init, bds, yerr_systematic=0, iterations=iterations, mean=mean)
        else:
            self.fit_errors(init, bds, sigma=self.sigma, iterations=iterations, mean=mean)




    def fit_xray_density(self): ## THIS IS JUST WRONG
        """ Fit x-ray density """

        self.density = lambda p,r: np.piecewise(r, [r<p[0], r>=p[0]], [lambda r: p[1]*p[2]*(r/p[0])**-p[3], lambda r: p[2]*(r/p[0])**-p[4]])

        xdata=self.datax ## Bug in np.piecewise prevents self.datax from being read as datax

        self.y_density=np.piecewise(xdata, [xdata<self.pfit[0], xdata>=self.pfit[0]], [lambda xdata: self.pfit[1]*self.pfit[2]*(xdata/self.pfit[0])**-self.pfit[3], lambda xdata: self.pfit[2]*(xdata/self.pfit[0])**-self.pfit[4]]) ## USED FOR ERROR PLOTTING


    def xray_plots(self):
        """Plot x-ray surface brightness and density on a logarithmic plot"""

        try:
            plt.rcParams["patch.force_edgecolor"] = True
        except KeyError:
            pass

        more_data=np.linspace(np.min(self.datax), np.max(self.datax), 1000)

        surf_bright = self.fitfunc(self.pfit, more_data)
        density = self.density(self.pfit, more_data)

        ######### Plotting Sim & Fitted Function ##########
        plt.subplot(121)
        plt.loglog(more_data,surf_bright)
        plt.errorbar(self.datax, self.datay, ls='none', yerr=self.sigma/2) ## yerr= 2*N
        plt.title('Surface Brightness')
        plt.ylabel('$cts/s/arcsec^-2$')
        plt.xlabel('Log (arcsec)')

        plt.subplot(122)
        plt.loglog(more_data,density)
        plt.errorbar(self.datax, self.y_density, yerr=self.y_density**0.5) ## yerr= 2*N
        plt.title('Electron Density')
        plt.ylabel('$N_e (cm^-3)$')
        plt.xlabel('Distance (arcsec)')
        plt.tight_layout()

        plt.show()






