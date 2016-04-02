'''
tools for the auditory neuroscientist

author: erik lee nylen
last update: 3/25/16

quick use:
from command line, go to folder containing soundTransformation.py and type:
python soundTransformations.py

includes functions:
	dBtoPa: a function for converting decibel list to Pascals
	PatodB: a function for converting from Pascals to decibels

	suite of functions for fitting data to the Maximum acceleration
	of Peak Pressure function as described by Peter Heil.  The model,
	while not mechanistic, provides a framework for understanding how
	the latencies of auditory neurons vary as  a function of the 
	Maximum Acceleration of Peak Pressure.  The model fitting routines
	are provided, with a fully loaded 

	model fitting can be modified for generalized modeling problems
	using least sqaures optimization



'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy import stats

def dBtoPa(vectin):
    '''convert vector of decibels values to Pascals'''
    return [np.exp(float(_)/float(20))*2/(10**5) for _ in vectin]	

def PatodB(vectin):	
    '''convert vector (list) of Pascals to decibels'''
    return [20.*np.log(_*(10**5)/2) for _ in vectin]

def rateDetector(stimulusIn):
    stimulusIn = [0]+stimulusIn
    return np.diff(stimulusIn)

def residualsMapp(p,y,x,errors=[]):
    '''calculates the residual error of the maximum acceleration of peak pressure'''
    Lmin,S,x0,a = p
    err = (y - (Lmin + a/(np.log(x-x0)+S)**4))
    return err

def pevalMapp(x,p):
    '''evalutes the maximum acceleration of peak pressure
    function as described by Peter Heil:
    Heil P: Auditory cortical onset responses revisited. I. 
    First-spike timing. J Neurophysiol 1997, 77:2616-2642.'''
    return p[0] + p[3]/(np.log(x-p[2])+p[1])**4

def mappFit(x,p0,y_meas,errs=[]):
    '''least squares fit of the spike latencies'''
    plsq = leastsq(residualsMapp,p0,args=(y_meas,x,errs))   
    return pevalMapp(x, plsq[0])

def exampleMappFit(x=np.arange(2,6,.1), S = .5, Lmin=10,x0=0.5,a=13.3):
    '''function provides an example figure of simulated neural timing data
    and fits these data with the model as described by Heil 

    Example usage:
    soundTransformations.exampleMappFit()
    '''
    fig = plt.figure()
    y_true = Lmin + a/(np.log(x-x0)+S)**4
    simErrors=[max(.01,abs(_*_ind/50)) for _ind,_ in enumerate(10*np.random.randn(len(x)))]
    y_meas = y_true + np.random.randn(len(x))
    p0 = [20,1,-3,13.3] # lmin, S, dx, Amp
    plsq = leastsq(residualsMapp,p0,args=(y_meas,x,simErrors))
    y_predict = pevalMapp(x, plsq[0])
    print 'plsq', plsq[0]
    plt.plot(x, y_predict,'o',c='k')
    plt.plot(x,y_true,c='k')
    plt.plot(x,y_meas,'x',c='k')
    plt.title('Least-squares fit to noisy sim, S='+str(S)+', Lmin='+str(Lmin)+', x0='+str(x0)+', a='+str(a)+'',style='italic')
    plt.legend(['Fit, r2 = '+str(np.round(rsquared(y_predict,y_meas),3)), 'True', 'Noisy error'])
    plt.xlabel('simulated MAPP (Pa/s^2)',style='italic');plt.ylabel('latency (msec)',style='italic')
    plt.savefig('Least-squares fit to noisy data, S='+str(S)+', Lmi='+str(Lmin)+', x0='+str(x0)+', a='+str(a)+'.png' )

def rsquared(x,y):
    '''easy way to just get the rsquared value'''
    slope,intercept,r_value,p_value,std_err=stats.linregress(x,y)
    return r_value    

if __name__ == "__main__":
    exampleMappFit()
